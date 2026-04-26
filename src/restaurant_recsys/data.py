from __future__ import annotations
from dataclasses import dataclass
from typing import List
import json

@dataclass
class Restaurant:
    business_id: str
    name: str
    categories: str
    city: str
    stars: float
    review_count: int
    latitude: float
    longitude: float

@dataclass
class Review:
    user_id: str
    business_id: str
    stars: float


def load_restaurants(path: str) -> List[Restaurant]:
    with open(path, "r", encoding="utf-8") as f:
        return [Restaurant(**json.loads(line)) for line in f if line.strip()]


def load_reviews(path: str) -> List[Review]:
    with open(path, "r", encoding="utf-8") as f:
        return [Review(**json.loads(line)) for line in f if line.strip()]
