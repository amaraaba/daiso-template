---
name: contribute-tool
description: >
  Add a new tool to a DAISO domain pack. Handles reading the source script
  (including from NFS), analyzing it, integrating into the pack's tool registry,
  wiring NFS path translation, and testing.
  Use when: add tool, add script, import tool, new tool, add this to the pack,
  make this a tool, register tool, integrate script, add function.
tools: [daiso/*]
---

# Contribute Tool

## When to use
Engineer has a Python script or function and wants to add it as a reusable tool in their domain pack.
Trigger phrases: "add this tool", "make this a DAISO tool", "add my script to the pack", "import this as a tool", "add a new tool"

## Flow

### 1. Identify the source

The engineer provides either:
- A **file path** (NFS or local) — read it. If NFS path on Windows, translate to Samba UNC first.
- A **code snippet** in the chat — use it directly.
- A **description** of what the tool should do — write it from scratch.

### 2. Identify the target pack

Ask which pack if unclear. Check what exists:
```
packs/<domain>/tools/
```

Each pack has its own structure. Inspect before adding:
- **array**: `tools.py` (8600+ lines, `TOOL_FUNCTIONS` dict), `cli.py` (CLI wrapper), plus helper modules (`tim_tools.py`, `emu_analyzer.py`, etc.)
- **scan / functional / reset**: Currently scaffolds (`.gitkeep` only). You'll create the initial tool file.

### 3. Analyze the source script

Before integrating, check:
1. **Dependencies** — does it import Intel-internal packages (e.g. `vaultmgr`, `itr_client`)? These won't work on Windows. Mark the tool as LINUX-ONLY.
2. **Hardcoded NFS paths** — any `/nfs/...` strings that should use `nfs_path()` for cross-platform support.
3. **Subprocess calls** — `os.system()`, `subprocess.run()` to Linux-only commands? Mark LINUX-ONLY.
4. **Function signatures** — identify the main callable functions, their parameters, and return types.
5. **Side effects** — does it write files, modify state, call external services? Flag as DANGEROUS.

Tell the engineer what you found:
> "This script has 3 functions. `parse_results()` is pure Python and will work on Windows. `run_flash_search()` calls `subprocess` — it's Linux-only. I'll add both but mark the Linux one."

### 4. Integrate into the pack

#### For a pack WITH existing tools (e.g. array):

**Option A — Small function (< 100 lines):** Add directly to the pack's main `tools.py`.
**Option B — Larger module (100+ lines):** Create a new file in `packs/<domain>/tools/` and import from it.

Then register in the pack's tool registry:
```python
# In tools.py, add to TOOL_FUNCTIONS dict:
TOOL_FUNCTIONS = {
    ...
    "new_tool_name": new_tool_function,
}
```

#### For a pack WITHOUT existing tools (scaffold):

1. Create `packs/<domain>/tools/tools.py` with the function(s).
2. Add a `TOOL_FUNCTIONS` dict at the bottom registering all functions.
3. Copy `packs/example-domain-a/tools/cli.py` as a template for `packs/<domain>/tools/cli.py`, updating the module docstring and import paths.
4. Remove the `.gitkeep` file.

### 5. Handle NFS paths

If any parameter accepts NFS paths:
1. Use a recognized path parameter name so CLI auto-translates: `path`, `master_path`, `output_path`, `log_path`, `run_dir`, `directory`, `deposit_list_path`, `path_a`, `path_b`, etc.
2. If the parameter name is custom, add it to `_path_keys` in the pack's `cli.py`.
3. Inside the function, use `nfs_path()` from `common/lib/paths.py` for any hardcoded NFS defaults:
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "lib"))
from paths import nfs_path

DEFAULT_DATA = nfs_path("/nfs/site/disks/mfg_nvl_016/shared/data.csv")
```

### 6. Handle Linux-only tools

If the tool requires Linux:
1. Add it to `_LINUX_ONLY` set in the pack's `cli.py`.
2. The CLI will block it on Windows with a clear message.
3. Tell the engineer it will work once SLES 15 is available.

### 7. Test

Run the tool via CLI to verify:
```powershell
py packs/<domain>/tools/cli.py new_tool_name --help
py packs/<domain>/tools/cli.py new_tool_name --arg1 value1
```

If it fails:
- **ImportError**: missing dependency — check if it's available on Windows.
- **Path errors**: NFS path not translated — check parameter name is in the path_keys list.
- **SyntaxError**: encoding issue — check for non-ASCII characters (em-dashes, smart quotes).

### 8. Update pack instructions

Add the new tool to the pack's `instructions.md` tool table so Copilot knows it exists:
```markdown
| Category | Tools |
|----------|-------|
| ... existing ... |
| New Category | new_tool_name |
```

### 9. Push

Use the `contribute` skill to commit and push the changes.

## Naming conventions

- Tool function names: `snake_case`, verb-first (e.g. `parse_results`, `query_coverage`, `generate_report`)
- Tool names in registry: same as function name
- Helper modules: descriptive `snake_case.py` (e.g. `coverage_tools.py`, `flash_parser.py`)

## Security rules

- NEVER include credentials, tokens, or API keys in tool code.
- Tools that modify files or run commands must be flagged as DANGEROUS in the tool definitions.
- Tools that accept path inputs must validate paths — no path traversal outside expected directories.
