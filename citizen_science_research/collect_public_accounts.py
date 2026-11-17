"""Resumable public ID/date collection. SQLite stores progress atomically.

No authentication, private fields, profile text, or account actions are used.
Summaries always state whether the directory traversal is complete.
"""
import argparse
import hashlib
import json
import re
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class StopCollection(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def fetch(url, folder, accept, delay):
    for attempt in range(3):
        time.sleep(delay)
        record = {'url': url, 'requested_at_utc': now()}
        try:
            with urlopen(Request(url, headers={'Accept': accept, 'User-Agent': 'PublicRegistrationResearch/1.0'}), timeout=35) as response:
                raw = response.read()
                record.update(status=response.status, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
            with (folder / 'requests.jsonl').open('a') as stream:
                stream.write(json.dumps(record) + '\n')
            return raw
        except HTTPError as error:
            record.update(status=error.code)
            with (folder / 'requests.jsonl').open('a') as stream:
                stream.write(json.dumps(record) + '\n')
            if error.code < 500 or attempt == 2:
                raise StopCollection(f'HTTP {error.code} at {url}; no page skipped') from error
        except (URLError, TimeoutError) as error:
            if attempt == 2:
                raise StopCollection(f'Network failure at {url}: {error}') from error
        time.sleep(2 ** (attempt + 1))
    raise StopCollection('Retries exhausted')


def validate_zoo(data, page, seen):
    if not isinstance(data, dict) or not isinstance(data.get('users'), list):
        raise StopCollection('Missing users array; not an empty end page')
    meta = data.get('meta', {}).get('users', {})
    if meta.get('page') != page or not isinstance(meta.get('count'), int):
        raise StopCollection('Missing or unexpected pagination metadata')
    users = data['users']
    if not users:
        raise StopCollection('Unexpected empty page; completeness cannot be established')
    ids = []
    rows = []
    for user in users:
        uid = str(user.get('id', ''))
        if not uid.isdigit():
            raise StopCollection('Invalid account ID')
        try:
            date = datetime.fromisoformat(user['created_at'].replace('Z', '+00:00'))
        except (KeyError, ValueError, TypeError):
            raise StopCollection('Missing/invalid created_at')
        if not date.tzinfo or date > datetime.now(timezone.utc):
            raise StopCollection('Registration date is naive or in the future')
        ids.append(uid)
        rows.append((uid, date.isoformat(), date.year, page))
    if len(ids) != len(set(ids)) or set(ids).intersection(seen):
        raise StopCollection('Duplicate/overlapping IDs; stopped before committing page')
    next_page = meta.get('next_page')
    if next_page is not None and next_page != page + 1:
        raise StopCollection('Unexpected next-page value')
    return rows, meta


def foldit_ids(html):
    ids = list(dict.fromkeys(re.findall(r'href="/users/(\d+)"', html)))
    if not ids or 'Foldit Players' not in html:
        raise StopCollection('Player directory missing; cannot interpret as end of directory')
    last = re.search(r'href="/users\?page=(\d+)"[^>]*>\s*Last', html)
    return ids, int(last[1]) if last else None


def foldit_date(html, uid):
    # Read only the labeled Profile Started field, not activity dates or biographies.
    match = re.search(r'>\s*Started\s*</[^>]+>\s*<[^>]+>\s*([A-Za-z]+ \d{1,2}, \d{4})', html)
    if not match or not re.search(r'>\s*' + re.escape(uid) + r'\s*<', html):
        raise StopCollection(f'Missing labeled start date/player ID for Foldit account {uid}')
    date = datetime.strptime(match[1], '%B %d, %Y')
    if date.date() > datetime.now(timezone.utc).date():
        raise StopCollection('Future Foldit start date')
    return date.date().isoformat(), date.year


def run(args):
    if args.platform == 'foldit':
        raise SystemExit('Foldit robots.txt disallows /users/* and specifies Crawl-delay: 300. Automated profile collection is disabled. Obtain an official export; the parser remains available for supplied data.')
    folder = Path(args.output) / args.platform
    folder.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(folder / 'accounts.sqlite')
    db.execute('CREATE TABLE IF NOT EXISTS accounts (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, year INTEGER NOT NULL, source_page INTEGER NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
    def get(key, default=None):
        row = db.execute('SELECT value FROM state WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else default
    def put(key, value):
        db.execute('INSERT OR REPLACE INTO state VALUES (?,?)', (key, json.dumps(value)))
    status = 'running'
    error = None
    page = get('next_page', 1)
    seen = {r[0] for r in db.execute('SELECT id FROM accounts')}
    first_count = get('initial_reported_count')
    last_count = get('latest_reported_count')
    last_page = get('directory_last_page')
    def summary():
        result = {
            'platform': args.platform, 'status': status, 'updated_at_utc': now(),
            'unique_accounts_saved': db.execute('SELECT COUNT(*) FROM accounts').fetchone()[0],
            'next_page': get('next_page', 1), 'initial_reported_count': first_count,
            'latest_reported_count': last_count, 'directory_last_page': last_page,
            'error': error, 'metric': 'Public account IDs and creation/start dates; not annual active users',
            'population_coverage_verified': False,
            'limitations': ['Partial counts are not population estimates.', 'A live directory is not a frozen snapshot.',
                            'Historical deleted/spam accounts and legacy-date semantics need independent validation.'],
            'year_counts_in_downloaded_records_only': dict(db.execute('SELECT year,COUNT(*) FROM accounts GROUP BY year ORDER BY year').fetchall()),
        }
        (folder / 'status.json').write_text(json.dumps(result, indent=2))
        return result
    try:
        if get('finished', False):
            status = 'directory_traversal_finished_coverage_unverified'
            return
        summary()
        for _ in range(args.max_pages):
            if args.platform == 'zooniverse':
                url = 'https://www.zooniverse.org/api/users?' + urlencode({'page': page, 'page_size': 200, 'sort': 'id'})
                raw = fetch(url, folder, 'application/vnd.api+json; version=1', args.delay)
                try:
                    data = json.loads(raw)
                except (ValueError, UnicodeDecodeError):
                    raise StopCollection('Response is not JSON')
                rows, meta = validate_zoo(data, page, seen)
                if first_count is None:
                    first_count = meta['count']
                last_count = meta['count']
                next_page = meta['next_page']
                with db:
                    db.executemany('INSERT INTO accounts VALUES (?,?,?,?)', rows)
                    put('next_page', next_page)
                    put('initial_reported_count', first_count)
                    put('latest_reported_count', last_count)
                    if next_page is None:
                        put('finished', True)
                seen.update(r[0] for r in rows)
            else:
                url = 'https://fold.it/users?' + urlencode({'page': page})
                raw = fetch(url, folder, 'text/html', args.delay).decode('utf-8')
                ids, observed_last = foldit_ids(raw)
                if observed_last:
                    last_page = observed_last
                if last_page is None:
                    raise StopCollection('Cannot establish directory pagination')
                for uid in ids:
                    existing = db.execute('SELECT source_page FROM accounts WHERE id=?', (uid,)).fetchone()
                    if existing:
                        if existing[0] != page:
                            raise StopCollection('Foldit directory shifted/overlapped; stopped')
                        continue
                    profile = fetch('https://fold.it/users/' + uid, folder, 'text/html', args.delay).decode('utf-8')
                    date, year = foldit_date(profile, uid)
                    with db:
                        db.execute('INSERT INTO accounts VALUES (?,?,?,?)', (uid, date, year, page))
                    summary()
                next_page = page + 1 if page < last_page else None
                with db:
                    put('next_page', next_page)
                    put('directory_last_page', last_page)
                    if next_page is None:
                        put('finished', True)
            print(f'{args.platform} page={page} records={db.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]}', flush=True)
            summary()
            if next_page is None:
                status = 'directory_traversal_finished_coverage_unverified'
                if args.platform == 'zooniverse' and len(seen) != last_count:
                    status = 'directory_traversal_finished_count_mismatch'
                break
            page = next_page
        else:
            status = 'page_budget_reached_partial_resumable'
    except (StopCollection, OSError, sqlite3.Error, KeyboardInterrupt) as exc:
        status = 'stopped_partial_resumable'
        error = str(exc) or 'Interrupted'
        print(error, flush=True)
    finally:
        print(json.dumps(summary(), indent=2), flush=True)
        db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=['zooniverse', 'foldit'])
    parser.add_argument('--output', default=str(Path(__file__).parent / 'account_collection'))
    parser.add_argument('--max-pages', type=int, default=20000)
    parser.add_argument('--delay', type=float, default=1.5)
    args = parser.parse_args()
    if args.delay < 1 or args.max_pages < 1:
        parser.error('Use delay >= 1 second and max-pages >= 1')
    run(args)
