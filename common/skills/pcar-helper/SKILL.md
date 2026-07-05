---
name: pcar-helper
description: >
  Guided PCAR3 / Flash Plist Builder operations — author plist configs,
  build plists, debug missing patterns, configure resetplb/segmented resets,
  release plists via ci_plist.
  Use when: plist, pcar, pcar3, plist_builder_pcar3, ResetPlb, PlistFile,
  Plb, segmented_resets, preburstplist, flash plist builder, vcf -p3,
  ci_plist, generate plist, missing patterns in plist, fix_needed plist,
  resetplb naming.
tools: [daiso/*]
---

# PCAR3 Helper

## When to use
Engineer needs help with any plist-generation task: writing a `.pcar3` config, running VCF on it, debugging missing patterns / `fix_needed_*.plist`, configuring resetplb / segmented resets, releasing plists with `ci_plist`, or migrating from PCAR2.

## Important
- **Don't hand-edit `.plist` files.** Always go through PCAR3. If a hand-edited plist needs diagnosis, use `plist_origin_tracking.py --plist <plist>`.
- **PCAR3 needs the tracegen env sourced** (it calls Vault + Linus directly). Source the product's tracegen setup before `vcf.py -p3 …`.
- **Run from a working drive.** Windows convention: `\\sc8-samba.sc.intel.com\nfs\site\disks\…` for SC, `\\pdx-samba…` for PDX.
- **`segmented_resets=True` is mandatory for NVL / PTL / LNL / LNS / MTL.** Missing it produces wrong PreBurst block names.
- **Never run `vcf.py -p3` or `ci_plist.py` for the engineer.** Show the command and ask them to run it in their sourced terminal.

## Operations

### Author — "write a PCAR3 config"

**What the engineer says:** "write a pcar3 config", "I need a plist for module Mxxx", "give me a starter pcar3 file"

1. Ask (only if not specified):
   - Output plist filename (e.g. `cpu28_main.plist`)
   - Product (NVL / PTL / LNS / MTL / …) — drives whether `segmented_resets=True` is required
   - TIDs or tuples to include
   - Reset behavior — default resetplb, custom altname, or `preburstplist=None`?
2. Generate the config from this skeleton:

   ```python
   #!/usr/bin/env python3
   from veplib.plist_builder_pcar3 import PlistFile, Plb, Pats, Tids, pcar3, ResetPlb

   pcar3.set_option(segmented_resets=True)   # mandatory for NVL/PTL/LNS/MTL/LNL

   level0 = PlistFile('<plist_filename>.plist')

   level1 = level0.add(Plb('<block_name>'))
   level1.add(Pats(Tids(['<tid>']), trctag="<LI_or_trctag>"))
   level1.add(ResetPlb())

   if __name__ == '__main__':
       pcar3.process()
       print(pcar3.report(detail=True))
       print(pcar3.gen_plist_preview())
   ```

3. Tailor the template:
   - **Default reset auto-attached:** `Plb('main_block')` with `segmented_resets=True` will get `PreBurstPList` automatically.
   - **Custom altname:** `Plb('test', preburstplist=ResetPlb(alt='dlvr_fc'))`
   - **Specific ratio:** `Plb('x', preburstplist=ResetPlb(alt='mdrv', ratio='dft_fabric_ratio=5'))`
   - **Disable preburst:** `Plb('y', preburstplist=None)`
   - **Reset PLB block:** `Plb('_RESET_1', ratiopre='dft_fabric_ratio=5')` (auto-builds resetplb name)
   - **Multi-bomgroup:** one `.pcar3` per bomgroup, files named `<base>_<bomgroup>.plist` (universal = `<base>_allplist.plist`).

4. Cite the relevant section of [pcar3-tools-documentation.md](../../packs/example-domain-a/products/nvl/knowledge/reference/pcar3-tools-documentation.md) for what was used.

### Build — "generate the plist from this config"

**What the engineer says:** "build the plist", "run pcar3", "vcf this config"

1. Ask for product-specific args from the engineer (or DRV team): `vrev`, `vectype`, `mode`.
2. Build the command:

   ```
   vcf.py -p3 <file.pcar3> -vrev <vrev> -vectype <hvm|sdr> -mode <sort|hdmt2sort|...>
   ```

3. Show it to the engineer:
   > Run this from the directory containing the `.pcar3` (working drive — Samba, not local C:):
   > ```
   > vcf.py -p3 cpu28_main.pcar3 -vrev vrevGMDA5P -vectype hvm -mode sort
   > ```
4. Tell them to inspect output: `<rundir>/pcar3/*.plist`.
5. If they want a **preview without running VCF**, suggest running the `.pcar3` directly: `python <file.pcar3>` — `pcar3.gen_plist_preview()` prints the structure without resolving patterns.

### Debug — "patterns are missing" / "I got `fix_needed_*.plist`"

**What the engineer says:** "the plist is named fix_needed_…", "patterns are commented out", "missing tuples", "wrong PreBurst name"

Walk the standard checklist:

1. **`fix_needed_<>.plist` rename** → `localrefplist_check=True` and a referenced PLB is not in the same plist.
   - Ask: which `RefPlb(...)` reference is unresolved?
   - Fix: add the missing block, or remove/correct the `RefPlb`. Names starting with `resetplb`/`postplb` are skipped by the check.

2. **Missing patterns appear as commented lines** → `show_missing=True` (default). Tuple exists but pattern not built.
   - Verify the tuple is in Flash (`flash_search`).
   - Verify the pattern is built for the right `vrev` / `vectype` / `mode` — these must match the VCF call.

3. **Wrong PreBurst block name** → `segmented_resets=False` on a product that requires segmented resets.
   - Add `pcar3.set_option(segmented_resets=True)` at the top of the config.
   - To suppress per-block: `Plb('x', preburstplist=None)`.

4. **`get_resetplb()` returns wrong name** → ratio/altname/module mismatch with product config.
   - Have the engineer print `pcar3.get_resetplb(patname, ratio=[…], altname='…')` and compare to the product's resetplb naming convention:
     `resetplb_<dft_fabric_ratio>_<reset_pair>_<vrev>_<mode>_<vectype>_list[_<altname>]`

5. **Tracegen errors** ("can't find Linus / Vault") → tracegen env not sourced. Have them source the product tracegen setup before running.

6. **`serev` mismatch** (PCAR2 only) → use `-serev skip`. Not a problem in PCAR3.

### Segmented-reset routing — "which resets does this trace need?"

**What the engineer says:** "find segmented resets", "all_segmented_reset_flow", "reset_pair / precat_pair / midcat_pair"

> These APIs are **Flash Plist Builder only** — the modern flow on NVL/PTL/LNS.

Show the engineer this snippet adapted to their trace name:

```python
trc = '<full_trace_name>'

print(pcar3.all_segmented_reset_flow(trc))
print(pcar3.find_segmented_reset_from_manual(trc))
print(pcar3.find_segmented_reset_from_direct(trc))
print(pcar3.find_segmented_reset_from_ip(trc, method="reset_pair"))
print(pcar3.find_segmented_reset_from_ip(trc, method="precat_pair"))
print(pcar3.find_segmented_reset_from_ip(trc, method="midcat_pair"))
print(pcar3.get_resetplb(trc))
```

Optional `name_filter` dict (e.g. `{"matchmode_cpu": "x"}`) narrows results.

### Release — "check in the plist"

**What the engineer says:** "release the plist", "ci_plist", "checkin to I drive"

1. Ask:
   - Module (e.g. `Mtpi`, `Marr`, …)
   - Revision (e.g. `RevTTA0.0p11`)
   - Comment (mandatory)
   - Lock? (released patches usually `-lock`, pre-si patches do not)
2. Build the command:

   ```
   ci_plist.py -module <Mxxx> -rev <Rev...> -comment "<msg>" [-lock]
   ```

3. Show it to the engineer with a confirmation note:
   > This stages the plist + patterns to the I:\ drive (eng/prod folders). Folder structure must match the DRV folder naming.

### Migrate — "convert PCAR2 to PCAR3"

**What the engineer says:** "convert this .pcar to pcar3", "migrate from pcar2"

1. Read the legacy `.pcar` text DSL.
2. Map the structure 1:1:
   - `<plist>` block → `level1 = level0.add(Plb('<name>'))`
   - tuple references → `Pats('<tuple>')` or `Pats(Tids([...]))`
   - `<catg>` multi-bomgroup line → multiple `PlistFile` instances, one per bomgroup
3. Replace ambles with `ResetPlb(...)` (modern products do this; check with DRV).
4. Add `pcar3.set_option(segmented_resets=True)` if the product requires it.
5. Wrap with the standard `if __name__ == '__main__': pcar3.process(); pcar3.report(detail=True); pcar3.gen_plist_preview()`.
6. Run preview locally: `python <file.pcar3>` — diff the preview against the original PCAR2 plist before going to VCF.

## Quick reference — the knobs that bite

| Option | Default | Set to True when |
|---|---|---|
| `segmented_resets` | False | Product is NVL / PTL / LNL / LNS / MTL |
| `localrefplist_check` | False | You want hard validation of `RefPlb` references |
| `show_missing` | True | (Leave on) — see missing patterns commented in output |
| `comment_end_bracket` | True | (Leave on) — output readability |
| `preamble_tuple` | False | Admin-set per product (FAQ#3 admin page) |
| `ratioagnostic_midpst` | False | Product `pattern.py` supports it |

## Quick reference — when to use which API

| Goal | API |
|---|---|
| Resolve resetplb name from a pattern | `pcar3.get_resetplb(patname, ratio=, altname=, module=)` |
| All segmented resets per `reset_flow` | `pcar3.all_segmented_reset_flow(patname)` |
| Segmented reset from IP | `pcar3.find_segmented_reset_from_ip(patname, method=…)` (`reset_pair` / `precat_pair` / `midcat_pair`) |
| Segmented reset from manual | `pcar3.find_segmented_reset_from_manual(patname)` |
| Segmented reset from direct | `pcar3.find_segmented_reset_from_direct(patname)` |
| Total chunk count | `pcar3.get_totalchunknum(tid=…, tup=…)` |
| Raw Linus / Vault / Finder dicts | `get_linus_dict()` / `get_vault_dict()` / `get_finder_dict()` |
| Preview plist without VCF | `pcar3.gen_plist_preview()` |

## Common mistakes to catch

1. **Missing `pcar3.set_option(segmented_resets=True)`** on NVL/PTL/LNS/MTL → wrong PreBurst block names.
2. **Hand-editing the generated `.plist`** → unsupported. Use PCAR3; diagnose with `plist_origin_tracking.py`.
3. **Running PCAR3 without tracegen env** → Vault/Linus calls fail silently or with cryptic import errors.
4. **Wrong `vrev` / `vectype` / `mode`** → patterns appear "missing" because they were built for a different combination.
5. **Mixing PCAR2 and PCAR3 invocations** → `vcf -list <tuplefile>` is PCAR2; `vcf.py -p3 <file>` is PCAR3. Pick one per product.
6. **Multi-bomgroup with bad filename suffix** → TPIE expects `*_allplist.plist` (universal) and `*_<bomgroup>.plist` (specific). `*_debug.plist` is debug only.
7. **`ci_plist` without comment** — always require `-comment "<msg>"`.
8. **Releasing pre-si plists with `-lock`** — only lock released-patch revisions.

## Key references

- [pcar3-tools-documentation.md](../../packs/example-domain-a/products/nvl/knowledge/reference/pcar3-tools-documentation.md) — full doc (objects, knobs, methods, examples, per-product notes, references).
- Companion pipeline tools: [vault-tools-documentation.md](../../packs/example-domain-a/products/nvl/knowledge/reference/vault-tools-documentation.md) (test source) · [itrace-tools-documentation.md](../../packs/example-domain-a/products/nvl/knowledge/reference/itrace-tools-documentation.md) (run / tracegen) · [flash-tools-documentation.md](../../packs/example-domain-a/products/nvl/knowledge/reference/flash-tools-documentation.md) (tuple / pattern DB).
- TVPV wikis: PCAR3 full reference (1207039914) · PCAR3 Examples (1404112654) · PCAR3 language (1202652087). LNS plist generation (HTD/2633412456). PTL PCD plist gen (HTD/3064541596).

## Key rules

- Don't run VCF or `ci_plist` for the engineer — show the command, let them run it in their sourced terminal.
- Don't hand-edit plists.
- Always set `segmented_resets=True` on NVL / PTL / LNL / LNS / MTL.
- Always require a `-comment` on `ci_plist`.
- Always cite the source (doc section or wiki link) when you give an answer beyond the template.
