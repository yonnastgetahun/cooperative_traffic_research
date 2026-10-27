# R4 — Development-only paired seed analysis (no M3 freeze)

This is a dry run of the predeclared formulas using three already inspected seeds per regime.
Each row in the summary represents the variability of **seed-level paired mean errors**; road-edge traversals are not assumed independent.

| Window | Mean improvement in timing MAE (FF − time-aware), s | Sample SD across 3 seeds, s | Mean TA lateness bias, s |
|---|---:|---:|---:|
| 200s | 5.48 | 0.14 | 54.38 |
| 600s | 3.97 | 0.07 | 19.27 |
| 1200s | 3.52 | 0.09 | 13.45 |

All numbers here are **exploratory development results**. No Student-t held-out confidence interval is calculated from these three seeds.
The later evaluation design targets ten untouched paired seeds per regime, subject to independent freeze authorization.
The time-aware predictor may show lower error while still systematically predicting arrival too early.
Do not equate prediction quality with improved network-wide traffic outcomes.
