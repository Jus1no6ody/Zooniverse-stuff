import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from collect_users import CollectionError, accept_page, run, validate_page


def user(uid):
    return {"uid": uid, "created": "Jun 01, 2026"}


class CollectorTests(unittest.TestCase):
    def test_missing_array_is_not_end_of_dataset(self):
        with self.assertRaises(CollectionError):
            validate_page({"error": "denied"})

    def test_duplicate_id_within_page(self):
        with self.assertRaises(CollectionError):
            validate_page({"data": {"users": [user(1), user(1)]}})

    def test_missing_date_is_not_silently_dropped(self):
        with self.assertRaises(CollectionError):
            validate_page({"data": {"users": [{"uid": 1}]}})

    def test_overlapping_pages_stop(self):
        seen = set()
        accept_page([user(1), user(2)], seen)
        with self.assertRaises(CollectionError):
            accept_page([user(2), user(3)], seen)

    def simulate(self, pages, collect=True, max_pages=5):
        with tempfile.TemporaryDirectory() as folder:
            args = argparse.Namespace(output=folder, offset_param="start", page_size=2,
                                      max_pages=max_pages, delay=1, collect=collect)
            offsets = []
            def fake(params, *unused):
                offsets.append(params["start"])
                return pages[len(offsets) - 1]
            with patch("collect_users.time.sleep"):
                code = run(args, fake)
            manifest = json.loads(next(Path(folder).glob("*/manifest.json")).read_text())
            return code, manifest, offsets

    def test_original_failure_stops_after_two_pages(self):
        code, manifest, offsets = self.simulate([[user(1), user(2)]] * 5)
        self.assertEqual(offsets, [0, 2])
        self.assertEqual(code, 1)
        self.assertFalse(manifest["pagination_verified"])
        self.assertEqual(manifest["unique_accounts"], 2)

    def test_disjoint_pages_then_empty_still_do_not_claim_population_coverage(self):
        code, manifest, _ = self.simulate([[user(1), user(2)], [user(3), user(4)], []])
        self.assertEqual(code, 0)
        self.assertTrue(manifest["pagination_verified"])
        self.assertFalse(manifest["population_coverage_verified"])

    def test_page_limit_is_partial(self):
        code, manifest, _ = self.simulate([[user(1), user(2)], [user(3), user(4)]], max_pages=2)
        self.assertEqual(code, 1)
        self.assertEqual(manifest["status"], "page_limit_reached_partial")


if __name__ == "__main__":
    unittest.main()
