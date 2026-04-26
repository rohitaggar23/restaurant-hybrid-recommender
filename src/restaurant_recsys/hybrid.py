from __future__ import annotations
from collections import defaultdict
from typing import List
from .data import Restaurant, Review
from .content import ContentRecommender
from .collaborative import CollaborativeRecommender
from .graph import GraphRecommender
from .location import nearby
from .popularity import popularity

class HybridRecommender:
    def __init__(self, restaurants: List[Restaurant], reviews: List[Review]):
        self.restaurants = restaurants
        self.content = ContentRecommender(restaurants)
        self.cf = CollaborativeRecommender(restaurants, reviews)
        self.graph = GraphRecommender(restaurants, reviews)

    def recommend(self, user_id: str | None = None, query: str | None = None, lat: float | None = None, lon: float | None = None, city: str | None = None, k: int = 5):
        scores = defaultdict(float)
        objects = {r.business_id: r for r in self.restaurants}

        def add(items, weight):
            for rank, (score, r) in enumerate(items, 1):
                scores[r.business_id] += weight * (score + 1.0 / rank)

        if query:
            add(self.content.recommend(query, k=10), 1.2)
        if user_id:
            add(self.cf.recommend(user_id, k=10), 1.0)
            add(self.graph.recommend(user_id, k=10), 0.8)
        if lat is not None and lon is not None:
            add(nearby(self.restaurants, lat, lon, k=10), 0.7)
        add(popularity(self.restaurants, city=city, k=10), 0.5)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
        return [{"business_id": bid, "name": objects[bid].name, "score": round(score, 4), "categories": objects[bid].categories, "stars": objects[bid].stars} for bid, score in ranked]
