# OneNote Import Tool

Import OneNote sections directly into your DAISO pack as Markdown knowledge files.

## Quick Start

```powershell
py common\tools\onenote_import.py \
  --urls "https://intel-my.sharepoint.com/.../Section.one#section-id={GUID}" \
  --domain firmware \
  --pack-root .
```

## Setup (One-time)

Intel's Azure tenant blocks external apps. You need to create your own app registration:

1. Go to **https://portal.azure.com** → **App registrations** → **New registration**
2. **Name:** `daiso-onenote`
3. **Account type:** "Accounts in this organizational directory only"
4. **Redirect URI:** Web, `http://localhost`
5. Click **Register**
6. Copy the **Application (client) ID** (big UUID on the Overview page)
7. Go to **API permissions** → **Add a permission** → **Microsoft Graph** → **Delegated permissions**
8. Search for and add **`Notes.Read`**
9. Done — no admin approval needed

Save the client ID:
```powershell
$env:DAISO_ONENOTE_CLIENT_ID = "your-client-id-here"
```

## Usage

### Import One Section

Paste the URL from OneNote's "Copy Link to Section":

```powershell
py common\tools\onenote_import.py \
  --urls "https://intel-my.sharepoint.com/..." \
  --domain firmware \
  --pack-root .
```

### Import Multiple Sections

```powershell
py common\tools\onenote_import.py \
  --urls \
    "https://intel-my.sharepoint.com/.../Section-A.one#section-id={GUID1}" \
    "https://intel-my.sharepoint.com/.../Section-B.one#section-id={GUID2}" \
  --domain firmware \
  --pack-root .
```

## What Happens

1. First run opens a browser for Intel SSO login (one-time per session)
2. Tool fetches all pages in each section via Microsoft Graph API
3. Converts OneNote HTML to Markdown with YAML front-matter
4. Saves to `packs/<domain>/knowledge/guides/<section-name>/*.md`
5. You say **"save my changes"** in Copilot → team gets the knowledge

## Token Caching

Auth tokens are cached in `.daiso-token-cache.json` (gitignored). Delete it to force re-login.

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Consent...must be configured" | Create the Azure app above; set `DAISO_ONENOTE_CLIENT_ID` |
| "Not found" | Check section ID is correct; verify you have access to the notebook |
| "No pages found" | The section exists but has no pages |

## URL Formats

All these formats are supported (copy directly from OneNote):
- `onenote:https://...#section-id={GUID}`
- `https://.../Doc.aspx?...&wd=target(...\|GUID/...)`
- `https://.../Doc.aspx?...&wdsectionfileid={GUID}`
