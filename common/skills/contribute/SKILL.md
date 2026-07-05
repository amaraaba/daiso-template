---
name: contribute
description: >
  Push new or modified skills, knowledge, or tools to the DAISO repo.
  Auto-detects changes, shows summary, lets engineer pick what to push.
  Use when: push changes, contribute, save skill, commit, share changes,
  submit, save my work, upload, send changes, done editing.
tools: [daiso/*]
---

# Contribute Changes

## When to use
Engineer created or modified content and wants to save/share it.
Trigger phrases: "save my changes", "submit", "commit", "I'm done", "push this", "share my work"

## Important
- **Engineers do NOT need to know git.** Copilot handles everything.
- Never ask the engineer to run git commands. Do it for them.
- **Only push when the engineer asks directly.** Trigger phrases listed above ("push my changes", "save my changes", "submit", etc.) count as a direct ask. Do NOT push as a side effect of any other workflow (saving a file, finishing a skill edit, ending a session).
- Never push without confirmation of *which* files.
- Never push to main directly — always branch + PR.
- **NEVER say "pushed" without a PR link in the same message.** This is the #1 rule of this skill. Extract the URL from `git push` output or build it: `https://github.com/amaraaba/daiso/pull/new/<branch>`. If the engineer has to ask "where's the link?", you violated this skill.
- Engineers may have **private or unfinished** work they do NOT want to push. Always ask.
- **Always give the engineer a clickable link after every push** — a new-PR link if it's a new branch, or a compare link if the branch already has an open PR. Never end a push without a link.

## Flow

### 1. Detect changes
Run `git status` to find what's changed. Show the engineer a simple summary:

> "You have these local changes:
> 1. Modified: `packs/<domain>/knowledge/guides/my-guide.md`
> 2. New file: `packs/<domain>/skills/new-skill/SKILL.md`
> 3. New file: `packs/<domain>/skills/my-private-notes/SKILL.md`

Do NOT show git terminology (staged, unstaged, tracked, etc.). Just "modified" and "new file", numbered.

### 2. Ask what to push

> "Which of these do you want to share? You can say:
> - **all** — push everything
> - **1, 2** — push only specific items (by number)
> - **none** / **cancel** — don't push anything"

Wait for the engineer's answer. Common patterns:
- "all" / "everything" → include all changed files
- "just 1 and 2" / "not 3" → include only the specified files
- "only the vault guide" → match by filename/description
- "skip the private one" → exclude anything with `private` or `my-` in the name

### 3. Submit only the selected files

```
git checkout -b <idsid>/<short-description>
git add <file1> <file2> ...          ← ONLY the files the engineer picked
git commit -m "<description of changes>"
git push -u origin <idsid>/<short-description>
```

**CRITICAL:** Use `git add <specific-files>` — NOT `git add -A`. Never push files the engineer didn't select.

Branch name: auto-generate from IDSID + brief description (e.g. `amaraaba/add-vault-guide`).
Commit message: auto-generate from the selected changes (e.g. "Add vault deposit guide for NVL").

### 4. Always show a link  — IN THE SAME MESSAGE AS THE PUSH CONFIRMATION

**HARD RULE:** the push-success message and the link must be sent together, in **one message**. Never wait for the engineer to ask for the link. If you find yourself writing "pushed!" without a URL in the same reply, you are violating this skill.

Pick the right link:

**Case A — brand-new branch (first push):**
`git push` output prints a new-PR URL like:
```
https://github.com/amaraaba/daiso/pull/new/<idsid>/<short-description>
```
If `git push` did not print one, build it: `https://github.com/amaraaba/daiso/pull/new/<branch-name>`

Tell the engineer:
> "Done! Branch pushed. **Click this link to open the PR page**, then click *Create pull request*:
> `<new-PR URL>`
>
> Your champion is auto-assigned as reviewer and gets an email."

**Case B — pushing more commits to a branch that already has an open PR:**
Do NOT send the new-PR link (GitHub will say a PR already exists). Instead, send a **compare link** so the engineer can see exactly what they just added on top of `main`:
```
https://github.com/amaraaba/daiso/compare/main...<idsid>/<short-description>
```

Tell the engineer:
> "Pushed your new commits. The existing PR is already updated automatically. Review the diff here:
> `<compare URL>`"

**How to tell which case you're in:**
- If you just ran `git checkout -b <new-branch>` in step 3 → Case A.
- If the branch already existed (you ran `git checkout <existing-branch>` and pushed more commits) → Case B. You can also detect this by inspecting `git push` output — GitHub prints either a `pull/new/...` URL (new) or no URL (existing branch).

**Rule:** never finish without sending exactly one of these two links **in the same message that announces the push succeeded**. The engineer must not have to ask "what about the link?".

### 5. Return to main
After pushing, switch back silently:
```
git checkout main
```

Unselected files remain as local changes on main — untouched and safe.

### 6. Getting updates (pull, not clone)
If the engineer says "pull latest", "update", "get new stuff":
```
git pull
```
That's it. No re-clone needed — ever. `git pull` brings in everything that was merged by others.
