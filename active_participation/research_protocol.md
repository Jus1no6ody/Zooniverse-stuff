# Active participation across four citizen-science platforms

## Research question

How has the number of active contributing accounts changed over time in
Zooniverse, Eterna, EyeWire, and Foldit?

The primary outcome is the number of distinct identified accounts completing
at least one scientific task in each calendar month, in UTC. Annual active
accounts provide a secondary outcome when a complete year of activity records
is available. Count the annual union of account IDs; do not sum monthly counts.
Describe accounts as accounts, not unique people.

Compare levels and within-platform trends. Do not add the four counts to claim
a global unique-person total. Task effort differs across platforms, so task
counts per person are a separate measure with platform-specific units.

## Current evidence

| Platform | Existing material | What is still required |
| --- | --- | --- |
| Zooniverse | Yearly classification totals; account-ID/registration-date collection in progress | Platform-wide distinct contributors by month, or complete dated classification events linked to stable pseudonymous account IDs |
| Eterna | Historical signup series; 66-account biased legacy sample | Monthly unique contributors or a complete export of dated scientific contributions |
| EyeWire | Historical signup series | Monthly unique tracers or dated scientific task completions; clarify EyeWire II account continuity |
| Foldit | Historical signup series; public profile start dates | Supported monthly unique-contributor export; clarify qualifying science puzzles versus tutorials |

Registration dates cannot show whether someone contributed in a later month.
The ongoing account download is supporting material; it cannot supply the
primary outcome. ERAS classification totals measure task volume. Its documented
individual-user statistics require authorization for the user themselves or an
administrator, and user-group statistics are scoped to a group. Those routes
do not establish access to a public platform-wide active-user series.

## Verified published reference point

Strasser et al. report these active-account counts in Table 1:

| Platform | Reported active accounts |
| --- | ---: |
| Zooniverse | 20,748 |
| EyeWire | 714 |
| Eterna | 614 |
| Foldit | 465 |

The authors define activity as at least one task in a 30-day window ending in
June 2021. These are a published reference point, not an independently
reconstructed calendar-June series. Exact UTC boundaries are not established
by that description, so keep them separate from the proposed calendar-month
series. The study's task definitions and data access should be clarified before
using this point for a new trend comparison.

Source: [Strasser et al. (2023), Table 1 and Active users methods](https://doi.org/10.1371/journal.pone.0293289).
Values verified from the article's linked manuscript XML. The article is CC BY.
The historical signup archive has its own CC BY-NC 4.0 license.

## Data acquisition specification

Request a platform-wide monthly table with period boundaries, distinct active
accounts, qualifying scientific task definition, and coverage notes. Annual
distinct counts must be supplied separately if only monthly aggregates are
available. Monthly unique counts cannot recover annual unique counts.

For event exports, request only stable pseudonymous account ID, stable event
ID, timestamp with timezone, and scientific task type/status. Names, email,
biographies, and other profile details are not needed. Identify anonymous
contributions separately; do not treat each anonymous event as a new person.
Clarify tutorial/practice inclusion, incomplete attempts, staff/test/bot accounts,
deleted/spam accounts, missing periods, and any platform migrations.

Request all years available rather than imposing an arbitrary common start.
Restrict direct comparisons to shared periods with matching coverage and
definitions. Leave missing values unavailable. A fully covered period with no
contributions may be zero. A partial export or current partial month may not.

## Reproducible event analysis

`analyze_activity.py` accepts normalized local event JSONL and a coverage JSON
manifest, then writes aggregate JSON. See `input_format.md`. It deduplicates
events, rejects conflicting duplicates, normalizes timestamps to UTC, counts
accounts within each platform, and withholds population totals for incomplete
periods. Coverage assertions must be supported by source/export validation.

The tests use synthetic fixtures solely to validate the computation. They are
not research observations. No active-user time series has been generated from
the registration or task-volume data.

## Next collection step

Use the adjacent request draft to obtain official monthly aggregates or supported
exports from the four teams. The draft is not sent. Once the first activity
export arrives, document its task definition, normalize it, audit completeness,
and run the analysis. Plot and compare only supported periods. Retention,
seasonality, and explanations for growth or decline need adequate longitudinal
data and should follow, not precede, this acquisition step.

API source: [Zooniverse ERAS documentation](https://github.com/zooniverse/eras/wiki/API-Docs).
