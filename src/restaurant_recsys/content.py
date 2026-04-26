from __future__ import annotations
import math, re
from collections import Counter
from typing import List, Tuple
from .data import Restaurant

WORD = re.compile(r"[a-zA-Z0-9_]+")

def toks(s: str):
    return WORD.findall(s.lower())

class ContentRecommender:
    def __init__(self, restaurants: List[Restaurant]):
        self.restaurants = restaurants
        self.docs = [Counter(toks(r.name + " " + r.categories + " " + r.city)) for r in restaurants]
        df = Counter()
        for d in self.docs:
            df.update(set(d))
        n = max(1, len(restaurants))
        self.idf = {t: math.log((n+1)/(c+1))+1 for t,c in df.items()}

    def recommend(self, query: str, k: int = 5) -> List[Tuple[float, Restaurant]]:
        q = Counter(toks(query))
        scored = []
        for r, d in zip(self.restaurants, self.docs):
            score = sum(q[t] * d.get(t,0) * self.idf.get(t,1.0) for t in q)
            scored.append((score, r))
        return [(s,r) for s,r in sorted(scored, key=lambda x: x[0], reverse=True)[:k] if s > 0]
