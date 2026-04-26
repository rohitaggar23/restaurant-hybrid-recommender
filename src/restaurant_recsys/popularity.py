from __future__ import annotations
from typing import List, Tuple
from .data import Restaurant

def popularity(restaurants: List[Restaurant], city: str | None = None, k: int = 5) -> List[Tuple[float, Restaurant]]:
    rows = [r for r in restaurants if city is None or r.city.lower() == city.lower()]
    if not rows:
        return []
    c = sum(r.stars for r in rows) / len(rows)
    counts = sorted(r.review_count for r in rows)
    m = counts[int(0.75 * (len(counts)-1))]
    def score(r: Restaurant):
        v = r.review_count
        return (v/(v+m))*r.stars + (m/(v+m))*c if (v+m) else r.stars
    return sorted([(score(r), r) for r in rows], key=lambda x: x[0], reverse=True)[:k]
