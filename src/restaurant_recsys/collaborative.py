from __future__ import annotations
from collections import defaultdict
from typing import List, Tuple
from .data import Restaurant, Review

class CollaborativeRecommender:
    def __init__(self, restaurants: List[Restaurant], reviews: List[Review]):
        self.restaurants = {r.business_id: r for r in restaurants}
        self.user_ratings = defaultdict(dict)
        self.item_ratings = defaultdict(list)
        for rev in reviews:
            self.user_ratings[rev.user_id][rev.business_id] = rev.stars
            self.item_ratings[rev.business_id].append(rev.stars)
        self.global_mean = sum(r.stars for r in reviews)/len(reviews) if reviews else 3.5

    def score(self, user_id: str, business_id: str) -> float:
        user_vals = list(self.user_ratings.get(user_id, {}).values())
        user_mean = sum(user_vals)/len(user_vals) if user_vals else self.global_mean
        item_vals = self.item_ratings.get(business_id, [])
        item_mean = sum(item_vals)/len(item_vals) if item_vals else self.global_mean
        return 0.55 * item_mean + 0.45 * user_mean

    def recommend(self, user_id: str, k: int = 5) -> List[Tuple[float, Restaurant]]:
        seen = set(self.user_ratings.get(user_id, {}))
        scored = []
        for bid, r in self.restaurants.items():
            if bid not in seen:
                scored.append((self.score(user_id, bid), r))
        return sorted(scored, key=lambda x: x[0], reverse=True)[:k]
