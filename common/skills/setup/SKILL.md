---
name: setup
description: >
  Set up DAISO for a new engineer — prerequisites, clone, Samba access.
  Use when: setup, onboard, new user, first time, configure, install, getting started.
---

# Setup DAISO — Guided Onboarding

## When to use
- New engineer joining DAISO for the first time.
- Reconfiguration needed (new product, new domain).

This is a **one-time setup**. Once complete, future sessions skip straight to the greeting.

## How to guide
- Walk the engineer through ONE step at a time.
- Wait for confirmation ("done", "ready", "next") before moving on.
- If a step fails, help troubleshoot before continuing.

---

## Step 1: Prerequisites

**VS Code extensions** (required):
- GitHub Copilot
- GitHub Copilot Chat

**Git on Windows** — required to clone the repo. Test from any PowerShell or VS Code terminal:
```powershell
git --version
```
If "command not found" or similar, install Git:
```powershell
winget install --id Git.Git -e --source winget
```
After install, **close and reopen the terminal** so PATH refreshes. If `winget` itself fails behind Intel proxy, run the installer manually after setting:
```powershell
$env:HTTP_PROXY  = "http://proxy-chain.intel.com:911"
$env:HTTPS_PROXY = "http://proxy-chain.intel.com:911"
```
(Alternative proxies: `proxy-chain.intel.com:912`, `proxy-dmz.intel.com:911`.)

**Python on Windows** — required to run DAISO tools. Test:
```powershell
py --version
```
If not found, install from https://www.python.org/downloads/ or:
```powershell
winget install --id Python.Python.3.12 -e --source winget
```

---

## Step 2: Clone your team's DAISO repo in VS Code

Before starting, get your **team's repo URL** from your DAISO champion (it's the GitHub repo your team created from the DAISO template — e.g. `https://github.com/<your-org>/<your-team-daiso>.git`).

Open VS Code. You should see the **Welcome** tab (if not, `Help → Welcome`). At this point no folder is open yet — that's fine. Pick **one** of the two paths below.

### Path A (recommended): VS Code's built-in clone

This is the easiest path and avoids the nested-folder trap because VS Code creates the subfolder for you.

1. On the Welcome tab, click **"Clone Git Repository..."**.
   - Or: `Ctrl+Shift+P` → type `Git: Clone` → Enter.
2. **Paste your team's repo URL** when prompted and press Enter.
3. VS Code opens a folder picker: **"Select Repository Location"**. Pick (or create) a *parent* folder — e.g. `C:\vs_projects`. **Pick the parent, not a folder with the repo name.** VS Code creates the subfolder for you.
4. When the clone finishes, VS Code asks **"Would you like to open the cloned repository?"** → click **Open**.

If clone fails:
- "Git not found" → go back to Step 1 and install Git, then restart VS Code.
- Authentication prompt → sign in with your GitHub account in the VS Code popup (or use a Personal Access Token as the password).
- Network error → check Intel proxy if you're off VPN.

### Path B: Terminal clone (if you prefer the command line)

1. **Pick (or create) a *parent* folder** — e.g. `C:\vs_projects`. This is the folder that will *contain* your repo, not the repo itself.
2. **File → Open Folder...** and select that parent folder.
3. **View → Terminal** (or `` Ctrl+` ``). Confirm with `pwd` that you're in the parent.
4. **In the terminal, run:**
   ```powershell
   git clone <your-team-repo-url>
   ```
5. **File → Open Folder...** again, this time pick the newly created repo folder.

**Recovery — if you already opened an empty folder by mistake:** In the terminal (already inside that folder), run `git clone <your-team-repo-url> .` — the trailing dot clones into the current folder. The folder must be empty.

### Confirm

Whichever path you took, the file explorer on the left should now show `common/`, `packs/`, `README.md`, etc.

---

## Step 3: Choose your domain(s) and product

Ask: *"Which domain(s) do you work in? Pick one or more from the packs available under `packs/` in the repo."*

Ask: *"What product?"* (e.g. `nvl`, `ptl`, `arl`)

---

## Step 4: Set up Samba access

DAISO tools access NFS files (deposit lists, emulation logs, coverage data) directly from Windows via Samba. No files need to be copied to VNC.

Ask: *"What Samba server do you use?"* (default: `sc8-samba.sc.intel.com`)

If the engineer is at a different Intel site, look up their Samba server from `common/lib/paths.py` → `SAMBA_SERVERS` dict. Common sites:
- SC8 (default): `sc8-samba.sc.intel.com`
- IIL/LC (Israel): `samba.iil.intel.com`
- PDX: `samba.pdx.intel.com`
- FM: `samba.fm.intel.com`

Full mapping: https://wiki.ith.intel.com/spaces/HPCTraining/pages/1803211685/How+do+I+access+Samba

Ask: *"What NFS disk do you use?"* (default: `mfg_nvl_016`)

Authenticate the Samba session (one-time per Windows login):
```powershell
net use "\\<samba>\nfs\site\disks\<nfs-disk>" /user:<idsid>
```
The engineer types their password when prompted.

Verify access:
```powershell
Test-Path "\\<samba>\nfs\site\disks\<nfs-disk>\<idsid>"
```
Should print `True`. If `False`:
- Wrong Samba server — try `sc8-samba.sc.intel.com`, `samba.iil.intel.com`, or ask IT.
- Wrong NFS disk — ask the engineer for their actual disk path.
- Authentication failed — re-run `net use` with correct credentials.

---

## Step 5: Verify tools work

Test that DAISO tools can read NFS files via Samba. Run a tool from your domain's pack:
```powershell
py packs\<domain>\tools\cli.py --help
```

If Python errors occur:
- "py not found" → go back to Step 1 and install Python.
- Import errors → check that the workspace is the `daiso` folder (not a parent).

---

## Step 6: Save Profile

Save the engineer's identity to `.daiso-profile.toml` (gitignored, local-only). This lets other skills (like `bootstrap-pack`) skip re-asking who they are.

Create the file at the repo root:
```toml
# DAISO Engineer Profile — local only, not committed
# Re-run setup to regenerate

[engineer]
idsid = "<idsid>"
name = "<full name if given, otherwise omit>"

[domain]
pack = "<domain>"          # matches a folder under packs/
product = "<product>"      # e.g. nvl, ptl, arl

[samba]
server = "<samba server>"  # sc8-samba.sc.intel.com
nfs_disk = "<nfs disk>"    # mfg_nvl_016
```

Use `vscode_askQuestions` to ask for the IDSID if not already known:
- **"What's your IDSID?"** (e.g., `amaraaba`) — *"Your Intel login ID. Used for git branches and NFS paths."*

Write the file with the answers collected during setup.

---

## Step 7: Confirm

> *"You're all set. Domain(s): <domains>. Product: <product>.*
> *Your profile is saved in `.daiso-profile.toml` (local only, not committed).*
> *To stay updated, just say 'pull latest' or run `git pull` in the terminal.*
> *To add another domain later, just tell me."*
