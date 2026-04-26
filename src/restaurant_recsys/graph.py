from __future__ import annotations
from collections import defaultdict
from typing import List, Tuple
from .data import Restaurant, Review

class GraphRecommender:
    """User-item graph proximity via two-hop co-preference counts."""
    def __init__(self, restaurants: List[Restaurant], reviews: List[Review]):
        self.restaurants = {r.business_id: r for r in restaurants}
        self.user_items = defaultdict(set)
        self.item_users = defaultdict(set)
        for rev in reviews:
            if rev.stars >= 4:
                self.user_items[rev.user_id].add(rev.business_id)
                self.item_users[rev.business_id].add(rev.user_id)

    def recommend(self, user_id: str, k: int = 5) -> List[Tuple[float, Restaurant]]:
        seen = self.user_items.get(user_id, set())
        scores = defaultdict(float)
        for item in seen:
            for neighbor_user in self.item_users[item]:
                if neighbor_user == user_id:
                    continue
                for candidate in self.user_items[neighbor_user]:
                    if candidate not in seen:
                        scores[candidate] += 1.0
        return sorted([(s, self.restaurants[bid]) for bid, s in scores.items() if bid in self.restaurants], key=lambda x: x[0], reverse=True)[:k]
