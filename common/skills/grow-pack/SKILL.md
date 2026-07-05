---
name: grow-pack
description: >
  Add or fix knowledge, skills, or debug patterns in the engineer's DAISO pack.
  Enforces DAISO content standards, prevents duplicates, updates indexes.
  Use when: add knowledge, teach the AI, AI didn't know, wrong answer,
  missing info, I know a trick, add a skill, improve, fix instructions,
  the AI got this wrong, contribute knowledge, share what I learned,
  add to pack, update pack, new error, record fix, capture this,
  save what we found, record this debug, save this session.
---

# Grow Pack

Add content to an engineer's existing DAISO pack. Enforce standards, prevent duplicates, update indexes.

## When to use
- Engineer has knowledge the AI is missing
- Engineer wants to record a debug pattern or fix
- Engineer wants to add or improve a skill
- Engineer found wrong or outdated content
- **Engineer just finished a debug session in this conversation** and wants to capture it

## When NOT to use
- Engineer wants to wrap a script as a CLI tool → `contribute-tool`
- Engineer wants to push existing changes → `contribute`

---

## Procedure

### 1. Identify the contribution

Ask what they want to add. Don't show a menu — listen to what they say and classify it:

| What they describe | Content type | Target location |
|---|---|---|
| A fact, process, or reference the AI didn't know | Knowledge file | `knowledge/{guides,reference,data}/` |
| An error they debugged and fixed | Debug pattern | `skills/debug-workflow/SKILL.md` → Known Errors table |
| A multi-step workflow the AI should guide | Skill | `skills/<name>/SKILL.md` |
| Something wrong or outdated in existing content | Fix | Edit the existing file |
| **"capture this" / "save what we found"** — refers to the current conversation | **Session capture** | See below |

**Session capture** — when the engineer says "capture this", "save what we just found", "record this debug", or similar, they mean: extract from the current conversation history. Do NOT re-ask what happened. You were there.

1. Scan the conversation for: the error/problem, the investigation steps, the root cause, and the fix.
2. Draft the output automatically — no interview needed.
3. **Always create a Known Errors row** in `debug-workflow/SKILL.md`. Every debug capture gets an index entry — no exceptions.
4. **Additionally**, decide if a knowledge guide is warranted:
   - **Simple fix** (single error → obvious root cause → single fix) → Known Errors row is enough.
   - **Complex debug** (multi-step investigation, multiple files checked, non-obvious root cause) → also create a knowledge guide in `knowledge/guides/`. The Known Errors row links to it.
5. Show the draft: *"Here's what I captured from our session. Correct?"*
6. Proceed to step 2 (duplicate check) then step 4 (validate) as normal.

### 2. Check for duplicates

Before creating anything:

1. Read `.daiso-profile.toml` → domain, product.
2. Search `packs/<domain>/` for files matching the topic — knowledge file names, skill descriptions, instruction sections.
3. If a match exists, show it:
   > "This is already covered in `<path>`. Want to update it instead?"
   - If yes → edit the existing file (go to step 4).
   - If the engineer's content is genuinely different → proceed to step 3.

### 3. Generate content

Follow the standard for the content type.

#### Knowledge file

**Location:** `packs/<domain>/products/<product>/knowledge/<subdir>/<topic>.md`
- `guides/` for how-to and workflows
- `reference/` for specs, architecture, lookup tables
- `data/` for structured data (TOML, tables)

**Standards:**
- Max 100 lines. If longer, split into two files.
- Reference style: tables, bullets, exact paths and commands. No tutorials.
- File name: lowercase, hyphens, no spaces (`clock-domain-mapping.md`).
- First line after title: `<!-- Source: <URL or "engineer input"> -->` — cite where it came from.
- If the source is a wiki URL and Co-Design MCP is installed → fetch and summarize. If MCP is not installed → note `<!-- TODO: fetch from <URL> with Co-Design MCP -->`.

#### Debug pattern

**Location:** `packs/<domain>/skills/debug-workflow/SKILL.md` → `## Known Errors` table.

If the table or skill doesn't exist, create the skill first (use the standard debug-workflow template below).

**Standards:**
- One row per error. Four columns: error string, root cause, fix, guide reference.
- Error string must be verbatim — the AI uses it to match future occurrences.
- Fix must be actionable — a command to run or a specific setting to change, not "investigate further".
- Guide reference: if a knowledge guide exists for this error, link it. If not, leave empty.

