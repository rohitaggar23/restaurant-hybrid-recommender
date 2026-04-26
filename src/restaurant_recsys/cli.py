from __future__ import annotations
import argparse, json, os
from .data import load_restaurants, load_reviews
from .hybrid import HybridRecommender

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--restaurants", default=os.path.join(ROOT, "data", "sample_restaurants.jsonl"))
    p.add_argument("--reviews", default=os.path.join(ROOT, "data", "sample_reviews.jsonl"))
    p.add_argument("--user-id", default="u1")
    p.add_argument("--query", default="spicy noodles")
    p.add_argument("--lat", type=float, default=None)
    p.add_argument("--lon", type=float, default=None)
    p.add_argument("--city", default=None)
    args = p.parse_args(argv)
    rec = HybridRecommender(load_restaurants(args.restaurants), load_reviews(args.reviews))
    print(json.dumps(rec.recommend(user_id=args.user_id, query=args.query, lat=args.lat, lon=args.lon, city=args.city), indent=2))

if __name__ == "__main__":
    main()
