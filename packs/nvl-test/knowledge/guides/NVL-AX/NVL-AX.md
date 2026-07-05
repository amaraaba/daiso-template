---
title: NVL-AX
source: Word Document
section: NVL-AX
imported: 2026-07-05T11:57:21.167380
---

1:1
Wednesday, 15 April 2026
14:53

Passing with new model, we have a problem in memsss
Coverage script shows a lot of missing, met with Uri yesterday and we closed all the gaps for special content
We need to close the gaps that Hadas left
Running simulation, there were gaps in Hadas run
Tool now is cabaple of doing many things
We have a billing issue that CDG is not part of expertgpt


References and Links
Sunday, 7 September 2025
15:03

HVM SPEC FOR ARRAY CONTENT:
MOW Requirements

2025_AEWG_NVL_array_presil_review


https://intel.sharepoint.com/sites/server/SPRPSM/_layouts/15/Doc.aspx?sourcedoc={6949faf6-ab6b-404e-976f-9c6d0b15de6e}&action=edit&wd=target%28MBIST.one%7C779a3a05-622d-4ceb-bae5-63db0fd6ffc3%2FContacts%7Cb4c87e1c-6a3b-46d7-8712-aa22ba5f2f2b%2F%29&wdorigin=NavigationUrl

\\sc8-samba.sc.intel.com\nfs\site\disks\mfg_nvl_016\amaraaba\nvlhub_axa0\summaries\script

/nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/OFFICIAL_SCRIPTS/
/nfs/site/disks/mfg_nvl_016/yfriedgu/run_area/summary_paths.list

NVL-S:


General
Thursday, 14 August 2025
17:24

NVL disk:
/nfs/site/disks/mfg_nvl_016/amaraaba

From Noya:
Disk:
/nfs/site/disks/amaraaba_wa01/nvl_ax_a0/

Simless Source:
source /nfs/site/disks/nzonis_wa01/nvlhub_ax/nvlhub_ax_ww35/mfg/sourceme -p nvlhub -s axa0
Emu Source:
source /nfs/site/disks/nzonis_wa01/nvlhub_ax/nvlhub_ax_ww35/mfg/sourceme -p nvlhub -s axa0  -m cu_emu













Source:
source /p/hdk/pu_tu/prd/cth_infra/latest/setCTH -m hub -s nvlax-a0 -b master

SC11 :
flash_search --prod NVLHUB trc --search_mode tuple --tuple 39750

/p/pde/tvpv/nvlhub/traces/a0/0046143/0039750/g0039750H0046143H_00_A0Maa00_XXXXXXXXX0000_HXXXxA00E0Pm0500xx_F8g044fgOgfc4mxxxxx_hub_hbo_ks_p0_xsa_pmovi_x_s.stil.bz2

/nfs/site/proj/nvlax/nvlax.models.09/hub/hub-nvlax-a0-master-25ww29a/src/codegen/hubs/dfx/tsdb_outdir/dft_inserted_designs/hub_rtl.dft_inserted_design/hub.icl

/nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/OFFICIAL_SCRIPTS/tsdb_outdir/patterns/hub_rtl.patterns_signoff/hub_hbo_ks_p0_xsa_pmovi_x_s_hry.stil


All required for pattern generation
Monday, 1 December 2025
16:05

Pattern specs:
/nfs/site/disks/mfg_ptl_001/NVLAX/PATTERN_SPECS/
/nfs/site/disks/mfg_nvl_016/yfriedgu/run_area/deposit.list
Turnin list:
/nfs/site/disks/mfg_ptl_001/NVLAX/deposit.list
echo 4 | vaultdeposit -proj nvlhub_axa0 -turnin disp_pmovi_temp_turnin.list

/nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/mbist_test_selection_input_files/parallelconfig_ks.toml


Uri's email
Tuesday, 2 September 2025
11:40
Setup:
cd /nfs/site/disks/amaraaba_wa01/nvl_ax_a0/
source /p/hdk/pu_tu/prd/cth_infra/latest/setCTH -m hub -s nvlax-a0 -b master
setenv TESSENT_PLUGIN_PATH /nfs/site/disks/mfg_ptl_001/NVLAX/vtu_gfx/run/tsdb_outdir/instrumentation/customPlugin
source /nfs/site/disks/mfg_ptl_001/NVLAX/vtu_gfx/run/tsdb_outdir/tessent.env
setenv PYTHONPATH /usr/intel/pkgs/python3/3.12.3/modules/r1/lib64/python3.12/site-packages/
cd /nfs/site/disks/amaraaba_wa01/nvl_ax_a0/

