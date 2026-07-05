---
name: review-changes
description: >
  Validate AI-generated content before pushing. Checks patspecs, configs,
  deposit lists, and other generated files against pack rules and common mistakes.
  Use when: review, check my work, does this look right, validate, sanity check,
  before I push, is this correct, QA, verify output.
tools: [daiso/*]
---

# Review Changes

## When to use
Engineer wants to validate content that Copilot generated (or that they edited) before pushing.
Trigger phrases: "does this look right?", "review my changes", "check this before I push", "validate", "sanity check"

## Why this exists
AI-generated content (patspecs, configs, deposit lists) can have subtle errors that pass syntax checks but cause silent failures on silicon. This skill catches common mistakes before they reach the vault.

## Flow

### 1. Identify what to review

Check `git diff` and `git status` to find modified/new files. Or the engineer points to a specific file.

Categorize each file:
- **patspec** (.config, .config.bz2 content)
- **deposit list** (.list)
- **TOML config** (.toml)
- **knowledge file** (.md, .toml in knowledge/)
- **skill** (SKILL.md)
- **tool code** (.py in tools/)

### 2. Apply validation rules per file type

#### PatSpec / Config files
- [ ] `PatternSpec` block name matches the test name convention for the pack
- [ ] `memory_instance_list` paths are syntactically valid (no typos in hierarchy)
- [ ] Algorithm name exists in the pack's algorithm DB (use `lookup_algorithm` tool if available)
- [ ] No duplicate fields inside a block
- [ ] `usage : pattern;` present (not `usage : scan;` unless scan pack)
- [ ] Flavor matches intent (e.g. `parallel_perstep` for per-memory, `parallel_allsteps` for full)

#### Deposit Lists
- [ ] Header comments present (`## twg.owner`, `## twg.testtype`, etc.)
- [ ] Every entry path exists (spot-check 2-3 via Samba)
- [ ] No duplicate entries
- [ ] Paths use consistent format (no mixed `/nfs/` and UNC)

#### TOML configs
- [ ] Valid TOML syntax (parse it)
- [ ] Required keys present for the pack (check pack's `config.toml` schema if available)
- [ ] No placeholder values left (`TODO`, `FIXME`, `<fill>`)

#### Tool code (.py)
- [ ] Imports resolve (no missing modules)
- [ ] Function registered in `TOOL_FUNCTIONS` if it's meant to be a tool
- [ ] No hardcoded `/nfs/` paths without `nfs_path()` wrapper
- [ ] No `subprocess` calls that would fail on Windows (unless in `_LINUX_ONLY`)
- [ ] No credentials or secrets

#### Knowledge / Skill files
- [ ] YAML front-matter is valid (for SKILL.md)
- [ ] No broken internal links
- [ ] No placeholder text

### 3. Report findings

Format:
```
✅ patspec_fit_pbp6_sari.config — PASS (6/6 checks)
⚠️ deposit.list — 1 issue:
   → Line 42: duplicate entry "cgc_fit_perbistport..."
❌ new_tool.py — 2 issues:
   → Line 15: hardcoded /nfs/ path without nfs_path()
   → Line 30: subprocess.run() but not in _LINUX_ONLY set
```

### 4. Offer to fix

For each issue found:
> "I found 2 issues. Want me to fix them, or just flag for you to review?"

If engineer says fix → apply corrections. If not → leave as-is.

### 5. Confirm ready to push

After all issues resolved:
> "All checks pass. Ready to push — say 'push' or use the contribute skill."

## What this does NOT do
- Run tests on silicon (can't)
- Guarantee correctness (validates format/rules, not functional behavior)
- Replace engineer judgment on algorithm selection or test intent
