# daiso-template — Build Your Team's AI Assistant

> GitHub Copilot knows Python. daiso-template knows *your* tools, products, and workflows.

**daiso-template is a forkable template.** Your team clones it, adds your own knowledge, and gets an AI assistant that understands your domain — your NFS paths, your CLI tools, your products, your debug patterns. You own the repo. You own the data.

---

## Why daiso-template?

Generic GitHub Copilot is powerful for code. But when an engineer asks:

> *"What's the right command for this job?"*
> *"Why is this check failing on our product?"*
> *"What does this internal test name decode to?"*

...generic Copilot can't help. It doesn't know your tools, your infrastructure, or your team's accumulated knowledge.

daiso-template closes that gap. You feed it your team's knowledge once — then every engineer on your team gets an expert assistant that knows your world.

---

## Quick Summary — Share This With Your Team

**daiso-template is a forkable template** for Intel teams to build a **domain-expert AI assistant**. Instead of configuring infrastructure or writing complex plugins, you:

1. **Fork the template** (this repo) to your team's GitHub
2. **Create your team's pack** — add your domain rules, tools, and knowledge as Markdown files
3. **Engineers clone and say "set me up"** in Copilot Chat → 5-minute guided setup
4. **Grow over time** — engineers teach the AI using "capture this" and "teach the AI" prompts

**What you get:**
- ✅ Copilot learns your tools, products, and workflows
- ✅ Every engineer gets a personal expert assistant
- ✅ Knowledge stays in Git (version control, team history)
- ✅ No infrastructure, no database, no complexity
- ✅ Setup takes ~15 minutes for a new team

**Example use cases:**
- *"What's the right command to run this test?"* → AI knows your test framework + product + flags
- *"Debug this error"* → AI knows your common failure patterns + logs + tools
- *"Generate the runbook"* → AI knows your process + templates + team rules

**Get started:** See "Getting Started" below, or jump to [`templates/pack-checklist.md`](templates/pack-checklist.md) for a detailed checklist.

---

## How It Works

```
DAISO template (this repo)
    └── Your team clones/forks it → your-team-daiso (your own GitHub repo)
            ├── common/               ← shared AI rules, NFS lib, skills (don't touch)
            ├── packs/
            │   └── <your-domain>/    ← YOUR team's content lives here
            │       ├── instructions.md    ← rules the AI always follows
            │       ├── skills/            ← guided workflows ("how to do X")
            │       ├── knowledge/         ← reference docs, guides, data tables
            │       └── tools/             ← Python tools the AI can run on your behalf
            └── templates/            ← starter files for skills, knowledge, tools
```

The `common/` layer handles all the infrastructure — NFS/Samba path translation, git workflow, onboarding, and shared skills. Your team only writes the domain-specific content inside `packs/<your-domain>/`.

---

## What You Can Teach It

| Content type | What it does | Where it lives |
|---|---|---|
| **Instructions** | Rules the AI always follows for your domain | `packs/<domain>/instructions.md` |
| **Skills** | Step-by-step playbooks (e.g. "how to run a job", "how to deposit a file") | `packs/<domain>/skills/<name>/SKILL.md` |
| **Knowledge guides** | Reference docs, architecture notes, debug guides | `packs/<domain>/knowledge/guides/` |
| **Knowledge data** | Structured lookup tables (TOML) — glossaries, config maps, decoders | `packs/<domain>/knowledge/data/` |
| **Tools** | Python functions the AI runs on your behalf — reads NFS files, parses logs, generates commands | `packs/<domain>/tools/` |

The AI gets smarter every time someone on your team says **"teach the AI"** or **"capture this debug"** — Copilot writes the content and saves it to the right place.

---

## Getting Started (New Team)

### Step 1 — Fork this template to your team's GitHub

Create your team's own repo from this template:

```
https://github.com/amaraaba/daiso-template
  → Click "Use this template" (top right)
  → Name it: my-team-daiso (or your team's name)
  → Create repository
```