setenv VAULT_TEST_RENAME <testname>

source /nfs/site/disks/mfg_ptl_001/NVLAX/patgen.csh

From  file: /nfs/site/disks/mfg_ptl_001/NVLAX/PATTERN_SPECS/hbo_ks_p0/hbo_ks_p0.pattern_spec
SSNDatapathOptions {
Datapath(hptp_wrapper_port) {
output_bus_width : 6;
}
}


Content parallel generation based on IDC : /nfs/iil/disks/mfg_lnl_023/umark/scripts/vaultdeposit_par.py:
> grep 'Patterns' /nfs/site/disks/mfg_ptl_001/NVLAX/PATTERN_SPECS/hbo_ks_p0/hbo_ks_p0.pattern_spec | awk -F'Patterns' '{print $2}' | sed 's/(//g' | sed 's/) {//g' | grep -v Specificationhub > hbo_ks_p0.testlist
> foreach i(`cat /nfs/site/disks/mfg_ptl_001/NVLAX/hbo_ks_p0.testlist`)
foreach? setenv VAULT_TEST_RENAME $i
foreach? source pat
PATTERN_SPECS/ patgen.csh
foreach? source /nfs/site/disks/mfg_ptl_001/NVLAX/patgen.csh
foreach? end










setenv STUBPATH /nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/OFFICIAL_SCRIPTS/STUB_ICLS_25ww09f/
setenv MBIST_COLLATERAL /nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/OFFICIAL_SCRIPTS/
setenv PATSPECLOCATION /nfs/site/disks/mfg_ptl_001/NVLAX/mbist-test-selection-v1.5.0/collateral_generation/PATTERN_SPECS/
setenv VAULT_TEST_RENAME hub_hbo_ks_p0_ssa_pmovi_y_r


Content Generation Flow
Sunday, 7 September 2025
15:21


Order of expected execution:  collateral generation>DUMS>STIL file generation
Common setup:


Collateral generation:


Digital Universal MBIST Scripts (DUMS):
Output: file with turnin commands, pattern spec.


STIL file generation:




Dictionary:
Absolutely! Here's a dictionary of commonly used terms and file types in the NVL-S MBIST content generation flow, especially relevant to Tessent Native and your work:

📁 File Types & Their Meanings


NVL-AX roadmap
Tuesday, 9 September 2025
14:11

1 - no MVE script - there is a new script that we use (Tim script) to generate the config files ( q to the meeting today, do we deposit configs or stils to vault)
2- lets say we generated the configs/stils, we need to take care of the turnin list and check if we have the rights intents.
3-how does the script work, what is the replacmenet of mastic where we set clocks/frequencies/Power domain/rom mem files....
4- Do we have all the instrumentation ready for all type of content, anything needed from our side?
5- naming convention for tests
6- how does DFx generate their configs (how different from TIm script)
7 - what changes do we need for the generation flow (iTrace not iTrace, local tool, parallel generation and parallel content)
8- HPTP vs TAP and how does it affect us.
9- FLOW MATRIX - a table for all supported frequencies per domain (most important LFM)
10 - dictionary for BISR content and collaterals generation and validation for HRY and RASTER and BISR.
11- content ownership in team

From <https://www.microsoft365.com/chat/?capabilities=interopPromise%2CsuspendOnClose%2CautoStart&client-request-id=d9b7293e-994c-c249-8e89-ede336bf75ef&version=19.2509.34011.0>



Headers enable
Tuesday, 16 September 2025
13:26

/nfs/site/disks/mfg_nvl_016/amaraaba
repo: /nfs/site/disks/nzonis_wa01/nvlhub_ax/for_user/
Source: source /nfs/site/disks/nzonis_wa01/repos/for_user_ww38/nvl_repo/mfg/sourceme -p nvlhub -s axa0
NB envs :
setenv WARD `pwd`
setenv NBQSLOT C2DG_FE_nvlaxa_DTSE_DEBUG
setenv NBPOOL sc8_normal
setenv NBCLASS "SLES12&&256G"


