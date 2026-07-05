---
mode: agent
description: "Build the DAISO (DTSE AI Solution) project from scratch based on this spec."
tools: [read, search, edit, execute, agent]
---

# DAISO — Full Project Build Spec v2

You are building **DAISO** (DTSE AI Solution) — a shared, federated AI assistant platform for Intel DTSE teams.

**Your job:** Scaffold the entire repo, create every file described below, and produce a working project. Follow this spec exactly.

---

## 1. Project Overview

DAISO is a shared platform where DTSE teams (Array, Scan, Functional, Reset) use the same AI infrastructure — VS Code + GitHub Copilot + MCP — but each team owns its own **content pack** with domain-specific instructions, skills, knowledge, and tools.

Each pack can support multiple **products** (NVL, PTL, LNL, etc.) with product-specific config, knowledge, and instructions — while sharing skills and tools across products.

### Key Principles

- One repo, federated ownership
- Standard primitives: Instructions, Skills, Knowledge, MCP Tools
- One shared MCP server, tools namespaced per team
- Shared NFS install — one copy, all engineers use it
- Supports both SSH mode (current) and local mode (after SLES 15 migration)
- 3-layer instructions: common → pack → product
- Product-specific knowledge separated from pack-level (product-agnostic) content
- Auto-detect engineer identity from SSH user + `~/.daiso.toml`
- Session start: greet by name, show active pack + what's new
- Contribution via auto-detect skill (diffs workspace vs main, pushes PR)
- No eval harness in Phase 1 — quality via champion review
- No personal skills tier in Phase 1
- Branding: **DAISO** everywhere
- Phase 1 scope: DTSE-IDC only. MPE/Oregon/DFx deferred.
- Pack names: `array`, `scan`, `functional`, `reset`
- English only

### AI Persona

- Senior peer — precise, direct, no hand-holding
- Explain complex topics when asked, but skip tutorials otherwise
- Answer-first — root cause at the top, supporting detail below
- Direct error handling — state the problem + next step, no apologies
- Cite sources always — knowledge file, tool output, or spec
- Never fabricate commands — tool output only
- When uncertain: say so. "I don't have data for this" beats a guess on silicon.

---

## 2. Repo Location and Hosting

- **Local path:** `c:\vs_projects\daiso`
- **Git hosting:** Intel GitHub Enterprise (github.intel.com)
- **Python minimum:** 3.10
- **License:** Intel internal

---

## 3. Directory Structure

Create exactly this:

```
daiso/
├── .github/
│   ├── copilot-instructions.md
│   └── CODEOWNERS
│
├── .vscode/
│   └── mcp.json
│
├── dtse-common/
│   ├── instructions.md
│   ├── skills/
│   │   ├── contribute/
│   │   │   └── SKILL.md
│   │   ├── discover/
│   │   │   └── SKILL.md
│   │   ├── search-specs/
│   │   │   └── SKILL.md
│   │   ├── setup/
│   │   │   └── SKILL.md
│   │   ├── glossary/
│   │   │   └── SKILL.md
│   │   ├── compare/
│   │   │   └── SKILL.md
│   │   ├── session-summary/
│   │   │   └── SKILL.md
│   │   ├── status-report/
│   │   │   └── SKILL.md
│   │   ├── vault-helper/
│   │   │   └── SKILL.md
│   │   └── explain-file/
│   │       └── SKILL.md
│   └── knowledge/
│       ├── guides/
│       │   └── .gitkeep
│       ├── reference/
│       │   └── .gitkeep
│       └── data/
│           └── glossary.toml
│
├── platform/
│   ├── README.md
│   ├── mcp-host/
│   │   ├── server.py
│   │   ├── registry.py
│   │   ├── common_tools.py
│   │   ├── config.py
│   │   └── requirements.txt
│   └── ci/
│       └── lint.yml
│
├── packs/
│   ├── README.md
│   ├── skills-catalog.md
│   │
│   ├── array/
│   │   ├── instructions.md
│   │   ├── skills/
│   │   │   ├── debug-workflow/
│   │   │   │   └── SKILL.md
│   │   │   ├── content-gen-workflow/
│   │   │   │   └── SKILL.md
│   │   │   ├── coverage-workflow/
│   │   │   │   └── SKILL.md
│   │   │   ├── deposit-workflow/
│   │   │   │   └── SKILL.md
│   │   │   ├── patspec-fix-workflow/
│   │   │   │   └── SKILL.md
│   │   │   ├── per-memory-pipeline/
│   │   │   │   └── SKILL.md
│   │   │   └── soft-algo-workflow/
│   │   │       └── SKILL.md
│   │   ├── products/
│   │   │   └── nvl/
│   │   │       ├── instructions.md
│   │   │       ├── config.toml
│   │   │       └── knowledge/
│   │   │           ├── guides/
│   │   │           ├── reference/
│   │   │           └── data/
│   │   │               ├── Algorithms.toml
│   │   │               ├── Algorithms.README.md
│   │   │               ├── Bisr.toml
│   │   │               └── Bisr.README.md
│   │   └── mcp/
│   │       ├── pack.toml
│   │       ├── tools.py
│   │       ├── tim_tools.py
│   │       ├── emu_analyzer.py
│   │       ├── emu_parser.py
│   │       ├── knowledge_engine.py
│   │       └── codesign.py
│   │
│   ├── scan/
│   │   ├── instructions.md
│   │   ├── skills/
│   │   │   └── .gitkeep
│   │   ├── products/
│   │   │   └── .gitkeep
│   │   └── mcp/
│   │       ├── pack.toml
│   │       └── config.toml
│   │
│   ├── functional/
│   │   ├── instructions.md
│   │   ├── skills/
│   │   │   └── .gitkeep
│   │   ├── products/
│   │   │   └── .gitkeep
│   │   └── mcp/
│   │       ├── pack.toml
│   │       └── config.toml
│   │
│   └── reset/
│       ├── instructions.md
│       ├── skills/
│       │   └── .gitkeep
│       ├── products/
│       │   └── .gitkeep
│       └── mcp/
│           ├── pack.toml
│           └── config.toml
│
├── templates/
│   ├── skill-template.md
│   ├── knowledge-guide-template.md
│   ├── knowledge-reference-template.md
│   ├── data-schema-template.md
│   └── pack-checklist.md
│
├── README.md
├── CONTRIBUTING.md
├── .gitignore
└── requirements.txt
```

