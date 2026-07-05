---
name: setup
description: >
  Set up DAISO for a new engineer or a new team.
  Use when: set me up, setup, onboard, new user, first time, configure, install, getting started, I am new, help me get started.
---

# Setup DAISO — Guided Onboarding

## How to run this skill
- ONE step at a time. Wait for the user to confirm ("done", "ready", "ok", "next") before moving on.
- Run verification commands yourself in the terminal — do not just tell the user to run them.
- If a step fails, troubleshoot it before continuing. Never skip a failing step.
- Be conversational — this is a guided experience, not a form dump.

---

## Step 0: Understand who this is

Ask ONE question first:

> "Welcome! Quick question before we start — are you:
> **A)** Setting up DAISO for your team for the first time (you're the champion or tech lead)?
> **B)** Joining a team that already has DAISO set up?"

Go to **Path A** or **Path B** based on the answer.

---

## Path A — First-time team setup (champion / tech lead)

Use this path when no one on the team has set up DAISO yet.

### A1 — Check prerequisites

Run these in the VS Code terminal to verify:

```powershell
git --version
py --version
```

**If git is missing:**
```powershell
winget install --id Git.Git -e --source winget
```
After install: close and reopen the terminal, then re-verify with `git --version`.

If winget fails (Intel proxy):
```powershell
$env:HTTPS_PROXY = "http://proxy-chain.intel.com:911"
winget install --id Git.Git -e --source winget
```

**If Python is missing:**
```powershell
winget install --id Python.Python.3.12 -e --source winget
```

**VS Code extensions** — ask the user to confirm both are installed:
- GitHub Copilot
- GitHub Copilot Chat

(`Ctrl+Shift+X` → search "GitHub Copilot" — both should show as installed)

---

### A2 — Create your team's repo

Ask: *"Has your team already created a GitHub repo from the DAISO template?"*

**If no:**
1. Go to **https://github.com/amaraaba/daiso-template**
2. Click **"Use this template"** → **"Create a new repository"**
3. Name it (e.g. `my-team-daiso`). Private is recommended for internal teams.
4. Click **"Create repository"** and copy the repo URL.

**If yes:** get the URL from them and proceed.

---

### A3 — Clone and open in VS Code

If the repo is not yet open locally:

**Option 1 (recommended):** `Ctrl+Shift+P` → `Git: Clone` → paste the repo URL → pick a parent folder (e.g. `C:\vs_projects`) → click Open when prompted.

**Option 2 (terminal):**
```powershell
cd C:\vs_projects
git clone <your-repo-url>
```
Then `File → Open Folder` and select the newly created folder.

Verify the folder looks right — the explorer on the left should show `common/`, `packs/`, `README.md`.

---

### A4 — Create your team's pack

Check what packs already exist:
```powershell
Get-ChildItem packs\ -Directory | Select-Object Name
```

The `example-domain-*/` folders are reference scaffolds — ignore them for now.

Ask: *"What do you want to call your domain? Use a short name, lowercase, no spaces — e.g. `firmware`, `dft`, `platform`, `validation`."*

Create the pack structure:
```powershell
$domain = "<their-answer>"
New-Item -ItemType Directory -Force -Path "packs\$domain\skills", "packs\$domain\knowledge\guides", "packs\$domain\knowledge\reference", "packs\$domain\knowledge\data", "packs\$domain\products", "packs\$domain\tools"
New-Item -ItemType File -Force -Path "packs\$domain\instructions.md"
```

Open `packs\<domain>\instructions.md` and help them write the first 3–5 rules the AI should always follow for their domain. Ask:
- What internal tools does your team use?
- What are the most common mistakes to avoid?
- What products/silicon do you work on?

Keep each rule as one bullet. They can always add more later.

Ask: *"What product or project does your team work on?"* Create a product folder:
```powershell
$product = "<their-answer>"
New-Item -ItemType Directory -Force -Path "packs\$domain\products\$product\knowledge\guides", "packs\$domain\products\$product\knowledge\reference", "packs\$domain\products\$product\knowledge\data"
New-Item -ItemType File -Force -Path "packs\$domain\products\$product\config.toml"
```

