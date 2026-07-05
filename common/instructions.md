# DAISO — Shared Instructions

These rules apply to all domains and all packs.

## Core Rules

- **ACT, DON'T DELEGATE** — use the CLI tools or terminal for actions. Don't tell the user to do things the AI can do.
- **NEVER FABRICATE COMMANDS** — tool commands, vault commands, and infrastructure commands MUST come from tool output or knowledge files. Wrong commands cause silent failures on production silicon.
- **ACTION BIAS** — when intent is clear but details are missing, pick a reasonable default and proceed.
- **STAY IN CONTEXT** — handle everything in one conversation. Never tell the user to switch tools or agents.
- **CITE SOURCES** — always reference the knowledge file or tool output that informed your answer. If nothing found: "NOT_FOUND: <what was searched>".
- **NEVER HALLUCINATE FACTS** — never use general knowledge for claims about Intel silicon or internal processes.
- **ANSWER FIRST** — lead with the root cause or answer. Put supporting detail below.
- **EXPLAIN WHEN ASKED** — skip tutorials by default. If the engineer asks "why?" or "explain", then go deeper.

## Tool Execution

DAISO tools are Python functions in `packs/<domain>/tools/`. They run locally on Windows, accessing NFS files via Samba.

### Running tools via CLI
```powershell
py packs/<domain>/tools/cli.py <tool_name> [--arg1 value1] [--arg2 value2]
py packs/<domain>/tools/cli.py --help    # list all available tools
```

NFS paths (`/nfs/...`) are auto-translated to Samba UNC paths on Windows by the CLI.

### Accessing NFS files

All NFS files are accessed directly from Windows via Samba UNC paths. No files need to be copied to VNC.

**When an engineer gives an NFS path** like `/nfs/site/disks/mfg_nvl_016/user/scripts/foo.py`:
1. Translate it to a Samba UNC path: replace `/nfs/` with `\\<samba-server>\nfs\` and `/` with `\`.
2. Default Samba server: `sc8-samba.sc.intel.com`. So `/nfs/site/disks/X` → `\\sc8-samba.sc.intel.com\nfs\site\disks\X`.
3. Use the UNC path with standard tools: `read_file`, `run_in_terminal`, `Get-Content`, etc.
4. To run a Python script on NFS: `py "\\sc8-samba.sc.intel.com\nfs\site\disks\...\script.py"`

If the engineer is at a different Intel site, ask which site and look up the Samba server from `common/lib/paths.py` → `SAMBA_SERVERS` dict (48 sites mapped). Or the engineer can set `DAISO_SAMBA_SERVER` env var.

**Path translation in Python** — use `common/lib/paths.py`:
```python
from paths import nfs_path, get_samba_for_site

# Auto-translates based on platform:
#   Windows → \\sc8-samba.sc.intel.com\nfs\site\disks\mfg_nvl_016\...
#   Linux   → /nfs/site/disks/mfg_nvl_016/...  (passthrough)
p = nfs_path("/nfs/site/disks/mfg_nvl_016/amaraaba/run_area")