---

## 4. README.md (repo root)

```markdown
# DAISO — DTSE AI Solution

One shared AI assistant platform for all DTSE teams.

## What is DAISO?

DAISO gives every DTSE engineer a domain-expert AI assistant in VS Code, powered by GitHub Copilot and connected to real tools via MCP.

- **One platform** — shared infrastructure, maintained centrally.
- **Team-owned packs** — each team owns its instructions, skills, knowledge, and tools.
- **Product-aware** — each pack supports multiple products (NVL, PTL, etc.) with product-specific config and knowledge.
- **Standard primitives** — learn once, contribute anywhere.

## Structure

| Folder | Purpose | Owner |
|--------|---------|-------|
| `dtse-common/` | Shared instructions, skills, knowledge | Platform team |
| `platform/` | MCP host, CI | Platform team |
| `packs/<team>/` | Team-specific content | Team champion |
| `packs/<team>/products/<product>/` | Product-specific config + knowledge | Team champion |
| `templates/` | Templates for contributors | Platform team |

## Quick Start

1. Ensure SSH to your VNC works (or use VS Code Remote-SSH on SLES 15).
2. Your platform team has a shared DAISO install on NFS.
3. Add to your `.vscode/mcp.json`:
   ```json
   {
     "servers": {
       "daiso": {
         "command": "ssh",
         "args": ["<you>@<your-vnc>", "python3", "/path/to/daiso/platform/mcp-host/server.py"],
         "transport": "stdio"
       }
     }
   }
   ```
   On SLES 15 (local mode), use the local command instead of SSH.
4. Create `~/.daiso.toml` on your VNC:
   ```toml
   work_area = "/nfs/site/disks/mfg_nvl_016/<your-idsid>/"
   team = "array"
   product = "nvl"
   ```
5. Open Copilot Chat. You're ready.

## Packs

| Pack | Domain | Champion | Status |
|------|--------|----------|--------|
| `array` | Array MBIST | Ahmad Maraaba | Active |
| `scan` | Scan / ATPG | TBD | Scaffold |
| `functional` | Functional test | TBD | Scaffold |
| `reset` | Reset & clock domains | TBD | Scaffold |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
```

---

## 5. platform/README.md

```markdown
# DAISO Platform

Infrastructure maintained by the platform team. Engineers and champions do not modify these files.

## Deployment Model

DAISO runs from a **single shared NFS location**. All engineers use the same install.

- One git clone on shared NFS (e.g. `/nfs/site/disks/mfg_nvl_016/daiso/`)
- `git pull` updates everyone — next Copilot session picks up changes
- Each engineer only configures their SSH target in `.vscode/mcp.json`
- Engineer identity auto-detected from SSH user + `~/.daiso.toml`

## MCP Host

The shared server (`mcp-host/server.py`) auto-discovers tools from pack `pack.toml` files. Tools are namespaced: `array/parse_emulation_run`, `scan/run_atpg_check`.

Generic tools (run_command, read_file, etc.) live in `common_tools.py` — available to all packs.

## Two Connection Modes

**SSH mode** (current):
```json
{
  "servers": {
    "daiso": {
      "command": "ssh",
      "args": ["<user>@<vnc>", "python3", "/nfs/.../server.py"],
      "transport": "stdio"
    }
  }
}
```

**Local mode** (after SLES 15 migration):
```json
{
  "servers": {
    "daiso": {
      "command": "python3",
      "args": ["/nfs/.../server.py"],
      "transport": "stdio"
    }
  }
}
```

## Updates

Platform team runs `git pull` on the shared NFS install. Everyone gets updates on next session.
```

---

## 6. .github/copilot-instructions.md

```markdown
# DAISO — GitHub Copilot Instructions

You are a DAISO-powered AI assistant for Intel DTSE engineers. You have deep domain expertise provided by team-specific content packs.

## How DAISO Works

- **Shared instructions** in `dtse-common/instructions.md` — always loaded.
- **Team packs** in `packs/<team>/` — each has instructions, skills, knowledge, MCP tools.
- **Product context** in `packs/<team>/products/<product>/` — product-specific rules, config, knowledge.
- **Skills** loaded on-demand when user intent matches the skill description.
- **Knowledge** pulled by skills or tools when needed.
- **MCP tools** execute real actions on the engineer's Linux environment.

## Active Packs

- `packs/array/` — Array MBIST
- `packs/scan/` — Scan / ATPG (scaffold)
- `packs/functional/` — Functional test (scaffold)
- `packs/reset/` — Reset & clock domains (scaffold)

## Instruction Loading Order

1. `dtse-common/instructions.md` (all teams, always)
2. `packs/<team>/instructions.md` (team rules, product-agnostic)
3. `packs/<team>/products/<product>/instructions.md` (product-specific rules)

## Common Skills (dtse-common)

contribute, discover, search-specs, setup, glossary, compare, session-summary, status-report, vault-helper, explain-file

## Session Start

1. Auto-detect the engineer from SSH user + ~/.daiso.toml
2. Greet: "Welcome <name>. Pack: <team>. Product: <product>."
3. Show what's new since last session (new skills/knowledge merged).

## Rules

1. Follow all three instruction layers.
2. When a skill matches user intent, load and follow it.
3. Never fabricate commands — always use MCP tools.
4. Cite sources when answering factual questions.
5. Answer-first — root cause at top, details below.
6. When uncertain, say so.
```