You now have your team's independent copy.

### Step 2 — Create your pack

```
packs/
└── <your-domain>/            ← name it after your team or domain (e.g. "firmware", "dft", "platform")
    ├── instructions.md       ← start here: 5–10 rules the AI should always follow for your domain
    ├── products/
    │   └── <product>/        ← one sub-folder per product your team works on
    │       ├── config.toml   ← product-specific paths, project names, settings
    │       └── knowledge/
    │           ├── guides/   ← how-to guides, architecture notes, debug playbooks
    │           └── reference/← deep reference docs, tool documentation
    └── skills/               ← add skills as your team identifies repeated workflows
```

Use the example packs under `packs/example-domain-*/` as reference.
Full checklist: [`templates/pack-checklist.md`](templates/pack-checklist.md)

### Step 3 — Assign a champion

One person on your team owns the pack — reviews PRs, keeps instructions accurate, and encourages the team to contribute. This is the most important step for long-term success.

### Step 4 — Invite your team

Share your repo with your team. Each engineer:

1. Clones the repo:
```powershell
git clone https://github.com/<your-org>/<your-team-daiso>.git
```

2. Opens the folder in VS Code

3. **In Copilot Chat, says:** `set me up`

Copilot will guide them through onboarding (~3 minutes). Profile is saved locally (not committed).

---

## Day-to-Day Usage

Once set up, engineers talk to Copilot in VS Code. No commands to remember.

| Say this | Copilot does this |
|---|---|
| `"set me up"` | Guided first-time setup |
| `"help"` / `"what can you do"` | Lists available skills for your domain |
| `"teach the AI"` | Saves new knowledge or a correction to your pack |
| `"capture this debug"` | Extracts root cause + fix from the conversation and saves it |
| `"save my changes"` | Git branch → commit → PR — no git knowledge needed |
| `"pull latest"` | Gets new skills and knowledge your team has merged |

---

## How the AI Gets Smarter Over Time

```
Engineer hits a problem
    → solves it with Copilot's help
    → says "capture this debug"
    → Copilot writes a knowledge guide and saves it
    → engineer says "save my changes" → champion merges the PR
    → next engineer with the same problem gets the answer instantly
```

Your pack accumulates your team's collective knowledge. The more it is used, the more useful it becomes.

---

## Architecture

```
GitHub (your team's repo — source of truth)
    └── git clone → Windows (VS Code workspace)
                    └── Samba → NFS (read/write files directly)
```

- **Windows** — Copilot reads instructions, skills, and knowledge. Python tools run locally.
- **NFS** — your team's files (logs, configs, data) accessed via Samba UNC paths. No VNC copy. No SSH.
- **Linux commands** — if your workflows require Linux tools, daiso-template generates the raw command string; the engineer pastes it into their Linux terminal.

---

## Repo Structure

| Folder | Purpose | Who edits it |
|--------|---------|--------------|
| `common/` | Shared AI rules, NFS/Samba lib, onboarding skills | Template maintainers |
| `packs/<domain>/` | Your team's domain knowledge and tools | Your team |
| `packs/example-domain-*/` | Example scaffolds showing the pack structure | Reference only |
| `templates/` | Starter files for skills, knowledge, and tools | Template maintainers |

---

## Contributing Back to the Template

If your team builds something that would benefit **all** DAISO users — a better shared skill, an improved template, a useful utility — open a PR against the original template repo. Your pack content stays yours; only truly generic improvements go upstream.

---

## Requirements

- **VS Code** with GitHub Copilot + GitHub Copilot Chat extensions
- **Python 3.8+** on Windows (for running pack tools)
- **Git** on Windows
- **Samba access** to your Intel NFS disks (for tools that read NFS files)
- A GitHub account with access to your team's repo

---

## Questions / Help

Open an issue on this repo, or ask your team's DAISO champion.