iTrace_manager -install -li lr_phase1a -saverundir -htd_hrv_mode -tag array_header_v1 -linus_overrides DUT_DIE=lite,SIMTYPE=simless



Sunday, 21 September 2025
15:15

setenv STUBPATH /nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/OFFICIAL_SCRIPTS/STUB_ICLS_25ww09f/
setenv MBIST_COLLATERAL /nfs/site/disks/mfg_ptl_001/NVLAX/nvlhub_a0/OFFICIAL_SCRIPTS/
setenv PATSPECLOCATION /nfs/site/disks/mfg_ptl_001/NVLAX/PATTERN_SPECS/


Latest release
Wednesday, 22 October 2025
12:24

Groups:



Please try below repo for enabling your line items and ensure you can run simless/emulation jobs.

Flash env is enabled; you can deposit your tests and ensure everything is working.

source /nfs/site/disks/epinhas_wa01/nvl/nvl_a0_ww43/nvl_repo/mfg/sourceme -p nvlhub -s axa0 -m cu_emu


Full flow enabling
Thursday, 30 October 2025
23:00





EMU/SIMLESS/SImulationj
Tuesday, 4 November 2025
14:43

Simless: source /nfs/site/disks/FE_dtse.integ.01/NVLAX_HUB/RELEASES/A0/dtse_nvlhub_axa0_v25_ww43a/mfg/sourceme -p nvlhub -s axa0
Emu: source /nfs/site/disks/FE_dtse.integ.01/NVLAX_HUB/RELEASES/A0/dtse_nvlhub_axa0_v25_ww43a/mfg/sourceme -p nvlhub -s axa0 -m cu_emu

setenv WARD `pwd`
setenv NBPOOL sc8_normal
setenv NBQSLOT C2DG_FE_nvlaxa_DTSE_DEBUG
setenv NBCLASS "SLES12&&64G"
iTrace_manager -li arr_mbist -tid 207413 -tag media_lsa_pmovi_dfxagg _mul5__01_2_v1 -linus_overrides DUT_DIE=lite,SIMTYPE=simulation -nots -install -saverundir


Before opening verdi:
/p/hdk/rtl/proj_tools/emu_tools/NVL_25.02.011/bin/emu_ztdb2zwd --class "SLES12&&64G" --qslot C2DG_FE_ptla_TLM_CSA --pool sc8_critical_gk

Emulation:
iTrace_manager -li arr_mbist -tid 225240 -tag hub_displsa_ks__lsa_pmovi_x_s_v0  -linus_overrides DUT_DIE=lite,SIMTYPE=emulation -nots -install -saverundir
Simless:
iTrace_manager -install -li arr_mbist_media_precat -tid 172170 -saverundir -tag array_media_precat_v0 -linus_overrides DUT_DIE=lite,SIMTYPE=simless -htd_hrv_mode
iTrace_manager -li arr_mbist -tid 207413 -tag media_lsa_pmovi_dfxagg _mul5__01_2_v1 -linus_overrides DUT_DIE=lite,SIMTYPE=simless -install -saverundir -htd_hrv_mode

iTrace_manager -li arr_mbist  -tid_file <file.list> -tag media_lsa_pmovi_dfxagg _mul5__01_2_v1 -linus_overrides DUT_DIE=lite,SIMTYPE=simless -install -saverundir -htd_hrv_mode



Simulation:
iTrace_manager -li arr_mbist_sim -tid 223191-tag memss0_pmovi_sim_v1 -linus_overrides DUT_DIE=lite,SIMTYPE=sim -nots -install -saverundir
iTrace_manager -install -li  arr_mbist_sim  -saverundir -htd_hrv_mode -tag memss0_pmovi_sim_v2 -linus_overrides DUT_DIE=lite,SIMTYPE=sim,atomfreq=disabled,memssfreq=disabled,defreq=disabled,mediafreq=disabled,dpunpufreq=disabled &

From <https://wiki.ith.intel.com/spaces/HTD/pages/4555486218/dtse_nvlhub_axa0_v26_ww04a>

