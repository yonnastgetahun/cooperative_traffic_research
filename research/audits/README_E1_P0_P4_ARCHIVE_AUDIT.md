# E1 post-Stage-1D P0–P4 read-only physical investigation: reproducibility

This directory contains the [E1 P0–P4 original-archive scientific audit script](e1_p0_p4_archive_audit.py), accompanied by the [completed report](../../docs/POST_EXP007_E1_P0_P4_PHYSICAL_MECHANISM_FAILURE_FINAL_REPORT_2026-11-03.md) and [frozen prospective plan](../../docs/POST_EXP007_E1_PHYSICAL_MECHANISM_FAILURE_INVESTIGATION_SPEC_AND_PLAN_2026-11-03.md).

**Scientific boundary:** This process does **not** execute SUMO, change the original E1 estimator, fit any capacity parameter, run new counterfactuals, retune old results, or generate independent validation labels. All original 4101–4105 and development 5101–5114 seeds remain previously inspected. Historic Test A and E1 Stage 1D stay NO-GO, Test B not run.

## Exact original evidence and source

- [Permanent original full Stage 1D release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-stage1d-development-2026-11-03): original 706 ZIP member bytes repackaged with SHA-256 member ledger; includes 60 × 1,000-driver SUMO tripinfos, 60 edgeData and 60 laneData gzip XML files, frozen route/demand/network manifests, predictions and labels.
- [Original GitHub Actions execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41737336992), original ZIP SHA-256 f8d2b76bd6eda63e11889bd7708888bfdb55af78edd0b30526a9d981feb72fa6.
- Frozen E1 source at original execution commit **05b770cf000f84677524e0a1e89bea06ec0e703b**. The audit checks the expected original Git blob SHA for the unchanged FIFO engine **0d446e2c52efd2b75adf351ad5d577f442a4ac29** and original static SUMO input adapter **4ddc2034944354a1605bc798c8df1850e51ea897**.
- The source code from the original commit remains source of truth; current main is accepted for no-SUMO fixtures only because the two cited model blobs are asserted unchanged.

## Run locally

Use Python 3.11+ with lxml 6.0.2, standard library and extracted original archive member files. From the repository root:

~~~bash
python3 -m pip install 'lxml==6.0.2'
mkdir -p original_e1_stage1d
# Extract the 'e1-stage1d-original-member-bytes-2026-11-03.zip'
# asset from the linked GitHub release into original_e1_stage1d.
python3 research/audits/e1_p0_p4_archive_audit.py \
    --root original_e1_stage1d \
    --out audit/p0_p4_e1
~~~

To avoid manual file handoff, the [GitHub archive-only workflow](../../.github/workflows/exp007-e1-p0-p4-archive-mechanism-investigation.yml) downloads the **existing** development artifact from run 41737336992 and runs the audit with no SUMO dependency. The uploaded audit tables are derived research outputs, not held-out confirmation.

**Script output:**
- integrity_60_arms.csv
- edge_detector_24_arms.csv
- external_edge_waiting_contrasts.csv
- top_external_waiting_edges.csv
- bundle_detector_interactions.csv
- devbuild_parameter_sensitivity.csv
- p0_p4_summary.json

The final scientific report preserves a compact, permanent subset under [docs/results](../../docs/results/) with prefix exp007_e1_p0_p4_. The script reconstructs **original independent and perturbed scenario observations**, using matched scenario IDs, five-second edgeData intervals and read-only original E1 predicted vehicle times. The compact tables are *not* a substitute for all 706 original members; raw data remain in the durable release.

**Interpretation discipline:** Edge waiting is a sampled, aggregated vehicle-time measure and not identical to 1,000-driver elapsed-time cost or 999-driver externality. The original archive has no FCD; five-second edgeData is not a per-vehicle road-entry trace. P3 toy fixture labels for compatible and incompatible turns are **stipulated by the fixture**, not independently decoded SUMO priority-junction turn compatibility. Full matched-seed SUMO causality of any particular junction remains unresolved.

**Reproducibility note:** Runtime lxml pin is an XML streaming helper, not a physical simulator, estimator or source of traffic predictions. CI does not create any new SUMO data; a successful audit is integrity and source-analysis success only.