Example row:
```
| MBIST DONE timeout after 500ms on ip6 | Clock override missing for ip6 bist port | Add iClockOverride in precat.pdl | `knowledge/guides/ip6-done-timeout-debug.md` |
```

**The Known Errors table is the master index.** Every debug capture — simple or complex — gets a row here. Knowledge guides provide the depth; the table provides the lookup.

#### Skill

**Location:** `packs/<domain>/skills/<skill-name>/SKILL.md`

**Standards:**
- YAML frontmatter with `name` and `description` (include `Use when:` with trigger keywords).
- Trigger keywords: pack with synonyms engineers actually type. 5-10 keywords minimum.
- Steps must be concrete: tool calls, commands, file paths. Not "analyze the situation".
- Include `## Key rules` with gotchas and constraints.
- Include `## Output format` showing what the answer to the user should look like.

#### Fix existing content

- Find the file containing the wrong content (search instructions, knowledge, skills).
- Show the engineer the current content and the proposed fix.
- Minimal edit — change only what's wrong. Don't restructure or "improve" surrounding content.

### 4. Validate

Before saving, check:

- [ ] **No duplicate** — step 2 confirmed no existing file covers this.
- [ ] **Right location** — file is in the correct `knowledge/`, `skills/`, or `data/` subdirectory.
- [ ] **Follows standards** — knowledge ≤ 100 lines, skill has YAML frontmatter + trigger keywords, debug row has all 3 columns.
- [ ] **No fabricated content** — everything came from the engineer's input, a file read, or an MCP fetch. Nothing invented.
- [ ] **File name** — lowercase, hyphens, descriptive (`emulation-timeout-debug.md` not `doc1.md`).

Show the engineer the final content and target path. Ask: *"Save this to `<path>`?"*

### 5. Save and integrate

After saving the file:

1. **Update the knowledge map** — if a knowledge file was added, check if `packs/<domain>/products/<product>/instructions.md` has a Knowledge Map table. If yes, add a row. If no, skip.

2. **Update the skills catalog** — if a skill was added, add a row to `packs/skills-catalog.md` with the skill name and trigger keywords.

3. **Check for skill graduation** — after saving a debug knowledge guide, scan `knowledge/guides/` for related files on the same topic area. If 3+ guides cover similar ground (e.g., multiple timeout debugs, multiple chain-fail debugs), suggest:
   > "You now have <N> debug guides about <topic>. There's a pattern here. Want me to create a `<topic>-debug` skill that automates this investigation? The skill would follow the steps from these guides automatically."
   
   If the engineer says yes, create the skill:
   - Pull the common investigation steps from the knowledge guides
   - Reference the guides as `## Key references`
   - Add the Known Errors rows from all related guides
   - The skill becomes the AI's playbook — next time the error hits, it follows the steps without the engineer having to drive

4. **Do NOT auto-push.** Tell the engineer:
   > "Saved to `<path>`. Say **push my changes** when you're ready to share with the team."

---

## Knowledge Pipeline

Content in DAISO follows a natural progression. Grow-pack supports every stage:

```
Session → Knowledge → Skill
```

| Stage | What happens | Trigger |
|-------|-------------|---------|
| **Session** | Engineer debugs with the AI in chat | Normal work |
| **Capture** | Engineer says "save this" → Known Errors row + knowledge guide | `grow-pack` (session capture) |
| **Accumulate** | Multiple guides on the same topic pile up | Happens naturally over days/weeks |
| **Graduate** | 3+ related guides → grow-pack suggests creating a skill | `grow-pack` (step 5 auto-detects) |
| **Skill** | AI follows the investigation steps automatically next time | Skill triggers on keywords |

**Every debug capture gets a Known Errors row.** That's the index. Knowledge guides provide depth. Skills graduate from proven patterns.

**Debug skills must search knowledge as a fallback.** When generating or graduating a debug skill, always include this step in the skill's procedure:

```markdown
## Steps
1. Match the error against the Known Errors table below.
2. If a match has a guide reference → read the guide for the full investigation path.
3. **If no match** → search `knowledge/guides/` for files related to the error keywords.
4. If still no match → gather context from logs and propose a new investigation.
```

This ensures no debug knowledge is orphaned — even if someone forgot to add the Known Errors row, the skill will still find the guide via search.
