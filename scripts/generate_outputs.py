from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from restaurant_recsys.data import load_restaurants, load_reviews
from restaurant_recsys.hybrid import HybridRecommender

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'

for d in ['metrics', 'tables', 'figures', 'reports', 'logs', 'recommendations']:
    (OUT / d).mkdir(parents=True, exist_ok=True)


def quality_proxy(items: list[dict]) -> float:
    """A simple offline proxy metric used for the sample dataset.

    If any recommended item has stars >= 4.2, treat it as 'useful' for this toy offline metric.
    This keeps the demo self-contained without a held-out test set.
    """

    useful = sum(1 for x in items if x.get('stars', 0) >= 4.2)
    return useful / max(1, len(items))


def main() -> None:
    restaurants = load_restaurants(str(ROOT / 'data/sample_restaurants.jsonl'))
    reviews = load_reviews(str(ROOT / 'data/sample_reviews.jsonl'))

    rec = HybridRecommender(restaurants, reviews)

    user_recs = rec.recommend(
        user_id='u1',
        query='spicy noodles vegetarian',
        lat=40.72,
        lon=-73.99,
        city='New York',
        k=6,
    )

    cold_recs = rec.recommend(
        user_id=None,
        query='coffee dessert cafe',
        lat=40.72,
        lon=-73.99,
        city='New York',
        k=6,
    )

    metrics = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'project': 'Restaurant Hybrid Recommender',
        'notes': 'Started as a notebook prototype; refactored into a package with portable sample data and exported artifacts.',
        'dataset': {
            'restaurants': len(restaurants),
            'reviews': len(reviews),
            'users': len(set(r.user_id for r in reviews)),
        },
        'offline_metrics': {
            'precision_proxy_at_6': round(quality_proxy(user_recs), 4),
            'cold_start_precision_proxy_at_6': round(quality_proxy(cold_recs), 4),
            'catalog_coverage_in_two_queries': round(
                len({x['business_id'] for x in user_recs + cold_recs}) / max(1, len(restaurants)),
                4,
            ),
            'top_user_score': user_recs[0]['score'] if user_recs else 0,
        },
    }

    (OUT / 'metrics/recommender_metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    (OUT / 'recommendations/user_u1_recommendations.json').write_text(json.dumps(user_recs, indent=2), encoding='utf-8')
    (OUT / 'recommendations/cold_start_recommendations.json').write_text(json.dumps(cold_recs, indent=2), encoding='utf-8')

    with (OUT / 'tables/recommendation_score_table.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['rank', 'business_id', 'name', 'score', 'categories', 'stars'])
        w.writeheader()
        for i, x in enumerate(user_recs, 1):
            w.writerow({'rank': i, **x})

    # Plots
    plt.figure(figsize=(8, 5))
    plt.bar([x['name'] for x in user_recs], [x['score'] for x in user_recs])
    plt.xticks(rotation=25, ha='right')
    plt.ylabel('Hybrid score')
    plt.title('Top recommendations (user u1)')
    plt.tight_layout()
    plt.savefig(OUT / 'figures/top_scores.png', dpi=180)
    plt.close()

    plt.figure(figsize=(7, 5))
    stars = [r.stars for r in reviews]
    plt.hist(stars, bins=[1, 2, 3, 4, 5, 6], align='left', rwidth=0.8)
    plt.xlabel('Review stars')
    plt.ylabel('Count')
    plt.title('Sample rating distribution')
    plt.tight_layout()
    plt.savefig(OUT / 'figures/rating_distribution.png', dpi=180)
    plt.close()

    plt.figure(figsize=(7, 5))
    keys = list(metrics['offline_metrics'].keys())
    vals = list(metrics['offline_metrics'].values())
    plt.bar(keys, vals)
    plt.xticks(rotation=25, ha='right')
    plt.title('Offline demo metrics')
    plt.tight_layout()
    plt.savefig(OUT / 'figures/offline_metrics.png', dpi=180)
    plt.close()

    report = f"""# Restaurant Hybrid Recommender — Experiment Report

Generated: {metrics['generated_at']}

## What was run

The run generates:

- a **personalized** set of recommendations for a known user (`u1`)
- a **cold-start** set of recommendations with no user history

Both are produced from the included sample dataset.

## Key artifacts

- `outputs/metrics/recommender_metrics.json`
- `outputs/recommendations/user_u1_recommendations.json`
- `outputs/recommendations/cold_start_recommendations.json`
- `outputs/figures/top_scores.png`

## Metrics

```json
{json.dumps(metrics['offline_metrics'], indent=2)}
```
"""

    (OUT / 'reports/EXPERIMENT_REPORT.md').write_text(report, encoding='utf-8')
    (OUT / 'logs/run.log').write_text(
        'Restaurant Hybrid Recommender output generation completed successfully.\n' + json.dumps(metrics, indent=2),
        encoding='utf-8',
    )

    # Small notebook snapshot (optional convenience)
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Restaurant Hybrid Recommender — Demo Run\n",
                    "This notebook is a lightweight snapshot of the latest generated metrics.\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "output_type": "stream",
                        "name": "stdout",
                        "text": [json.dumps(metrics, indent=2) + "\n"],
                    }
                ],
                "source": ["# Generated by scripts/generate_outputs.py\n"],
            },
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    (ROOT / 'notebooks/restaurant_recommender_demo.ipynb').write_text(json.dumps(nb, indent=1), encoding='utf-8')

    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()
