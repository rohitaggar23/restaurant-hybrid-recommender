from __future__ import annotations
import math
from typing import List, Tuple
from .data import Restaurant

def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2-lat1)
    dl = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*r*math.atan2(math.sqrt(a), math.sqrt(1-a))

def nearby(restaurants: List[Restaurant], lat: float, lon: float, k: int = 5) -> List[Tuple[float, Restaurant]]:
    scored = []
    for r in restaurants:
        dist = haversine_km(lat, lon, r.latitude, r.longitude)
        scored.append((1/(1+dist), r))
    return sorted(scored, key=lambda x: x[0], reverse=True)[:k]