---

## 7. dtse-common/instructions.md

```markdown
# DAISO — Shared DTSE Instructions

These rules apply to ALL DTSE teams and all packs.

## Core Rules

- **ACT, DON'T DELEGATE** — use MCP tools for actions. Don't tell the user to do things the AI can do.
- **NEVER FABRICATE COMMANDS** — tool commands, vault commands, and infrastructure commands MUST come from MCP tool output. Wrong commands cause silent failures on production silicon.
- **ACTION BIAS** — when intent is clear but details are missing, pick a reasonable default and proceed.
- **STAY IN CONTEXT** — handle everything in one conversation. Never tell the user to switch tools or agents.
- **CITE SOURCES** — always reference the knowledge file or tool output that informed your answer. If nothing found: "NOT_FOUND: <what was searched>".
- **NEVER HALLUCINATE FACTS** — never use general knowledge for claims about Intel silicon or internal processes.
- **ANSWER FIRST** — lead with the root cause or answer. Put supporting detail below.
- **EXPLAIN WHEN ASKED** — skip tutorials by default. If the engineer asks "why?" or "explain", then go deeper.

## MCP Environment Constraints

The MCP server runs via SSH (or locally on SLES 15) on the engineer's VNC. It has NO sourced environment — no CAD tools, no project setup, no Intel modules.

### What MCP run_command CAN do

`cat`, `ls`, `find`, `grep`, `bzcat`, `head`, `tail`, `wc`, `diff`, `awk`, `sed`, `python3` (no Intel imports), read files, list directories, patch config files — anything that works on a bare Linux shell.

### What MCP run_command CANNOT do

- `source` any setup script
- `module load`
- `vaultmgr`, `vaultdeposit`
- `flash_search`, `flash_*`
- `itools`, `tessent`, `synopsys`
- Anything under `/p/pde/` needing project env vars

### Decision Rule

> Can it run with just `bash -c "command"` on a bare Linux box?
> - YES → use run_command
> - NO → give the user the exact command to copy-paste in their sourced terminal

**Note:** After SLES 15 migration, some of these constraints may relax. The VS Code terminal will be a real VNC shell capable of sourcing environments. Validate after migration.

### Writing Files via MCP

csh heredocs corrupt content. Use python3 base64 decode or write via Samba from Windows.

### Compressed Logs

`.bz2` files require `run_command("bzcat ... | tail -100")` — never read directly.

## Safety Rules

- NEVER modify files outside the team's designated workspace unless explicitly asked.
- NEVER run destructive commands without explicit user confirmation.

## Engineer Identity

The engineer's identity is auto-detected:
- IDSID from SSH user (`$USER`)
- Team, product, and work area from `~/.daiso.toml`

On first use, the `setup` skill creates this config interactively.
```

---

## 8. Pack Instructions

### packs/array/instructions.md (product-agnostic)

```markdown
# Array — Pack Instructions

You are a senior DFT engineer with deep expertise in Array MBIST (Memory Built-In Self-Test). Be precise, cite sources, challenge wrong assumptions. Skip tutorials.

## MBIST-Specific Rules

- ALWAYS ask about the algorithm (pmovi, marchc, galcol) — it determines test content.
- NEVER fabricate iTrace commands — always use `prepare_itrace_command` tool.

## MCP Tools (array namespace)

48 tools:

| Category | Tools |
|----------|-------|
| Emulation Debug | parse_emulation_run, query_emulation_run, recommend_fsdb_windows, generate_fsdb_overrides, prepare_fsdb_rerun, analyze_emulation_mismatches, analyze_sim_log |
| Vault 3.0 | vault_query, vault_query_command, vault_checkout_command, vault_modify_command, list_deposit_tests, filter_deposit_list |
| iTrace | prepare_itrace_command, register_itrace_run, check_itrace_status, read_itrace_results |
| Coverage | find_latest_coverage_xlsx, run_coverage_script, check_coverage_run, analyze_coverage_xlsx |
| Algorithm DB | lookup_algorithm, decode_test_name, suggest_algorithms, list_algorithm_categories, get_deposit_format |
| MBIST Engineering | query_array_info, query_parconfig, generate_multipass_disable_list, diagnose_mbist_failure, validate_toml_config, generate_test_name, generate_config_skeleton, explain_mbist_flow_step, collateral_generation_guide, mbist_checklist |
| NVL Per-Memory | parse_dft_summary, query_bp_mem_map, diff_patspec, generate_per_memory_patspec, generate_deposit_batch |
| Shell | run_command |
| Knowledge | glossary_lookup, query_data, list_tables |
| Co-Design | search_specs, search_hsd, list_codesign_sources |

## Test Name Format

`mb_<domain>_<config>__a_<cell_type>_<algo>_<addr>_<bg>[_suffix]`

## Signal Semantics

- `MBISTPG_EN=0` → controller OFF
- `MBISTPG_GO=0` → test FAILED (readback mismatch)
- `MBISTPG_DONE=0` → test still running
- `LV_TM` must be 0 during MBIST; `BIST_CLK` must toggle

## Vault Checkin Rules

- `-m "comment"` is MANDATORY on every checkin
- `-ci_source` path must be the full absolute path

## Product-Specific Content

Product rules, paths, configs, and knowledge are in `products/<product>/`. Load the product matching the engineer's `~/.daiso.toml`.
```

### packs/array/products/nvl/instructions.md

