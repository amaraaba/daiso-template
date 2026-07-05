"""
DAISO — OneNote Import Tool

Fetches all pages from one or more OneNote sections and saves them as
Markdown knowledge files under packs/<domain>/knowledge/guides/.

Usage:
    py common/tools/onenote_import.py --urls "<url1>" "<url2>" --domain firmware --pack-root .
    py common/tools/onenote_import.py --help

URL formats accepted (paste directly from OneNote "Copy Link to Section"):
    onenote:https://intel-my.sharepoint.com/.../Notebook.one#section-id={GUID}&end
    https://intel-my.sharepoint.com/.../_layouts/Doc.aspx?sourcedoc=...&wdsectionfileid={GUID}

Authentication:
    First run opens a browser for Microsoft (Intel SSO) login — one-time per session.
    Token is cached in .daiso-token-cache.json (gitignored).
    Set DAISO_ONENOTE_CLIENT_ID env var to use your own Azure AD app registration.
    Default uses Microsoft Graph Explorer public client (may be blocked on some tenants).
"""

import re
import os
import sys
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

import msal
import requests
import html2text

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Microsoft Office first-party client ID — pre-approved on most enterprise tenants.
# Override with DAISO_ONENOTE_CLIENT_ID env var or --client-id arg
# if your tenant blocks this too (requires your own Azure AD app registration).
DEFAULT_CLIENT_ID = "d3590ed6-52b3-4102-aeff-aad2292ab01c"

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
SCOPES = ["https://graph.microsoft.com/Notes.Read"]
TOKEN_CACHE_FILE = ".daiso-token-cache.json"

# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def parse_section_id(url: str) -> str | None:
    """
    Extract the OneNote section ID (GUID) from any SharePoint OneNote URL format.

    Handles:
      onenote:https://...#section-id={GUID}&end
      https://.../Doc.aspx?...&wdsectionfileid={GUID}&...
      https://.../Doc.aspx?...&wd=target(...|GUID/...)
    """
    url = url.strip()

    # Format 1: onenote: deep link — #section-id={GUID}
    m = re.search(r"section-id=\{([0-9A-Fa-f\-]{36})\}", url)
    if m:
        return m.group(1)

    # Format 2: wd=target(...|GUID/...) — OneNote section ID embedded in the wd param
    # This takes priority over wdsectionfileid which is a SharePoint item ID, not a OneNote ID
    m = re.search(r"wd=target%28[^|]+%7C([0-9A-Fa-f\-]{36})", url)
    if m:
        return m.group(1)

    # Format 3: wdsectionfileid={GUID} — fallback (SharePoint item ID, may differ from OneNote ID)
    m = re.search(r"wdsectionfileid=%7[Bb]([0-9A-Fa-f\-]{36})%7[Dd]", url)
    if m:
        return m.group(1)
    m = re.search(r"wdsectionfileid=\{([0-9A-Fa-f\-]{36})\}", url)
    if m:
        return m.group(1)

    return None


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def get_token(client_id: str, pack_root: Path) -> str:
    cache_path = pack_root / TOKEN_CACHE_FILE
    cache = msal.SerializableTokenCache()

    if cache_path.exists():
        cache.deserialize(cache_path.read_text())

    app = msal.PublicClientApplication(
        client_id,
        authority="https://login.microsoftonline.com/organizations",
        token_cache=cache,
    )

    # Try silent first (cached token)
    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    # Interactive browser login if needed
    if not result or "access_token" not in result:
        print("\nOpening browser for Microsoft login (Intel SSO)...")
        print("Sign in with your Intel account. This is a one-time step per session.\n")
        result = app.acquire_token_interactive(scopes=SCOPES)

    if "access_token" not in result:
        error = result.get("error_description") or result.get("error") or str(result)
        raise RuntimeError(f"Authentication failed: {error}")

    # Persist cache
    if cache.has_state_changed:
        cache_path.write_text(cache.serialize())
        print(f"Token cached at {cache_path} (gitignored).")

    return result["access_token"]


# ---------------------------------------------------------------------------
# Graph API helpers
# ---------------------------------------------------------------------------

