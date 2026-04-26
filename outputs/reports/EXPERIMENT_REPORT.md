# Restaurant Hybrid Recommender - Experiment Report

Generated: 2026-04-22T05:59:05.215044+00:00

## Run Scope

The run generates personalized recommendations for known user `u1` and cold-start recommendations for a new user profile. Both outputs are produced from the included sample restaurant dataset.

## Key Artifacts

- `outputs/metrics/recommender_metrics.json`
- `outputs/recommendations/user_u1_recommendations.json`
- `outputs/recommendations/cold_start_recommendations.json`
- `outputs/tables/recommendation_score_table.csv`
- `outputs/figures/top_scores.png`
- `outputs/figures/rating_distribution.png`
- `outputs/figures/offline_metrics.png`

## Dataset Summary

| Entity | Count |
|---|---:|
| Restaurants | 18 |
| Users | 10 |
| Reviews | 50 |

## Metrics

| Metric | Result |
|---|---:|
| precision_proxy_at_6 | 1.0000 |
| cold_start_precision_proxy_at_6 | 0.8333 |
| catalog_coverage_in_two_queries | 0.4444 |
| top_user_score | 13.5855 |
