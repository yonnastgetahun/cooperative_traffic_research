# Cooperative Traffic Research — Research-pivot social publication record

**Status:** LinkedIn and X **PUBLISHED** on November 8, 2026 UTC after explicit user approval. **Do not retry or republish.**

## LinkedIn — document carousel

- Post: https://www.linkedin.com/feed/update/urn:li:ugcPost:7525113243074252800/
- LinkedIn Posts API: `201 Created`, returned `urn:li:ugcPost:7525113243074252800`.
- Media: exact approved **five-page PDF** (716,744 bytes), SHA256 `0f0042b44a08ca4c726e94a71cbc3506375d3e1d00035e0ba38a6773a14ff34d`.
- Caption: `social/linkedin/traffic_pivot_announcement.txt`, with historical research hashtags and traffic-specific tags.
- Successful GitHub Actions: https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42463395847
- First attempt: https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42463042920 — LinkedIn uploaded the PDF but stopped on an optional document GET (HTTP 400), **before post creation**. LinkedIn-only corrected attempt succeeded through [PR #112](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/112).

## X — four-image research announcement

- Post: https://x.com/yonnastgetahun/status/2119346244766031969
- X API returned post ID `2119346244766031969` and verified **all four media keys** on readback.
- Media: the approved `02_result`, `03_controls`, `04_rng`, `05_pivot` PNG panels, each byte-verified before publishing. Dedicated cover `01_cover` is in the LinkedIn PDF.
- Caption: `social/x-traffic-pivot-2026-11-08-draft.txt` with the same seven historical research hashtags plus `#TrafficResearch`.
- GitHub Actions: https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42463042920 — overall result flagged failure because LinkedIn's first attempt stopped, but the **X job succeeded**, and media readback passed. Approved publication introduced by [PR #111](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/111).
- **X was not republished** during LinkedIn recovery.

## Research integrity and nonpublication boundaries

This is a scientific research **pivot announcement**, not proof that cooperative traffic improves flow, not a conclusion that SUMO is invalid, and not a completed cross-simulator experiment. Source findings remain at [Post-T1 scientific report](../../docs/POST_T1_SUMO_RNG_EVENT_ORDER_AND_PHYSICAL_PROPAGATION_SOURCE_AUDIT_FINAL_REPORT_2026-11-07.md). Neither publishing workflow ran new SUMO simulations or changed any scientific verdict. No Metricool subscription was used. No credentials, tokens, or private user data are recorded here.