186
31456

## test_id: 223191
## owner: arr
## testtype/attributes: array_mbist/burnin,hvm_req
## stepping: nvlhub_axa0
## file_rev: 0
## record_rev_id: 1
223191 /p/pde/tvpv/global_db/apparatelocalddg/dev/__rev0/Test/191/223191/223191/memss0_ks.pattern_spec  VAULT_TEST_RENAME=replace:hub_memss0_ks__xsa_pmovi_x_s -dirtag hub_memss0_ks__xsa_pmovi_x_s VAULT_RECORD_REV=1 VAULT_FILE_REV=0

## te


Eitan Email
Thursday, 27 November 2025
16:47

NVL Permissions Page - HTD Wiki - Intel Enterprise Wiki

Release model:
/nfs/site/disks/FE_dtse.integ.01/NVLAX_HUB/RELEASES/A0/dtse_nvlhub_axa0_v25_ww43a

Model_root EMU:
/nfs/site/proj/nvlax/nvlax.emulation.models.01//fc_emu/fc_emu-nvlax-a0-master-25ww35a
Model_root RTL:
/nfs/site/proj/nvlax/nvlax.models.11/hub//hub-nvlax-a0-master-25ww36a

Highlights:
Enabled features/flows:
Simless
Emulation
Flash & Vault

Setup:
Simless: source /nfs/site/disks/FE_dtse.integ.01/NVLAX_HUB/RELEASES/A0/dtse_nvlhub_axa0_v25_ww43a/mfg/sourceme -p nvlhub -s axa0
Emu: source /nfs/site/disks/FE_dtse.integ.01/NVLAX_HUB/RELEASES/A0/dtse_nvlhub_axa0_v25_ww43a/mfg/sourceme -p nvlhub -s axa0 -m cu_emu
Set envs: nvl_envs

Headers location and rules files line:
Location: SC8:
/p/pde/tvpv/nvlhub/headers/HAX/A0/
Include this line at beginning of header:
::LINUS_INC $HVM_ROOT/mfg/rules/LiRules.py


iTrace_manager commands:
Simless: iTrace_manager -install -launch -li ssn_cont -saverundir -htd_hrv_mode -tag dtse_is_the_best_team_ever -linus_overrides DUT_DIE=lite,SIMTYPE=simless &
Emulation: iTrace_manager -install -launch -li lr_phase1a -saverundir -htd_hrv_mode -tag reset_team_is_the_best_team -linus_overrides DUT_DIE=lite,SIMTYPE=emulation -nots  &

Generate and open FSDB in EMU or VCS (TLS)
Switches in list file (both emu or vcs):
.nbclass SLES12&&64G&&6C
+overrides -ms -fsdb -c 1700us -fsdbstart 0 -fsdblength 1700us -ms- -dirtag fsdb
Or:
+overrides -ms -fsdb -c 1700us -fsdbstart 100us -fsdblength 1700us -ms- -dirtag fsdb
Where:
-c: when to stop run (not stop dumping)
-fsdbstart: time to start dumping
-fsdblength: fsdb window
Units are in us (micro seconds), except for time 0 where you don’t specify us units.
To align emu/vcs to us units:
▪ Remove 6 digits from time unit (in ps).
▪ For example, from logbook: {23456789 ps} eq to 23us
FSDB window in EMU:
• Don’t exceed 10us.
For example:
+overrides -ms -fsdb -c 10us -fsdbstart 0 -fsdblength 10us -ms- -dirtag fsdb
In EMU:
Cd to rundir
Convert ztdb file:
/p/hdk/rtl/proj_tools/emu_tools/NVL_25.02.011/bin/emu_ztdb2zwd --class "SLES12&&64G" --qslot C2DG_FE_ptla_TLM_CSA --pool sc8_critical_gk &
Run: emu_verdi &


Failinj issue
Tuesday, 2 December 2025
14:53







Meeting today
Wednesday, 10 December 2025
11:56

Ownership on various content types
○ KS
○ HRY
○ HVQK
Raster
Repair
BLS
Infra and ENV and collaterals 1 owner
ROM?
Validation plan tracker modidivation - need to add memtype
Array info
Contact in DFx and how to communicate
Power and clocks excel - need to ask reset to set the right freqs
DV tests requirement
Coverage script
Soft algos
Test time estimation
Tagging script and release notes structure
Scol



