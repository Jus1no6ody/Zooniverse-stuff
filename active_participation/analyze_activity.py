"""Count distinct contributing accounts from normalized scientific task events.

Inputs are local JSONL events and a JSON coverage manifest. No user records are
downloaded here. Complete-period totals require explicitly attested coverage.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PLATFORMS = {'zooniverse', 'eterna', 'eyewire', 'foldit'}


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamps must include a timezone')
    return parsed.astimezone(timezone.utc)


def normalize_coverage(items):
    coverage = {}
    for item in items:
        platform = item['platform']
        if platform not in PLATFORMS or platform in coverage:
            raise ValueError('Use one coverage interval per known platform')
        start, end = timestamp(item['start']), timestamp(item['end_exclusive'])
        if start >= end or type(item.get('complete')) is not bool:
            raise ValueError('Invalid coverage interval or complete flag')
        if item.get('scope') != 'platform' or not item.get('source') or not item.get('task_definition'):
            raise ValueError('Platform-wide scope, source, and task definition are required')
        coverage[platform] = {**item, 'start_dt': start, 'end_dt': end}
    return coverage


def analyze(events, coverage_items):
    coverage = normalize_coverage(coverage_items)
    observed = defaultdict(list)
    seen = {}
    duplicates = 0
    excluded = 0
    for event in events:
        platform = event['platform']
        if platform not in coverage:
            raise ValueError('Every event needs a platform coverage declaration')
        event_id = event.get('event_id')
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError('A stable nonempty event_id is required')
        if 'user_id' not in event or (event['user_id'] is not None and
                (not isinstance(event['user_id'], str) or not event['user_id'].strip())):
            raise ValueError('user_id must be a stable string or explicit null for anonymous events')
        if type(event.get('scientific_task')) is not bool:
            raise ValueError('scientific_task must be an explicit boolean')
        time = timestamp(event['timestamp'])
        interval = coverage[platform]
        if not interval['start_dt'] <= time < interval['end_dt']:
            raise ValueError('Event falls outside declared coverage')
        key = (platform, event_id)
        identity = (event['user_id'], time.isoformat(), event['scientific_task'])
        if key in seen:
            if seen[key] != identity:
                raise ValueError('Conflicting records share an event ID')
            duplicates += 1
            continue
        seen[key] = identity
        if event['scientific_task']:
            observed[platform].append((time, event['user_id']))
        else:
            excluded += 1
    output = []
    for platform, item in coverage.items():
        start, end = item['start_dt'], item['end_dt']
        windows = []
        for year in range(start.year, end.year + 1):
            ys = datetime(year, 1, 1, tzinfo=timezone.utc)
            ye = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
            if ys < end and ye > start:
                windows.append(('year', str(year), ys, ye))
            for month in range(1, 13):
                ms = datetime(year, month, 1, tzinfo=timezone.utc)
                me = datetime(year + (month == 12), month % 12 + 1, 1, tzinfo=timezone.utc)
                if ms < end and me > start:
                    windows.append(('month', f'{year}-{month:02}', ms, me))
        for grain, label, ws, we in windows:
            rows = [(t, uid) for t, uid in observed[platform] if ws <= t < we]
            accounts = {uid for _, uid in rows if uid is not None}
            anonymous = sum(uid is None for _, uid in rows)
            complete = item['complete'] and start <= ws and we <= end
            output.append({
                'platform': platform, 'period_type': grain, 'period': label,
                'period_start_utc': ws.isoformat(), 'period_end_exclusive_utc': we.isoformat(),
                'coverage_complete': complete,
                'active_identified_accounts': len(accounts) if complete else None,
                'observed_identified_accounts': len(accounts),
                'observed_scientific_events': len(rows), 'anonymous_scientific_events': anonymous,
                'source': item['source'], 'task_definition': item['task_definition'],
            })
    return {'metric': 'Distinct identified accounts with at least one scientific task in the period',
            'timezone': 'UTC', 'duplicate_event_rows_removed': duplicates,
            'non_scientific_events_excluded': excluded,
            'limitations': ['Accounts are not unique people.', 'Anonymous events cannot be converted into unique participants.',
                            'Annual active accounts are counted by union, not by summing monthly counts.',
                            'Complete coverage is a source assertion requiring independent validation.'],
            'periods': output}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--events', type=Path, required=True)
    parser.add_argument('--coverage', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.events.open() as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    result = analyze(events, json.loads(args.coverage.read_text())['coverage'])
    result['input_sha256'] = {name: hashlib.sha256(path.read_bytes()).hexdigest()
                              for name, path in [('events', args.events), ('coverage', args.coverage)]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(f'Saved {len(result["periods"])} period rows to {args.output}')


if __name__ == '__main__':
    main()
