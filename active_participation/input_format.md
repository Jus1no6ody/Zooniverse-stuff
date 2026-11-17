# Local event input format

Python 3.10+; standard library only. Store inputs and generated outputs under
`active_participation/local_data/`, which is excluded from Git.

Each event JSONL row needs:

| Field | Meaning |
| --- | --- |
| `platform` | `zooniverse`, `eterna`, `eyewire`, or `foldit` |
| `event_id` | Stable nonempty event ID as a string, unique within that platform |
| `user_id` | Stable pseudonymous account ID as a string, or explicit `null` for an anonymous event |
| `timestamp` | ISO timestamp including a timezone; converted to UTC |
| `scientific_task` | Boolean recording whether the completed event meets the documented scientific contribution definition |

Normalize source-specific task types before running the analysis. Do not infer
contributions from signups, points without dates, leaderboard presence, or
profile visits. Only pass completed task records; explicitly flag tutorials or
other excluded events false.

The coverage file is an object with a `coverage` array containing one interval
per platform. Each entry needs `platform`, `start`, `end_exclusive`, `complete`
(boolean), `scope` (`platform`), `source`, and `task_definition`.

Set `complete` true only after validating that the export covers that entire
platform and interval. An event outside the declared interval is rejected.
Adjacent coverage segments should be normalized to one independently verified
continuous interval before import. Project-only data do not establish
platform-wide active counts and are rejected by this first analysis tool.

```sh
python3 active_participation/analyze_activity.py \
  --events active_participation/local_data/events.jsonl \
  --coverage active_participation/local_data/coverage.json \
  --output active_participation/local_data/active_accounts.json
```

The result includes full-calendar-month and full-calendar-year windows that
intersect declared coverage. `active_identified_accounts` is `null` for partial
windows or incomplete exports. Observed counts remain separately labeled and
must not be charted as platform totals. Anonymous task events are reported
separately without inventing unique participant counts. Output provenance
includes hashes of both inputs. This script assumes records fit in memory; large
exports require a streaming or database implementation before production use.