```markdown
# Array — NVL Product Instructions

NVL-specific rules, paths, and conventions.

## Vault Project

`nvlhub_axa0`

## Key NFS Paths

- dftSummary: `/nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/OFFICIAL_SCRIPTS/hub.dftSummary`
- Pattern Specs: `/nfs/site/disks/mfg_ptl_001/NVLAX/PATTERN_SPECS/<config>/<config>.pattern_spec`
- Deposit list: `/nfs/site/disks/mfg_ptl_001/NVLAX/deposit.list`

## Configuration Overlap Rule — CRITICAL

Full configs are supersets of sub-configs. NEVER mix a full config with its sub-configs.

- `media_ks` OR (`mediassa_ks` + `mediasmsag_ks` + ...) — never both
- `memss0_ks` OR (`memss0ssa_ks` + `memss0lsa_ks`) — never both
- `hbo_ks_pN` OR (`hbossa_ks_pN` + `hbolsa_ks_pN`) — never both
- `vpu_ks` + `vpualltle_ks` — complementary, POR needs BOTH

## Domains

media, chassis, display, hbo, memss, iax, vtu, ipu, mfs, vpu, fuse

## Commands Run by User Only

- Vault deposit: `echo 4 | /p/pde/tvpv/nvlhub/tracegen/tools/hvmtools/latest/bin/vaultdeposit -proj nvlhub_axa0 -turnin <TURNIN_FILE>`
- Any vaultmgr, flash_search, itools, tessent, module load

## Knowledge Map

| Topic | File |
|-------|------|
| Emulation debug | knowledge/guides/emulation_run_debug_guide.md |
| DONE=0 debug | knowledge/guides/emulation_mbist_done_timeout_debug.md |
| MBIST flow | knowledge/guides/mbist_flow_and_debug_handbook.md |
| PatternSpec | knowledge/guides/mint_spec_key_chapters.md |
| Per-memory gen | knowledge/guides/nvl_per_memory_patspec_generation.md |
| Test configs | knowledge/reference/nvl_test_configurations.md |
| Test plan | knowledge/reference/nvl_test_plan_reference.md |
| Clock domains | knowledge/reference/nvl_clock_domains.md |
| Power domains | knowledge/reference/nvl_power_domains.md |
| Signal semantics | knowledge/reference/signal-semantics-kb.md |
| Vault ops | knowledge/reference/vault-3.0-operations.md |
| Algorithms | knowledge/data/Algorithms.toml |
```

### Placeholder pack instructions (scan, functional, reset)

```markdown
# <Pack Name> — Pack Instructions

> Scaffold. Champion will fill in domain-specific content.

## To activate:

1. Assign a champion.
2. Write domain rules in this file.
3. Add skills — see `templates/skill-template.md`.
4. Create product folder: `products/<product>/`.
5. Implement MCP tools if needed.
6. See `packs/array/` as the reference.
```

---

## 9. MCP Server

### packs/array/mcp/pack.toml

```toml
[pack]
name = "array"
description = "Array MBIST tools"
champion = "Ahmad Maraaba"
namespace = "array"

[tools]
module = "tools"
extra_modules = ["tim_tools", "emu_analyzer"]
```

### packs/array/products/nvl/config.toml

```toml
[product]
name = "nvl"
vault_project = "nvlhub_axa0"

[paths]
dft_summary = "/nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/OFFICIAL_SCRIPTS/hub.dftSummary"
pattern_specs = "/nfs/site/disks/mfg_ptl_001/NVLAX/PATTERN_SPECS"
deposit_list = "/nfs/site/disks/mfg_ptl_001/NVLAX/deposit.list"
coverage_script = "/nfs/site/disks/mfg_nvl_016/amaraaba/scripts/nvl_mbist_coverage_status_steps_plists.py"
```

### Placeholder pack.toml (scan, functional, reset)

```toml
[pack]
name = "<team>"
description = "TBD"
champion = "TBD"
namespace = "<team>"

[tools]
module = ""
```

### platform/mcp-host/server.py

```python
#!/usr/bin/env python3
"""DAISO shared MCP server — loads tools from all packs.

Transport: stdio (via SSH or locally on SLES 15).
Usage: python3 platform/mcp-host/server.py
"""
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from registry import discover_packs, register_pack_tools
from common_tools import register_common_tools
from config import load_engineer_config

server = FastMCP("daiso")

engineer = load_engineer_config()
register_common_tools(server, engineer)

packs_dir = Path(__file__).parent.parent.parent / "packs"
for pack in discover_packs(packs_dir):
    register_pack_tools(server, pack, engineer)

if __name__ == "__main__":
    server.run(transport="stdio")
```

### platform/mcp-host/registry.py

```python
#!/usr/bin/env python3
"""Pack discovery and tool registration."""
import importlib, sys
from pathlib import Path
from dataclasses import dataclass
from typing import List
try:
    import tomllib
except ImportError:
    import tomli as tomllib

@dataclass
class PackInfo:
    name: str
    namespace: str
    description: str
    champion: str
    mcp_dir: Path
    module_name: str
    extra_modules: List[str]

def discover_packs(packs_dir: Path) -> List[PackInfo]:
    packs = []
    for pack_dir in sorted(packs_dir.iterdir()):
        toml_path = pack_dir / "mcp" / "pack.toml"
        if not toml_path.exists():
            continue
        with open(toml_path, "rb") as f:
            config = tomllib.load(f)
        pack_cfg = config.get("pack", {})
        tools_cfg = config.get("tools", {})
        module_name = tools_cfg.get("module", "")
        if not module_name:
            continue
        packs.append(PackInfo(
            name=pack_cfg.get("name", pack_dir.name),
            namespace=pack_cfg.get("namespace", pack_dir.name),
            description=pack_cfg.get("description", ""),
            champion=pack_cfg.get("champion", "TBD"),
            mcp_dir=pack_dir / "mcp",
            module_name=module_name,
            extra_modules=tools_cfg.get("extra_modules", []),
        ))
    return packs

def register_pack_tools(server, pack: PackInfo, engineer=None):
    mcp_dir_str = str(pack.mcp_dir)
    if mcp_dir_str not in sys.path:
        sys.path.insert(0, mcp_dir_str)
    for mod_name in [pack.module_name] + pack.extra_modules:
        try:
            importlib.import_module(mod_name)
        except ImportError as e:
            print(f"[DAISO] Warning: {mod_name} from {pack.name}: {e}", file=sys.stderr)
```