Clocks
Sunday, 14 December 2025
16:20

https://docs.intel.com/documents/ClientSilicon/nvl/global/Clock/NVL%20Clock%20HAS/NVL%20Clock%20HAS.html#punitS















MEDIA SSN issue
Tuesday, 27 January 2026
14:09

To check what was generated with SSN and what with TAP look for run_steps:
Solving ProcedureStep(customProc_0)
1171 //  Warning: There were 172 SSN_R1 violations (Inferring SSH instances from ICL).
1172 //        Solving TestStep(run_steps)
1173 //  Warning: There were 172 SSN_R1 violations (Inferring SSH instances from ICL).
'sfc_media.par_smdecode42.smscmi0_smdecode41.alnunit1_smdecode4_rtl_tessent_mbist_bap_inst.smdecode4_rtl_tessent_mbist_bap_tdr_short_inst.memory_mfg_test_reg', inac
1329 //           It will be accessed in global IJTAG mode.

to check what faills back to TAP:
1327 //  Warning: The following write target is in a local IJTAG network of an inactive SIH:
1328 //              'sfc_media.par_smdecode42.smscmi0_smdecode41.alnunit1_smdecode4_rtl_tessent_mbist_bap_inst.smdecode4_rtl_tessent_mbist_bap_tdr_short_inst.memory_mfg_test_reg', inactive SIH 'sfc_media.par_smdecode42.cdu_smdecode4   1328 1_vccsa_ps_hcp0.cdu_smdecode41_vccsa_ps_hcp0_ijtag_tessent_ssn_ijtag_host_sih0_inst_cdu_smdecode41_vccsa_ps_hcp0_ijtag_tessent_ssn_ijtag_host_sih0_inst_i'
1329 //           It will be accessed in global IJTAG mode.


DFTCOPILOT
Sunday, 15 February 2026
15:08

TODO:
Check if we can auto get token per user
or add to aliases .cshrc
Integrate co-design
Find best FSDB window
Debug FSDB runs
Why its better than using direct VS code?
Work with lvlibs
Work on VS
Fully automated runs for iTrace
Open VS:

& "$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe"  --user-data-dir "$env:TEMP\vscode-clean"  --disable-workspace-trust   --disable-extensions   --disable-gpu


Keys:
sed -i 's/^setenv OPENAI_API_KEY .*/setenv OPENAI_API_KEY pak_e6_qzLABhWrwyET6qU7Dim-j4xpuXHmXMPOdMGXwM1Y/' .env.csh
sed -i 's/setenv OPENAI_API_KEY .*/setenv OPENAI_API_KEY pak_3loJs765Hs99m7RJPE6saMRn2YvxFxN1_JOE7OesCjs/' /nfs/site/disks/mfg_nvl_016/amaraaba/scripts/dftcopilot/users/$USER/env.csh
Ahmad: pak_ORn_gt8bDfpuCOf-l1CyjTKV10i5PapUimSLUREujpQ
Ibraheem: pak_ORn_gt8bDfpuCOf-l1CyjTKV10i5PapUimSLUREujpQ
Guy: pak_3loJs765Hs99m7RJPE6saMRn2YvxFxN1_JOE7OesCjs
Lama: pak_e6_qzLABhWrwyET6qU7Dim-j4xpuXHmXMPOdMGXwM1Y

How to run
source .venv/bin/activate.csh
source .env.csh 
python dftcopilot.py agent -v



DFX
Tuesday, 24 February 2026
15:30

Inputs for discussion with DFT

Communication & work mode
- Clear contacts to work with
- DFT people availability, we must have instant approach to people in DFT team
- Optionally: weekly meeting for sync with the relevant people
- Documentation and organization
○ Clear mail communication and notifications on insertion area changes, PM config changes, precats etc.
○ Do we need a shared drive or Teams channel?

Deliveries
- Array-info - including repair data, TT?
- Validated and clean portable tsdb (tgz) and insertion areas - once created no changes unless clearly communicated

