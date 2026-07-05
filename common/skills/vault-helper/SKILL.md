---
name: vault-helper
description: >
  Guided vault operations — query, checkout, checkin, modify, deposit.
  Use when: vault, checkout, checkin, modify, deposit, TID, vaultmgr,
  vaultdeposit, query vault, find TID, obsolete, vault status.
tools: [daiso/*]
---

# Vault Helper

## When to use
Engineer needs help with any vault operation: finding records, checking out source, checking in changes, depositing new tests, or modifying records.

## Important
- **NEVER execute vault-modify commands directly.** Always show the command and ask for confirmation.
- **`-m "comment"` is MANDATORY on every checkin.** Reject checkin requests without a comment.
- **Vault commands require a sourced environment** (HVM tools). Generate the command for the engineer to paste in their sourced terminal, or use pack tools that build the command string.

## Operations

### Query — "find a vault record"

**What the engineer says:** "find TID 207413", "search vault for pmovi", "what's in vault for media_ks"

1. Determine what they're looking for:
   - **By TID**: use the pack's `vault_query` or `vault_query_command` tool with `tid=<TID>`
   - **By pattern**: use `query_field="path"` + `query_value="<pattern>"`
   - **By intent**: use `query_field="intent"` + `query_value="<value>"`
2. Show results in a readable table (TID, test name, status, owner).
3. If too many results, help narrow the filter.

### Checkout — "get the source for TID X"

**What the engineer says:** "checkout TID 207413", "get the patspec for this test"

1. Build the command directly from the pack's vault project and tool path:
   ```
   mkdir -p output/<TID>_<project>/ && vaultmgr -proj <project> -q test_id = <TID> -- -pr all -- -co_source output/<TID>_<project>/
   ```
2. Show it to the engineer:
   > Run this in your sourced terminal:
   > ```
   > mkdir -p output/207413_nvlhub/ && vaultmgr -proj nvlhub_axa0 -q test_id = 207413 -- -pr all -- -co_source output/207413_nvlhub/
   > ```
3. Explain the directory structure: files nest as `<dir>/<TID>/<TID>/<name>.pattern_spec`.
4. After checkout, offer to read/explain the pattern spec.

### Checkin — "push my changes back"

**What the engineer says:** "checkin TID 207413", "save my patspec changes to vault"

1. **Require a comment.** If not provided, ask: "What did you change? (this becomes the vault comment)"
2. Build the command directly:
   ```
   vaultmgr -proj <project> -q test_id = <TID> -- -pr all -- -ci_source <path> -m "<comment>"
   ```
3. **CRITICAL:** The `ci_source` path must be the FULL path to the innermost directory containing the `.pattern_spec` file. Warn the engineer:
   > The ci_source path must point to the innermost `<TID>/` directory, e.g.:
   > `/path/output/207413_nvlhub/207413/207413/`
4. Show the command for confirmation before execution.

### Modify — "obsolete TID X" / "update a field"

**What the engineer says:** "obsolete TID 207413", "update the tag", "add notes to this TID"

1. Build the command directly based on action:
   - **Obsolete:** `vaultmgr -proj <project> -q test_id = <TID> -- -pr all -- -r status obsolete -r- --`
   - **Update field:** `vaultmgr -proj <project> -q test_id = <TID> -- -pr all -- -r <field> <value> -r- --`
   - **Add notes:** `vaultmgr -proj <project> -q test_id = <TID> -- -pr all -- -a notes "<text>" --`
2. **Always confirm before execution** — these modify vault state.

### Deposit — "add a new test to vault"

**What the engineer says:** "deposit this test", "create a vault entry", "I need a turnin file"

This is the most complex operation. Defer to the pack's deposit workflow skill if one exists (e.g. array has `deposit-workflow`). If no pack-specific skill:

1. **Gather required info:**
   - Test name (or enough to generate one)
   - Pattern spec path
   - Project (e.g. `nvlhub_axa0`, `ptl_a0`)
   - Turnin list path
2. **Generate the deposit command:**
   ```
   echo 4 | <vaultdeposit_bin> -proj <project> -turnin <turnin_list>
   ```
   The `echo 4` selects "deposit" from the interactive menu.
3. **Config isolation rule:** The config file must be alone in its own directory — vault deposit uploads the entire folder.
4. Show the command and let the engineer run it in their sourced terminal.
5. After deposit, verify with a vault query for the new TID.

## Pack-specific defaults

Each pack defines its own vault project, tool paths, and test naming conventions:
- **Array**: project `nvlhub_axa0`, tools at `/p/pde/tvpv/nvlhub/tracegen/tools/hvmtools/latest/bin/`
- **Other packs**: check `packs/<domain>/products/<product>/config.toml` for vault project and paths

When a pack has tools like `vault_query`, `vault_query_command`, `vault_checkout_command`, `vault_modify_command` — use them. They handle project defaults and command formatting.

## Common mistakes to catch

1. **Checkin without comment** — vault rejects it silently. Always enforce `-m`.
2. **Wrong ci_source path** — must be the innermost directory, not the checkout root.
3. **Depositing with other files in the config directory** — vault uploads everything.
4. **Querying with too-broad filters** — help narrow: by algorithm, config, or cell type.
5. **Forgetting to verify after deposit** — always query vault to confirm the TID was created.