### platform/mcp-host/common_tools.py

```python
#!/usr/bin/env python3
"""Generic tools available to all packs."""
import subprocess, os

def register_common_tools(server, engineer):
    @server.tool()
    def run_command(command: str, timeout: int = 30) -> str:
        """Run a shell command on the VNC. Only bare Linux commands."""
        try:
            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True, text=True, timeout=timeout,
                cwd=engineer.get("work_area", os.path.expanduser("~"))
            )
            output = result.stdout
            if result.stderr:
                output += "\nSTDERR:\n" + result.stderr
            return output[:50000]
        except subprocess.TimeoutExpired:
            return f"Command timed out after {timeout}s"

    @server.tool()
    def read_file(path: str, start_line: int = 1, end_line: int = 200) -> str:
        """Read lines from a file on NFS."""
        with open(path) as f:
            lines = f.readlines()
        return "".join(lines[start_line - 1:end_line])

    @server.tool()
    def list_directory(path: str) -> str:
        """List directory contents on NFS."""
        return "\n".join(sorted(os.listdir(path)))
```

### platform/mcp-host/config.py

```python
#!/usr/bin/env python3
"""Load engineer config from ~/.daiso.toml."""
import os
from pathlib import Path
try:
    import tomllib
except ImportError:
    import tomli as tomllib

def load_engineer_config() -> dict:
    config_path = Path.home() / ".daiso.toml"
    defaults = {
        "user": os.environ.get("USER", "unknown"),
        "work_area": os.path.expanduser("~"),
        "team": "unknown",
        "product": "unknown",
    }
    if not config_path.exists():
        return defaults
    with open(config_path, "rb") as f:
        user_config = tomllib.load(f)
    defaults.update(user_config)
    defaults["user"] = os.environ.get("USER", "unknown")
    return defaults
```

### platform/mcp-host/requirements.txt

```
mcp>=1.0.0
tomli>=2.0.0;python_version<"3.11"
```

---

## 10. .vscode/mcp.json

```json
{
  "servers": {
    "daiso-ssh": {
      "command": "ssh",
      "args": [
        "<your-idsid>@<your-vnc-host>",
        "/usr/intel/pkgs/python3/3.11.9/bin/python3",
        "/nfs/site/disks/mfg_nvl_016/daiso/platform/mcp-host/server.py"
      ],
      "transport": "stdio"
    },
    "daiso-local": {
      "command": "/usr/intel/pkgs/python3/3.11.9/bin/python3",
      "args": ["/nfs/site/disks/mfg_nvl_016/daiso/platform/mcp-host/server.py"],
      "transport": "stdio",
      "disabled": true
    }
  }
}
```

---

## 11. .github/CODEOWNERS

```
/dtse-common/               @amaraaba
/platform/                   @amaraaba
/packs/array/                @amaraaba
/packs/scan/                 @scan-champion
/packs/functional/           @functional-champion
/packs/reset/                @reset-champion
/templates/                  @amaraaba
```

---

## 12. CI — platform/ci/lint.yml

```yaml
name: DAISO PR Checks
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate SKILL.md front-matter
        run: |
          find packs/ dtse-common/ -name "SKILL.md" | while read f; do
            head -1 "$f" | grep -q "^---" || { echo "FAIL: $f missing front-matter"; exit 1; }
          done
      - name: Validate pack.toml
        run: |
          pip install tomli
          python3 -c "
          import tomli, glob, sys
          for f in glob.glob('packs/*/mcp/pack.toml'):
              with open(f, 'rb') as fh: d = tomli.load(fh)
              if 'pack' not in d: print(f'FAIL: {f}'); sys.exit(1)
          print('All valid')
          "
      - name: No namespace collisions
        run: |
          python3 -c "
          import tomli, glob, sys
          ns = []
          for f in glob.glob('packs/*/mcp/pack.toml'):
              with open(f, 'rb') as fh: d = tomli.load(fh)
              n = d.get('pack',{}).get('namespace','')
              if n in ns: print(f'COLLISION: {n}'); sys.exit(1)
              if n: ns.append(n)
          print(f'{len(ns)} namespaces OK')
          "
```

---

## 13. Common Skills

Create each in `dtse-common/skills/<name>/SKILL.md`. Full content for all 10:

### contribute

```markdown
---
name: contribute
description: >
  Push new or modified skills, knowledge, or tools to the DAISO repo.
  Auto-detects changes, diffs against main, shows summary, pushes PR.
  Use when: push changes, contribute, save skill, commit, share changes.
tools: [daiso/*]
---

# Contribute Changes

## When to use
Engineer created or modified content during their session and wants to push it.

## Steps
1. Diff workspace against `main` branch — find modified/new files.
2. Show summary: "You modified X, created Y. Push as PR?"
3. If confirmed: create branch `<idsid>/<description>`, commit, push, open PR.
4. Report: "PR #N opened. Champion <name> will review."

## Key rules
- Never push without confirmation.
- Never push to main directly — always branch + PR.
- Engineer does not need git knowledge.
```

### discover

```markdown
---
name: discover
description: >
  List available skills, knowledge, and tools across all packs.
  Use when: what can you do, list skills, help, catalog, capabilities.
tools: [daiso/*]
---

# Discover Capabilities

## When to use
Engineer wants to know what DAISO can do.

## Steps
1. Read `packs/skills-catalog.md`.
2. Show: common skills + pack-specific skills for the engineer's team.
3. If asked about a specific skill, show its description and triggers.
```

### search-specs

```markdown
---
name: search-specs
description: >
  Search Intel architecture specs, HSD bugs, wikis via Co-Design.
  Use when: what does spec say, search spec, HSD, bug, architecture.
tools: [array/search_specs, array/search_hsd, array/list_codesign_sources]
---

# Search Specs & HSD

## When to use
Engineer asks about specs, known bugs, or wiki docs.

## Steps
1. Use `search_specs` for architecture docs.
2. Use `search_hsd` for known bugs.
3. Return with citations.
```