def graph_get(token: str, path: str) -> dict:
    resp = requests.get(
        f"{GRAPH_BASE}{path}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    if resp.status_code == 404:
        raise RuntimeError(f"Not found: {path}\nCheck that the section ID is correct and you have access.")
    resp.raise_for_status()
    return resp.json()


def graph_get_raw(token: str, path: str) -> bytes:
    resp = requests.get(
        f"{GRAPH_BASE}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "text/html",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.content


# ---------------------------------------------------------------------------
# HTML → Markdown
# ---------------------------------------------------------------------------

def html_to_markdown(html_bytes: bytes) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0           # no line wrapping
    h.protect_links = True
    h.wrap_links = False
    return h.handle(html_bytes.decode("utf-8", errors="replace")).strip()


# ---------------------------------------------------------------------------
# Main import logic
# ---------------------------------------------------------------------------

def import_section(token: str, section_id: str, output_dir: Path) -> list[Path]:
    """Fetch all pages in a section and write them as .md files. Returns saved paths."""
    print(f"\n  Fetching section {section_id}...")

    # Get section metadata
    try:
        section = graph_get(token, f"/me/onenote/sections/{section_id}")
    except RuntimeError:
        # Try via sites endpoint for SharePoint-hosted notebooks
        section = graph_get(token, f"/me/onenote/sections/{section_id}")

    section_name = section.get("displayName", section_id)
    print(f"  Section: \"{section_name}\"")

    # Get pages
    pages_data = graph_get(token, f"/me/onenote/sections/{section_id}/pages?$select=id,title,createdDateTime,lastModifiedDateTime")
    pages = pages_data.get("value", [])

    if not pages:
        print("  No pages found in this section.")
        return []

    print(f"  Found {len(pages)} page(s). Fetching content...")

    # Safe folder name from section name
    safe_section = re.sub(r'[^\w\-]', '_', section_name).strip('_').lower()
    section_dir = output_dir / safe_section
    section_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for page in pages:
        page_id = page["id"]
        title = page.get("title") or "untitled"
        safe_title = re.sub(r'[^\w\-]', '_', title).strip('_').lower()

        print(f"    - {title}")

        # Fetch page HTML content
        html_content = graph_get_raw(token, f"/me/onenote/pages/{page_id}/content")
        markdown = html_to_markdown(html_content)

        # Add YAML front-matter
        created = page.get("createdDateTime", "")[:10]
        modified = page.get("lastModifiedDateTime", "")[:10]
        content = f"""---
title: "{title}"
source: onenote
section: "{section_name}"
imported: "{modified or created}"
---

{markdown}
"""
        out_path = section_dir / f"{safe_title}.md"
        out_path.write_text(content, encoding="utf-8")
        saved.append(out_path)

    return saved


def run(urls: list[str], domain: str, pack_root: Path, client_id: str):
    # Parse section IDs from URLs
    section_ids = []
    for url in urls:
        sid = parse_section_id(url)
        if sid:
            section_ids.append(sid)
            print(f"Parsed section ID: {sid}")
        else:
            print(f"WARNING: Could not parse section ID from URL:\n  {url}")

    if not section_ids:
        print("No valid section IDs found. Exiting.")
        sys.exit(1)

    # Authenticate
    token = get_token(client_id, pack_root)
    print("Authenticated OK.")

    # Output directory
    output_dir = pack_root / "packs" / domain / "knowledge" / "guides"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Import each section
    all_saved = []
    for sid in section_ids:
        saved = import_section(token, sid, output_dir)
        all_saved.extend(saved)

    # Summary
    print(f"\nDone. {len(all_saved)} file(s) saved to packs/{domain}/knowledge/guides/")
    for p in all_saved:
        rel = p.relative_to(pack_root)
        print(f"  {rel}")

    print("\nNext step: say 'save my changes' to commit and share with your team.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Import OneNote sections into DAISO knowledge files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--urls", nargs="+", required=True,
        help="One or more SharePoint OneNote section URLs (paste from 'Copy Link to Section')",
    )
    parser.add_argument(
        "--domain", required=True,
        help="Your pack domain name (e.g. firmware, dft, platform)",
    )
    parser.add_argument(
        "--pack-root", default=".",
        help="Root of the DAISO repo (default: current directory)",
    )
    parser.add_argument(
        "--client-id", default=None,
        help="Azure AD app client ID. Defaults to DAISO_ONENOTE_CLIENT_ID env var, then built-in public client.",
    )

    args = parser.parse_args()

    client_id = (
        args.client_id
        or os.environ.get("DAISO_ONENOTE_CLIENT_ID")
        or DEFAULT_CLIENT_ID
    )

    run(
        urls=args.urls,
        domain=args.domain,
        pack_root=Path(args.pack_root).resolve(),
        client_id=client_id,
    )


if __name__ == "__main__":
    main()
