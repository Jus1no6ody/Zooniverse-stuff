import argparse
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from collect_public_accounts import StopCollection, run, validate_zoo


def response(page, ids, next_page):
    return {'users': [{'id': str(uid), 'created_at': '2012-01-01T00:00:00Z'} for uid in ids],
            'meta': {'users': {'page': page, 'count': 4, 'next_page': next_page}}}


class CollectorTests(unittest.TestCase):
    def test_missing_users_is_not_completion(self):
        with self.assertRaises(StopCollection):
            validate_zoo({'error': 'denied'}, 1, set())

    def test_overlap_rejected(self):
        with self.assertRaises(StopCollection):
            validate_zoo(response(2, [2, 3], None), 2, {'2'})

    def test_invalid_date_rejected(self):
        data = response(1, [1, 2], 2)
        data['users'][0]['created_at'] = 'not a date'
        with self.assertRaises(StopCollection):
            validate_zoo(data, 1, set())

    def test_checkpoint_and_resume_after_failed_request(self):
        with tempfile.TemporaryDirectory() as folder:
            args = argparse.Namespace(platform='zooniverse', output=folder, max_pages=10, delay=1.5)
            with patch('collect_public_accounts.fetch', side_effect=[json.dumps(response(1, [1, 2], 2)).encode(), StopCollection('HTTP 429')]):
                run(args)
            status_path = Path(folder) / 'zooniverse/status.json'
            status = json.loads(status_path.read_text())
            self.assertEqual(status['unique_accounts_saved'], 2)
            self.assertEqual(status['next_page'], 2)
            self.assertEqual(status['status'], 'stopped_partial_resumable')
            with patch('collect_public_accounts.fetch', return_value=json.dumps(response(2, [3, 4], None)).encode()) as fetch:
                run(args)
                self.assertIn('page=2&', fetch.call_args.args[0])
            status = json.loads(status_path.read_text())
            self.assertEqual(status['unique_accounts_saved'], 4)
            self.assertEqual(status['status'], 'directory_traversal_finished_coverage_unverified')
            self.assertFalse(status['population_coverage_verified'])
            with sqlite3.connect(Path(folder) / 'zooniverse/accounts.sqlite') as db:
                self.assertEqual(db.execute('SELECT COUNT(DISTINCT id) FROM accounts').fetchone()[0], 4)

    def test_foldit_profile_crawl_disabled_before_network(self):
        with patch('collect_public_accounts.fetch') as fetch:
            with self.assertRaises(SystemExit):
                run(argparse.Namespace(platform='foldit'))
            fetch.assert_not_called()


if __name__ == '__main__':
    unittest.main()