### setup

```markdown
---
name: setup
description: >
  Set up DAISO for a new engineer — SSH, MCP, ~/.daiso.toml.
  Use when: setup, onboard, new user, first time, configure, install.
tools: [daiso/*]
---

# Setup DAISO

## When to use
New engineer or reconfiguration needed.

## Steps
1. Check if ~/.daiso.toml exists.
2. If not, interview: work area? team? product? (auto-detect IDSID from $USER)
3. Create ~/.daiso.toml.
4. Verify MCP connection.
5. Confirm: "You're set up. Pack: <team>. Product: <product>."
```

### glossary

```markdown
---
name: glossary
description: >
  Explain DTSE terminology, acronyms, concepts.
  Use when: what is, define, explain term, acronym, glossary.
tools: [daiso/*]
---

# Glossary Lookup

## When to use
Engineer asks what a term means.

## Steps
1. Check `dtse-common/knowledge/data/glossary.toml`.
2. If found, return definition.
3. If not, check pack knowledge.
4. If still not found: "Not in glossary. You can add it."
```

### compare

```markdown
---
name: compare
description: >
  Diff two files — pattern specs, configs, knowledge files.
  Use when: diff, compare, difference, what changed, before after.
tools: [daiso/*]
---

# Compare Files

## When to use
Engineer wants to see differences between two files.

## Steps
1. Get two file paths.
2. Run diff via run_command.
3. Summarize meaningful differences.
```

### session-summary

```markdown
---
name: session-summary
description: >
  Recap current session — what was debugged, generated, changed.
  Use when: summarize, recap, what did we do, wrap up.
tools: [daiso/*]
---

# Session Summary

## When to use
Engineer wants a recap.

## Steps
1. Review conversation history.
2. Summarize: questions, tools called, files changed, findings.
3. List pending actions.
4. Remind about contribute skill if content was modified.
```

### status-report

```markdown
---
name: status-report
description: >
  Generate weekly/monthly progress report from session activity.
  Use when: status report, weekly report, progress, activity summary.
tools: [daiso/*]
---

# Status Report

## When to use
Engineer wants an activity summary over a period.

## Steps
1. Ask for time period.
2. Gather session summaries.
3. Organize by category.
4. Format as concise report.
```

### vault-helper

```markdown
---
name: vault-helper
description: >
  Guided vault operations — checkout, checkin, modify, query, deposit.
  Use when: vault, checkout, checkin, modify, deposit, TID, vaultmgr.
tools: [daiso/*]
---

# Vault Helper

## When to use
Engineer needs vault operation help.

## Steps
1. Determine operation.
2. Use MCP tool for query/checkout/modify.
3. For sourced-env commands (vaultmgr, vaultdeposit): generate exact command for user.

## Key rules
- `-m "comment"` MANDATORY on checkin.
- NEVER run vault commands via MCP.
```

### explain-file

```markdown
---
name: explain-file
description: >
  Explain any DFT file — pattern specs, STIL, SPF, TOML, logs.
  Use when: explain this file, what is this, parse, file format.
tools: [daiso/*]
---

# Explain File

## When to use
Engineer has a file and wants to understand it.

## Steps
1. Read the file.
2. Identify format.
3. Explain structure section by section.
4. Reference relevant knowledge.

## Key rules
- For .bz2, use bzcat.
- For large files, summarize first.
```

---

## 14. Skill Format Spec

All SKILL.md files must follow:

```markdown
---
name: <skill-name>
description: >
  <What it does.>
  Use when: <trigger phrases>.
tools: [<namespace>/*]
---

# <Title>

## When to use
<Scenario description.>

## Steps
1. ...

## Key references
- <Primary knowledge file> (explicit)
- Also search knowledge/ for related (hybrid)

## Key rules
- <Constraint>
```

**Rules:**
- Front-matter REQUIRED: `name`, `description`, `tools`
- `description` must include "Use when:" with specific trigger phrases
- `tools` uses wildcard: `[array/*]`, `[daiso/*]`
- Key references: list primary files + allow search (hybrid)

---

## 15. Knowledge Format Spec

### Markdown (guides + reference)

```markdown
---
title: "<Title>"
domain: <pack>
product: <product or "all">
author: <name>
date: YYYY-MM-DD
---
```

### Categories

- `guides/` — "How to do X"
- `reference/` — "What is X"
- `data/` — TOML + companion README

### TOML data

Each `.toml` needs a `.README.md` documenting fields, valid values, how to add entries.

---

## 16. Skills Catalog — packs/skills-catalog.md

```markdown
# DAISO Skills Catalog

## Common Skills (all teams)

| Skill | Triggers |
|-------|----------|
| contribute | push changes, save skill, commit |
| discover | what can you do, list skills, help |
| search-specs | search spec, HSD, architecture |
| setup | setup, onboard, first time |
| glossary | what is, define, acronym |
| compare | diff, compare, what changed |
| session-summary | summarize, recap, wrap up |
| status-report | weekly report, status, progress |
| vault-helper | vault, checkout, checkin, deposit |
| explain-file | explain this file, what is this |

## Array Pack

| Skill | Triggers |
|-------|----------|
| debug-workflow | error, fail, debug, GO=0, DONE=0 |
| content-gen-workflow | generate, create, deposit, itrace |
| coverage-workflow | coverage, status, what needs |
| deposit-workflow | deposit entry, deposit format |
| patspec-fix-workflow | patspec fix, dfx_agg, TID fix |
| per-memory-pipeline | per-memory, per-mem |
| soft-algo-workflow | soft algo, lvlib, hammer |

## Scan Pack
(None yet)

## Functional Pack
(None yet)

## Reset Pack
(None yet)
```

---

