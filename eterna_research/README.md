# Eterna registration data investigation

The old file `eterna_all_users_raw_progress.csv` contains
4,939,900 rows but only 66 distinct user IDs. It cannot establish annual or
cumulative Eterna account counts. The original file is preserved.

The old collector incremented `start` but did not check whether results changed.
The public wiki documents a `search` parameter for `type=users`, but does not
document pagination for that query:
https://wiki.eternagame.org/wiki/API_for_Server_Data_Queries

## Replacement collector

`collect_users.py` defaults to a two-page test of the old `start` parameter.
It requires disjoint IDs and the requested page size before considering that
test passed. It stops on repeated IDs, malformed results, access denial,
rate limiting, invalid dates, or a page limit. Failed requests are never skipped.
Raw successful responses and a manifest record the evidence for each run.
Every run has its own directory. Account data is explicitly named partial.

Run `python3 collect_users.py` to probe. `--collect` permits bounded traversal
after the same checks; it does not prove that all historical accounts are exposed.
`--offset-param` allows testing a parameter independently once there is evidence
for it. None has been validated against the live service yet.

No annual totals are published from partial or unverified data. An empty page
after successful pagination establishes only the end of that API traversal.
Coverage requires confirmation of endpoint scope and a matching authoritative
total or an official aggregate/export. Deleted, hidden, or excluded accounts may
be absent even from an otherwise complete traversal.

With suitable data, count unique account IDs by registration year. Cumulative
counts describe registrations represented in the export. They do not establish
historical active accounts or unique people. Mark the collection year partial.

## Current blocker

Live public endpoint requests returned HTTP 403 Forbidden during this session.
No fresh population data or validated pagination has been obtained.
Next: use an accessible public account directory/export or obtain an official
yearly registration aggregate from Eterna. Do not repeat the original loop.

## Tests

`python3 -m unittest -v test_collect_users.py`

Tests cover the original repeated-page failure, overlap, invalid responses and
dates, page limits, and the distinction between traversal and population coverage.