○ Broken
§ Tgz stopped working due to few dirs deleted
§ (itrace flow is built for tgz)
○ Clean
§ Have to be lower than 1GB
§ Not create tests in it

- Tests' run modes/granularity/flavors
- Models used for tests run
- Mastic configs:
○ Real (partition) names
○ Include relevant/real clock names
○ Power delivery info
○ HVM worthy (to be used as is)

BISR
- Define the exact delivery including data and format (Mastic commands regression list in order to align tests to chains to arrays)
○ List of BIRA tests validation for every RotRead
○ Lookup table with IP, bisr ctrl, bist chain, tests, etc.
- Validation flow
Other documentation



DFT
• Array info
• Precat - separated per IP (per our definition)
• Initial MasticX PM config - we are taking it one step forward and returning to DFT
• MBIST: Insertions/TSDB/TGZ +renaming (done by script) + <1GB size
• Repair
○ full regression list
○ MasticX commands, revision, configuration PM config
○ Mapping of BISR chain to IP
○ Fuse to IP mapping
• Raster + LYA
○ Atom + LLC L2P. CTV mapping (for template parsing)
○ L2R
Tool
• Generation tool
• Collateral generation tools
• Tester Templates

Design
• DV+ RWA plan/requirements +
• RWA fuses

Customer expectations (from us)
• Full content delivery (all types)
Info related to clocks and Power


DAISO
Tuesday, 2 June 2026
21:46

Dev branch for protection
Ask for github pro for classic branch protection rules
Github course for all
Stash and pop


TFM
Wednesday, 10 June 2026
15:08

Are we building and maintaining the tools?
Why not give DTEG to build all?
It's a big project - whats the plan?
Reuse vs new
/nfs/site/disks/mfg_ptl_001/NVLAX/deposit.list

| Area | Files | Requirements | Notes |
|---||---||---||---|
| Model | TSDB (unzipped) | Folder structure : 
tsdb_outdir/.* 
> 
mem_tcd | tsdb_outdir: will have the tsdb files and will output natively, unless design changes names.
 
mem_tcd: will have the memory tcds needed for the memory dimensions. |
| Model | load_model.do | Will have pointers to all tsdb in current model |  |
| Model | *.icl | Only 1 top level icl per model |  |


| Area | Files | Requirements | Notes |
|---||---||---||---|
| Model | generate_summaries | Invokes tessent , setsup env and  calls generate_summaries.do | Output:
*.dft_summary
design.toml
*.repair_dict |
| Model | generate_summaries.do | Load :
 soc level icl,
instrumentation
load_model.do
 
generate:
 *.dft_summary
design.toml
*.repair_dict |  |


| Area | Files | Output | notes |
|---||---||---||---|
| local | *.dft_summary
Design.toml
*.repair_dict |  |  |
| local | parallel_config.toml | Defines parallel groups to be run | MBIST Test Selection · intel-innersource/applications.manufacturing.intel.array.mbist-test-generation Wiki |
| local | Configuration.toml | Project configuration setup | MBIST Test Selection · intel-innersource/applications.manufacturing.intel.array.mbist-test-generation Wiki |
| local | Modifications.toml | Any type of modification for the project(corner cases) | MBIST Test Selection · intel-innersource/applications.manufacturing.intel.array.mbist-test-generation Wiki |
|  |  |  |  |


| Area | files | Requirements | Notes |
|---||---||---||---|
| Model | native_tessent.do | Calls:
 soc level icl,
instrumentation
load_model.do
pattern_spec | Current setup with DRV flows hooked together:
Copies files, renames env setup, vault deposit etc |