## 17. Contribution Workflow

**During session:** Engineer works normally. Copilot may create/modify files.

**Push (on-demand or session end):**
1. Engineer says "push my changes" OR Copilot detects modifications.
2. Copilot diffs workspace vs main, shows summary.
3. If confirmed: branch → commit → push → PR.
4. Champion reviews → merges.
5. `git pull` on shared NFS → everyone gets updates.

**Engineer never runs git commands.** The `contribute` skill handles it.

**Merge rights:** Champion only per pack. Platform team for dtse-common/ and platform/.

---

## 18. Templates

### templates/skill-template.md

```markdown
---
name: <skill-name>
description: >
  <What it does.>
  Use when: <triggers>.
tools: [<namespace>/*]
---

# <Title>

## When to use
<Scenario.>

## Steps
1. ...

## Key references
- <file>

## Key rules
- <rule>
```

### templates/knowledge-guide-template.md

```markdown
---
title: "<How to do X>"
domain: <pack>
product: <product or "all">
author: <name>
date: YYYY-MM-DD
---

# <Title>

## Context
<When/why needed.>

## Steps
1. ...

## Common mistakes
- ...
```

### templates/knowledge-reference-template.md

```markdown
---
title: "<What is X>"
domain: <pack>
product: <product or "all">
author: <name>
date: YYYY-MM-DD
---

# <Title>

## Definition
<Concise definition.>

## Details
<Technical details.>
```

### templates/data-schema-template.md

```markdown
# <File> — Schema

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ... | ... | ... | ... |

## Adding an entry

1. Add `[entry]` section to the .toml.
2. Fill required fields.
3. PR → review.
```

### templates/pack-checklist.md

```markdown
# New Pack Checklist

- [ ] Create `packs/<team>/`
- [ ] Write `instructions.md`
- [ ] Create `mcp/pack.toml`
- [ ] Create `products/<product>/` with config.toml + knowledge/
- [ ] Add at least one skill
- [ ] Add at least one knowledge file
- [ ] Assign champion
- [ ] Update skills-catalog.md
- [ ] Open PR
```

---

## 19. CONTRIBUTING.md

```markdown
# Contributing to DAISO

## Who
Any DTSE engineer. No git knowledge required.

## What

| I want to... | Where |
|--------------|-------|
| Share a workflow | `packs/<team>/skills/<name>/SKILL.md` |
| Document knowledge | `packs/<team>/products/<product>/knowledge/guides/` or `reference/` |
| Add structured data | `packs/<team>/products/<product>/knowledge/data/` (TOML + README) |
| Build a tool | `packs/<team>/mcp/` |

## How

**Recommended:** Work with Copilot, then say "push my changes." DAISO handles git.

**Manual:** Branch → edit → PR → champion review.

## Standards

- Skills: YAML front-matter (`name`, `description`, `tools`), "When to use", "Steps", "Key rules"
- Knowledge: YAML front-matter (`title`, `domain`, `product`, `author`, `date`)
- Data: TOML + companion README

## Review

- Pack content → champion
- Shared content → platform team
```

---

## 20. .gitignore

```
__pycache__/
*.pyc
*.pyo
.env
*.egg-info/
dist/
build/
.vscode/settings.json
*.xlsx
*.pptx
```

---

## 21. requirements.txt

```
mcp>=1.0.0
tomli>=2.0.0;python_version<"3.11"
```

---

## 22. dtse-common/knowledge/data/glossary.toml

```toml
[MBIST]
term = "Memory Built-In Self-Test"
definition = "On-chip test logic that tests embedded memories."

[ATPG]
term = "Automatic Test Pattern Generation"
definition = "Algorithmic generation of test vectors to detect faults."

[DFT]
term = "Design for Test"
definition = "Design techniques that make a chip testable."

[MCP]
term = "Model Context Protocol"
definition = "Protocol connecting AI assistants to external tools."

[NFS]
term = "Network File System"
definition = "Distributed file system for shared storage."

[VNC]
term = "Virtual Network Computing"
definition = "Remote Linux desktop session for CAD work."

[IDSID]
term = "Intel Design System ID"
definition = "Engineer's unique identifier across Intel systems."

[iTrace]
term = "Intel Trace"
definition = "Emulation infrastructure for running DFT test content."

[STIL]
term = "Standard Test Interface Language"
definition = "IEEE 1450 format for test patterns."
```

---

## 23. Content to Port from dftcopilot-vscode

Copy from `c:\vs_projects\dftcopilot-vscode`. Do NOT modify during porting.

### Skills (7)

| Source | Destination |
|--------|-------------|
| `.github/skills/debug-workflow/SKILL.md` | `packs/array/skills/debug-workflow/SKILL.md` |
| `.github/skills/content-gen-workflow/SKILL.md` | `packs/array/skills/content-gen-workflow/SKILL.md` |
| `.github/skills/coverage-workflow/SKILL.md` | `packs/array/skills/coverage-workflow/SKILL.md` |
| `.github/skills/deposit-workflow/SKILL.md` | `packs/array/skills/deposit-workflow/SKILL.md` |
| `.github/skills/patspec-fix-workflow/SKILL.md` | `packs/array/skills/patspec-fix-workflow/SKILL.md` |
| `.github/skills/per-memory-pipeline/SKILL.md` | `packs/array/skills/per-memory-pipeline/SKILL.md` |
| `.github/skills/soft-algo-workflow/SKILL.md` | `packs/array/skills/soft-algo-workflow/SKILL.md` |

### Knowledge — NVL guides

