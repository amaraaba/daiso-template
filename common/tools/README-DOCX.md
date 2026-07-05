# Import Word Documents as Knowledge Files

Convert `.docx` files (Word documents, OneNote exports, etc.) to Markdown and save them in your pack's knowledge guides.

## Quick Start

```powershell
cd /path/to/your/daiso-repo
py common/tools/docx_to_markdown_import.py `
  --docx "C:\path\to\document.docx" `
  --domain <your-domain> `
  --section-name "Document Title"
```

**Example:**
```powershell
py common/tools/docx_to_markdown_import.py `
  --docx "C:\Users\username\OneDrive - Intel Corporation\Documents\NVL-AX.docx" `
  --domain nvl-test `
  --section-name "NVL-AX Architecture"
```

## What It Does

1. **Reads** `.docx` file
2. **Converts** to Markdown
3. **Adds metadata** (YAML front-matter with title, source, section, import date)
4. **Saves** to `packs/<domain>/knowledge/guides/<section-name>/*.md`

## Output Format

Each converted document becomes a Markdown file with front-matter:

```markdown
---
title: Document Title
source: docx
section: NVL-AX Architecture
imported: 2026-07-05T12:34:56.789012
---

# Document content here

Converted from Word format...
```

## Options

| Option | Required | Description |
|--------|----------|-------------|
| `--docx` | ✅ Yes | Path to `.docx` file |
| `--domain` | ✅ Yes | Pack domain (e.g., `nvl-test`) |
| `--section-name` | ❌ No | Section name for front-matter (default: filename) |
| `--pack-root` | ❌ No | Pack root path (default: current directory) |

## Supported File Types

- **Word Documents** (`.docx`)
- **OneNote Exports** (OneNote can save sections as `.docx`)

## After Import

```powershell
# Check what was created
ls packs/<domain>/knowledge/guides/

# Review the Markdown
code packs/<domain>/knowledge/guides/<section-name>/

# Commit to git
git add packs/<domain>/knowledge/guides/
git commit -m "Add <section-name> documentation"
git push
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ERROR: packs/ not found` | Run from DAISO repository root |
| `ERROR: File not found` | Check file path, use absolute path with quotes if spaces |
| Conversion looks wrong | Document may have complex formatting; edit Markdown manually |
| Missing content | Check original `.docx` for protected sections or embedded objects |

## Technical Details

- **Dependencies:** `python-docx`, `html2text`
- **Installed by:** DAISO setup (see `setup` skill)
- **Source:** `common/tools/docx_to_markdown_import.py`