# Look up Samba server for a different Intel site:
server = get_samba_for_site("iil")  # → samba.iil.intel.com
```

The default Samba server is `sc8-samba.sc.intel.com`. Engineers at other sites can override via `DAISO_SAMBA_SERVER` env var. The full 48-site mapping is in `common/lib/paths.py` → `SAMBA_SERVERS`.

**In the CLI**, pass NFS paths as-is — they are auto-translated:
```powershell
py packs/<domain>/tools/cli.py filter_deposit_list --filter_pattern lvlf --master_path /nfs/site/disks/mfg_nvl_016/yfriedgu/run_area/deposit.list
```

### Creating new tools

New tools go in `packs/<domain>/tools/`. Each pack defines its own tool structure. To add a tool, use the `contribute-tool` skill — it handles reading the source, integrating into the pack's tool registry, wiring path translation, and testing.

The general pattern:
1. Add the Python function in the pack's tools directory.
2. Register it in the pack's tool registry (e.g. array uses `TOOL_FUNCTIONS` dict in `tools.py`; other packs may differ).
3. If the pack has a CLI wrapper, the new tool is auto-discovered — no extra registration needed.

For path arguments that accept NFS paths, use parameter names from this list so CLI auto-translation works: `path`, `master_path`, `output_path`, `log_path`, `run_dir`, `directory`, `reference_patspec`, `dft_summary_path`, `deposit_list_path`, `path_a`, `path_b`.

### What tools CAN do
- Read/write files on NFS via Samba (deposit lists, coverage XLSX, patspecs, configs, logs)
- Parse and filter structured data (deposit lists, DFT summaries, emulation logs)
- Query knowledge bases and algorithm databases
- Generate commands for the engineer to run (vault, iTrace)
- Decode test names, validate configs, diff patspecs

### What tools CANNOT do (yet)
- Execute Linux commands (`vaultmgr`, `iTrace_manager`, `flash_search`, `vaultdeposit`, etc.)
- Source domain-specific environment scripts
- Run anything requiring CAD tools or project modules

### CRITICAL: DAISO is Windows-only — NEVER suggest `py packs/...` on Linux
DAISO lives ONLY in the engineer's Windows workspace (e.g. `c:\vs_projects\daiso`). It is NOT on the engineer's Linux/VNC host. Telling the engineer to paste `py packs/<domain>/tools/cli.py ...` into Linux WILL FAIL — the path does not exist there.

Rules for Linux-only / sourced-env commands (vaultmgr, iTrace_manager, vaultdeposit, flash_*, fbflow, EDA tools):

1. **NEVER** wrap them in a daiso CLI invocation when telling the engineer to run them on Linux.
2. **ALWAYS** produce the RAW underlying command (e.g. `vaultmgr -proj nvlhub_axa0 -q path LIKE %X% -- -pl test_id -- > out.list`) for the engineer to paste in their Linux csh pane.
3. Use the daiso `*_command` GENERATORS (`vault_query_command`, `vault_checkout_command`, `vault_modify_command`, `prepare_itrace_command`, etc.) — these are designed to **build the raw command string** that the engineer copy-pastes into Linux. Run the generator from Windows, hand over the resulting raw string.
4. **NEVER** call `run_in_terminal` on Windows for a Linux binary — it will fail with "file not found" or a clearer "requires Linux" error. If a daiso tool says "requires Linux", switch to the `*_command` generator path immediately.

#### Tool execution matrix
| Command type | Where it runs | How to deliver |
|---|---|---|
| daiso pack tools (read/parse/query/decode) | Windows (the AI) | Run via `run_in_terminal` or `py packs/<domain>/tools/cli.py ...` |
| `vaultmgr` read-only queries | Linux (sourced csh) | Build raw `vaultmgr` cmd → engineer pastes in Linux |
| `vaultmgr` checkout/checkin/modify/obsolete | Linux (sourced csh, engineer only) | Use `vault_*_command` generator → engineer pastes |
| `iTrace_manager` install/launch/kill | Linux (sourced csh, engineer only) | Use `prepare_itrace_command` → engineer pastes |
| `vaultdeposit`, `flash_*`, EDA tools | Linux (sourced csh, engineer only) | Build raw cmd → engineer pastes |

When SLES 15 arrives, the VS Code terminal will connect directly to VNC and these can run end-to-end.

### Compressed Logs
`.bz2` files can be read with Python's `bz2` module. The `analyze_sim_log` tool handles this automatically.

## Safety Rules

- NEVER modify files outside the engineer's designated workspace unless explicitly asked.
- NEVER run destructive commands without explicit user confirmation.

## Engineer Identity

The engineer's domain(s), product, and IDSID are saved in `.daiso-profile.toml` at the repo root (gitignored, local-only). Created during the `setup` skill. Samba server and NFS disk are also stored there, along with `.daiso-sync.conf`.

**At session start**, read `.daiso-profile.toml` to know who this engineer is. If the file is missing, run the `setup` skill.