| Source | Destination |
|--------|-------------|
| `knowledge/tribal/emulation_run_debug_guide.md` | `packs/array/products/nvl/knowledge/guides/emulation_run_debug_guide.md` |
| `knowledge/tribal/emulation_mbist_done_timeout_debug.md` | `packs/array/products/nvl/knowledge/guides/emulation_mbist_done_timeout_debug.md` |
| `knowledge/tribal/mbist_flow_and_debug_handbook.md` | `packs/array/products/nvl/knowledge/guides/mbist_flow_and_debug_handbook.md` |
| `knowledge/tribal/mint_spec_key_chapters.md` | `packs/array/products/nvl/knowledge/guides/mint_spec_key_chapters.md` |
| `knowledge/tribal/nvl_per_memory_patspec_generation.md` | `packs/array/products/nvl/knowledge/guides/nvl_per_memory_patspec_generation.md` |
| `knowledge/tribal/min_freq_bist_clock_override.md` | `packs/array/products/nvl/knowledge/guides/min_freq_bist_clock_override.md` |
| `knowledge/tribal/nvl_pdl_procedures.md` | `packs/array/products/nvl/knowledge/guides/nvl_pdl_procedures.md` |

### Knowledge — NVL reference

| Source | Destination |
|--------|-------------|
| `knowledge/tribal/soft_algo_reference.md` | `packs/array/products/nvl/knowledge/reference/soft_algo_reference.md` |
| `knowledge/tribal/nvl_test_configurations.md` | `packs/array/products/nvl/knowledge/reference/nvl_test_configurations.md` |
| `knowledge/tribal/nvl_test_plan_reference.md` | `packs/array/products/nvl/knowledge/reference/nvl_test_plan_reference.md` |
| `knowledge/tribal/nvl_clock_domains.md` | `packs/array/products/nvl/knowledge/reference/nvl_clock_domains.md` |
| `knowledge/tribal/nvl_power_domains.md` | `packs/array/products/nvl/knowledge/reference/nvl_power_domains.md` |
| `knowledge/tribal/nvl_pmux_and_retention.md` | `packs/array/products/nvl/knowledge/reference/nvl_pmux_and_retention.md` |
| `knowledge/tribal/nvl_reset_sequence.md` | `packs/array/products/nvl/knowledge/reference/nvl_reset_sequence.md` |
| `knowledge/tribal/nvl_emulation_paths.md` | `packs/array/products/nvl/knowledge/reference/nvl_emulation_paths.md` |
| `knowledge/tribal/nvl-array-mbist-master-reference.md` | `packs/array/products/nvl/knowledge/reference/nvl-array-mbist-master-reference.md` |
| `knowledge/tribal/vault-3.0-operations.md` | `packs/array/products/nvl/knowledge/reference/vault-3.0-operations.md` |
| `knowledge/tribal/Vault-Deposit-Format.md` | `packs/array/products/nvl/knowledge/reference/Vault-Deposit-Format.md` |
| `knowledge/tribal/stil-test-structure.md` | `packs/array/products/nvl/knowledge/reference/stil-test-structure.md` |
| `knowledge/tribal/spf_structure_reference.md` | `packs/array/products/nvl/knowledge/reference/spf_structure_reference.md` |
| `knowledge/tribal/pattern_spec_validation_rules.md` | `packs/array/products/nvl/knowledge/reference/pattern_spec_validation_rules.md` |
| `knowledge/tribal/tessent_mbist_introduction.md` | `packs/array/products/nvl/knowledge/reference/tessent_mbist_introduction.md` |
| `knowledge/tribal/tessent_mbist_user_guide_key_chapters.md` | `packs/array/products/nvl/knowledge/reference/tessent_mbist_user_guide_key_chapters.md` |
| `knowledge/reference/common_errors.md` | `packs/array/products/nvl/knowledge/reference/common_errors.md` |
| `knowledge/reference/MBIST-Algorithm-Reference.md` | `packs/array/products/nvl/knowledge/reference/MBIST-Algorithm-Reference.md` |
| `knowledge/reference/MBIST-Test-Naming-Convention.md` | `packs/array/products/nvl/knowledge/reference/MBIST-Test-Naming-Convention.md` |
| `knowledge/reference/MBIST-Modification-Types.md` | `packs/array/products/nvl/knowledge/reference/MBIST-Modification-Types.md` |
| `knowledge/reference/signal-semantics-kb.md` | `packs/array/products/nvl/knowledge/reference/signal-semantics-kb.md` |
| `knowledge/reference/emulation-run-log-structure.md` | `packs/array/products/nvl/knowledge/reference/emulation-run-log-structure.md` |
| `knowledge/reference/remediation-playbook.md` | `packs/array/products/nvl/knowledge/reference/remediation-playbook.md` |

### Collateral data

| Source | Destination |
|--------|-------------|
| `collateral/Algorithms.toml` | `packs/array/products/nvl/knowledge/data/Algorithms.toml` |
| `collateral/Bisr.toml` | `packs/array/products/nvl/knowledge/data/Bisr.toml` |

### MCP tools

| Source | Destination |
|--------|-------------|
| `tools.py` | `packs/array/mcp/tools.py` |
| `tim_tools.py` | `packs/array/mcp/tim_tools.py` |
| `emu_analyzer.py` | `packs/array/mcp/emu_analyzer.py` |
| `emu_parser.py` | `packs/array/mcp/emu_parser.py` |
| `knowledge_engine.py` | `packs/array/mcp/knowledge_engine.py` |
| `codesign.py` | `packs/array/mcp/codesign.py` |

NOTE: Fix import paths after porting.

---

## 24. What NOT to Port

- `ai.py`, `chat.py`, `ui.py` — old chat interface
- `build_presentation*.py` — presentation scripts
- `nvl_mbist_coverage_status_steps_plists.py` — stays on NFS
- `workflows/`, `workflow_loader.py` — old workflow engine
- `rag/` — old RAG system
- `sample_data/`, `emu_logs/` — test data
- `agents/` — old agent system
- `docs/`, `project_docs/` — DFT Copilot docs

---

## 25. After Scaffolding

1. `git init`
2. Verify structure matches §3.
3. Copy content per §23.
4. Fix import paths in ported Python.
5. Report what was created and what needs attention.
