import unittest
from analyze_activity import analyze


def coverage(complete=True, end='2025-01-01T00:00:00Z'):
    return [{'platform': 'zooniverse', 'start': '2024-01-01T00:00:00Z',
             'end_exclusive': end, 'complete': complete, 'scope': 'platform',
             'source': 'SYNTHETIC TEST FIXTURE', 'task_definition': 'Completed scientific classification'}]


def event(key, uid, date, scientific=True):
    return {'platform': 'zooniverse', 'event_id': key, 'user_id': uid,
            'timestamp': date, 'scientific_task': scientific}


class ActivityTests(unittest.TestCase):
    def period(self, result, label):
        return next(p for p in result['periods'] if p['period'] == label)

    def test_annual_union_and_monthly_counts(self):
        rows = [event('a', 'same', '2024-01-01T00:00:00Z'),
                event('b', 'same', '2024-02-01T00:00:00Z')]
        result = analyze(rows, coverage())
        self.assertEqual(self.period(result, '2024')['active_identified_accounts'], 1)
        self.assertEqual(self.period(result, '2024-01')['active_identified_accounts'], 1)
        self.assertEqual(self.period(result, '2024-03')['active_identified_accounts'], 0)

    def test_partial_period_is_unavailable_not_zero(self):
        result = analyze([], coverage(end='2024-02-15T00:00:00Z'))
        self.assertEqual(self.period(result, '2024-01')['active_identified_accounts'], 0)
        self.assertIsNone(self.period(result, '2024-02')['active_identified_accounts'])
        self.assertIsNone(self.period(result, '2024')['active_identified_accounts'])

    def test_partial_export_never_claims_complete(self):
        result = analyze([], coverage(complete=False))
        self.assertTrue(all(p['active_identified_accounts'] is None for p in result['periods']))

    def test_duplicate_events_anonymous_and_tutorials(self):
        row = event('a', 'u', '2024-01-01T00:00:00Z')
        result = analyze([row, row, event('b', None, '2024-01-01T00:00:00Z'),
                          event('c', 'tutorial-only', '2024-01-01T00:00:00Z', False)], coverage())
        january = self.period(result, '2024-01')
        self.assertEqual(january['active_identified_accounts'], 1)
        self.assertEqual(january['anonymous_scientific_events'], 1)
        self.assertEqual(january['observed_scientific_events'], 2)
        self.assertEqual(result['duplicate_event_rows_removed'], 1)

    def test_conflicting_duplicate_stops(self):
        with self.assertRaises(ValueError):
            analyze([event('a', 'u', '2024-01-01T00:00:00Z'),
                     event('a', 'v', '2024-01-01T00:00:00Z')], coverage())

    def test_timezone_normalized_before_month_assignment(self):
        result = analyze([event('a', 'u', '2024-02-01T00:30:00+09:00')], coverage())
        self.assertEqual(self.period(result, '2024-01')['active_identified_accounts'], 1)
        self.assertEqual(self.period(result, '2024-02')['active_identified_accounts'], 0)

    def test_end_boundary_exclusive(self):
        with self.assertRaises(ValueError):
            analyze([event('a', 'u', '2025-01-01T00:00:00Z')], coverage())

    def test_project_scope_cannot_claim_platform_population(self):
        item = coverage()
        item[0]['scope'] = 'project'
        with self.assertRaises(ValueError):
            analyze([], item)


if __name__ == '__main__':
    unittest.main()