---

### A5 — Samba / NFS access (optional)

Ask: *"Do your team's tools need to read files from Intel NFS disks (e.g. logs, configs, run outputs)?"*

**If no:** skip this step entirely.

**If yes:**

Ask:
- *"What's your Samba server?"* — look up in `common/lib/paths.py` → `SAMBA_SERVERS` if unsure. Common ones:
  - SC8: `sc8-samba.sc.intel.com`
  - IIL/Israel: `samba.iil.intel.com`
  - PDX: `samba.pdx.intel.com`
  - FM: `samba.fm.intel.com`
- *"What NFS disk path do your team's files live under?"* (e.g. `/nfs/site/disks/mfg_xxx_016`)

Authenticate (one-time per Windows login):
```powershell
net use "\\<samba-server>\nfs\site\disks\<disk>" /user:<idsid>
```
The user types their password when prompted.

Verify:
```powershell
Test-Path "\\<samba-server>\nfs\site\disks\<disk>"
```
Should return `True`. If `False`: wrong server or disk path — ask IT or the team's NFS admin.

---

### A6 — Save profile

Save the engineer's identity to `.daiso-profile.toml` at the repo root (gitignored — never committed).

Ask for their IDSID if not already known: *"What's your IDSID (your Intel login ID)?"*

Write the file:
```toml
# DAISO local profile — not committed, local machine only

[engineer]
idsid = "<idsid>"

[domain]
pack = "<domain>"
product = "<product>"

[samba]
enabled = <true or false>
server = "<samba-server or empty>"
nfs_disk = "<disk path or empty>"
```

---

### A7 — Commit and push the new pack

The new pack structure should be committed to the repo so the team can pull it.

Run:
```powershell
git add packs\<domain>\
git commit -m "Add <domain> pack scaffold"
git push
```

Share the repo URL with the rest of the team so they can follow **Path B** below.

---

### A8 — Confirm

> *"Your team's DAISO is ready. Pack: `<domain>`. Product: `<product>`.*
> *Share this repo URL with your team: `<repo-url>`*
> *They clone it and say 'set me up' — onboarding takes ~3 minutes.*
>
> *Next steps to get more value:*
> *- Say 'teach the AI' to add your first knowledge guide*
> *- Say 'what can you do' to see available skills*
> *- Check `templates/pack-checklist.md` for the full setup checklist"*

---

## Path B — Engineer joining an existing team

Use this path when the team already has a DAISO repo set up.

### B1 — Check prerequisites

Same as A1 — verify git, Python, and VS Code extensions.

---

### B2 — Get the repo URL

Ask: *"What's your team's DAISO repo URL? (Get it from your team's DAISO champion if you don't have it)"*

---

### B3 — Clone and open in VS Code

Same as A3.

---

### B4 — Choose your domain and product

Scan what packs exist:
```powershell
Get-ChildItem packs\ -Directory | Where-Object { $_.Name -notlike "example-domain*" } | Select-Object Name
```

Show the list and ask: *"Which domain do you work in?"*

Then ask: *"What product?"* — scan `packs\<domain>\products\` for existing products and show them.

---

### B5 — Samba / NFS access (optional)

Check if the pack has tools that use NFS:
```powershell
Test-Path "packs\<domain>\tools"
```

If tools exist, ask: *"Do you need to access NFS files from Windows for your work? (Your champion can tell you if unsure)"*

If yes — follow the same Samba setup as **A5**.
If no — skip.

---

### B6 — Save profile

Same as A6.

---

### B7 — Confirm

> *"You're all set. Domain: `<domain>`. Product: `<product>`.*
> *Profile saved locally in `.daiso-profile.toml` (not committed).*
>
> *Things to try:*
> *- Say 'what can you do' to see skills available for your domain*
> *- Say 'pull latest' to get new knowledge and skills your team has added*
> *- Say 'teach the AI' when you learn something the AI should know"*
