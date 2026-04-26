import os, unittest
from restaurant_recsys.data import load_restaurants, load_reviews
from restaurant_recsys.content import ContentRecommender
from restaurant_recsys.location import nearby
from restaurant_recsys.popularity import popularity
from restaurant_recsys.hybrid import HybridRecommender

ROOT = os.path.join(os.path.dirname(__file__), "..")

class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.restaurants = load_restaurants(os.path.join(ROOT, "data", "sample_restaurants.jsonl"))
        self.reviews = load_reviews(os.path.join(ROOT, "data", "sample_reviews.jsonl"))

    def test_content_returns_relevant_restaurant(self):
        rows = ContentRecommender(self.restaurants).recommend("spicy noodles curry", k=3)
        self.assertEqual(len(rows), 3)
        self.assertTrue(any("curry" in r.categories.lower() or "noodles" in r.categories.lower() for _, r in rows))

    def test_location_returns_nearby_result(self):
        rows = nearby(self.restaurants, 40.73, -73.99, k=3)
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(score > 0 for score, _ in rows))

    def test_popularity(self):
        rows = popularity(self.restaurants, k=3)
        self.assertGreaterEqual(len(rows), 3)

    def test_hybrid(self):
        rows = HybridRecommender(self.restaurants, self.reviews).recommend(user_id="u1", query="spicy noodles", lat=40.73, lon=-73.99)
        self.assertGreater(len(rows), 0)
        self.assertIn("name", rows[0])

if __name__ == "__main__":
    unittest.main()