| File Type / Term | Meaning / Purpose |
|---||---|
| .icl | Instrumentation Control Language file. Defines the top-level design and memory instrumentation setup for MBIST. Only one top-level ICL per model. |
| .do | Tessent Shell Script. Contains commands for Tessent to execute (e.g., load model, generate patterns). Used in automation flows. |
| .conf | Configuration File. Used to define concurrency, environment setup, or flow behavior (e.g., concurrency.conf, configuration.conf). |
| .toml | TOML Configuration File. Used in DUMS to define parallel execution (parallel_config.toml), project setup (Configuration.toml), and overrides (Modifications.toml). |
| .dft_summary | Design-for-Test Summary. Output from generate_summaries.do, includes test coverage and memory instrumentation details. |
| design.toml | TOML file describing the design structure and test configuration. Used by DUMS and STIL generation. |
| .repair_dict | Dictionary of repairable faults and memory repair strategies. Generated during collateral creation. |
| pattern_spec | Specification file for MBIST pattern generation. Defines how patterns are created and what they target. |
| native_tessent.do | Main Tessent script for STIL generation. Calls ICL, instrumentation, and model setup. |
| load_model.do | Script that loads TSDB and other model files into Tessent. |
| generate_summaries.do | Script that runs Tessent to produce summaries and repair dictionaries. |
| TSDB | Test Structure Database. Contains memory and test structure definitions. Must be unzipped and follow a specific folder structure. |
| mem_tcd | Memory Test Configuration Data. Contains memory-specific test setup used by Tessent. |
| PDQE | Pattern Development Quality Engineering. Refers to scripts and processes for generating and validating MBIST patterns. |
| DUMS | Digital Universal MBIST Scripts. Automates pattern spec creation, tagging, and vault turn-in commands. |
| COGS | Collateral for DUMS. Supports DUMS with necessary design and test files. |
| Vault | Central repository for MBIST content submission and validation. |
| STIL | Standard Test Interface Language. Format used to describe test patterns for simulation and tester execution. |
| VTPSIM | Simulation tool for verifying tester patterns. |
| VTRAN | Converts STIL files to tester-compatible formats. |
| PDL | Pattern Description Language. Used for describing test patterns, especially for TAP-based access. |
| TAP | Test Access Port. A standard interface for accessing test logic in chips. |
| HPTP / SSN | High-speed test protocols used in MBIST flows. Often require special handling in pattern generation. |


| 225240 |
|---|
| 223191 |


| hub_memss0_ks__xsa_pmovi_x_s |
|---|


| Workstream | Deliverable | notes | Owner |
|---||---||---||---|
| DFx Insertions Intake | Receive MBIST controller RTL insertions list (load_module.do) | upload to teams folder | Uri |
| ArrayInfo Intake | Array Info file received | received , new teams folder for NVL AX |  |
| Vault and iTrace | Configs for Vault, and iTrace for STIL |  |  |
| Special content | Instrumentation and collaterals for special content | Uri to enable fusereadout, SAR for raster (matchloop TBD), New collaterals gen scripts (need to check) | Uri |
| Clocks and PD | DFx to deliver config | Need to find where to define (new config?), MBIST pm? | Uri, Yael |
| RAGN Configuration | RAGN values defined per frequency & corner | Modify Expandata script to support STIL, Define values in flash RAGN config | Yael |
| Scoreboards Setup | Scoreboard templates per domain (gen/emu/vtpsim/tagging) | Build scoreboard (generaion/validation) | Ahmad |
| Lineitems, headers & Reset POR | Define lineitems + header + reset per content type (KS & Special) | 6 resets, 6 precats, need to define Lis, header per domain | LineItems(Ahmad/Yael), Headers ( Uri to provide basic and owners to adjust per domain) |
| TID Generation | Run MBIST test_selection to generate configs, Tessent do_file  for STIL |  |  |
| Simless Samples | Generate pmovi + failinj simless samples |  |  |
| Emulation (pmovi) | Run emulation for pmovi; populate scorecard |  |  |
| VTPSIM (pmovi) | Run VTPSIM for pmovi with FSDB; populate scorecard |  |  |
| TTR Parallelization | Generate parallel content where feasible (TT reduction) |  |  |
| Content & Tagging | KS traces/content + FLASH conversion + NVL tagging per domain |  |  |
| PCAR/Plists | Initial PCAR ordering + plist structure for NVL Arrays |  |  |
| IFPM Optimization | Run optimizing script for IFPM after content validation |  |  |
| Full Content Generation | Generate KS, HRY, RASTER, BISR, RETENTION content |  |  |
| Paranoia Check | Run paranoia checks on generated content |  |  |
| Collaterals & PCAR | Generate BISR/RASTER collaterals; build basic PCARs |  |  |
| Release Notes & Handoff | Prepare release notes; package content for Sort/Class |  |  |
