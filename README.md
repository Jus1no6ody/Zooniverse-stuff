For a mini project I am working on :).
Sub thesis

## Citizen-science participation research

Collectors, checks, and source notes for Eterna, Zooniverse, EyeWire, and Foldit.
The existing `live_zooniverse_slide.html` is retained.

### View the results

**[Open the results tables](RESULTS.md)** for the published active-account reference point, yearly Zooniverse classifications, and historical signup counts. The page labels each measure and its coverage limits. New monthly active-participation results still require activity exports.

### Primary outcome: active participation

The thesis now focuses on distinct accounts completing scientific tasks over
time. Registration records and total classifications are supporting measures.
See [the research protocol](active_participation/research_protocol.md) for the
definitions, a verified published 2021 reference point, current data gaps, and
the acquisition specification. No new platform-wide active-user series has yet
been collected. A draft data request is prepared but has not been sent.

The [event analysis tool](active_participation/analyze_activity.py) counts
monthly and annual distinct contributing accounts from supplied task records.
It keeps incomplete periods unavailable and handles anonymous events separately.
See [input instructions](active_participation/input_format.md).

```sh
python3 -m unittest discover -s active_participation -p 'test_*.py'
```

### Run the Zooniverse account collector

Requires Python 3.10 or later. It uses only the standard library.

```sh
python3 citizen_science_research/collect_public_accounts.py zooniverse
```

The collector saves public account IDs and creation dates into a local SQLite
database, with a checkpoint after every page. Run the same command to resume
after checking any recorded stopping reason. Run only one collector per output
directory. The default delay is 1.5 seconds, with 200 accounts requested per page.
A full download can take several hours. For a bounded run, add `--max-pages 10`.

Outputs are under `citizen_science_research/account_collection/zooniverse/`:

- `accounts.sqlite`: account IDs, creation timestamps, years, and source pages.
- `status.json`: progress, stopping reasons, and coverage limitations.
- `requests.jsonl`: request timestamps, URLs, and response hashes.

The collector stops on repeated IDs, invalid dates, missing pagination metadata,
HTTP access errors, or rate limits. It never skips a failed page. Account-level
outputs are excluded from Git. A complete traversal still requires checking the
API account total, legacy account dates, and the population definition.

Foldit automated profile collection is disabled because the site's crawler
rules disallow `/users/*`. EyeWire and Foldit need a supported export for a
verified current account-level series. Eterna access returned HTTP 403 during
the 17 November 2026 investigation. See `eterna_research/README.md` for its
guarded pagination probe and the repeated-download failure it addresses.

### Available aggregate data

- `zooniverse_research/eras_yearly_raw.json`: yearly classifications for
  2007–2026, retrieved on 17 November 2026. The buckets sum to the returned total.
- `zooniverse_research/api_validation.json`: dated API checks and limitations.
- `citizen_science_research/all_four_historical_series.json`: published monthly
  cumulative signup series for all four platforms, with coverage warnings.
- `citizen_science_research/historical_signup_review.json`: EyeWire/Foldit
  year-end snapshots and the complete published monthly values.
- `citizen_science_research/published_data/S1_Signup.csv`: unmodified source
  table. Its right-hand `Month` column is the date axis for platform counts.
- `citizen_science_research/findings.md`: sources, definitions, and access checks.

Classifications count contributions. Account counts do not establish unique
people or annual active users. The published study excludes zero-contribution
accounts, so its historical series must not be spliced directly onto current
all-account directory totals. EyeWire and Foldit values repeat after December
2017; those repetitions do not establish zero growth. The 2026 activity bucket
is a partial year. Partial account-download summaries are not annual population
estimates. None of the current four-platform account series is presented as a
fully validated dataset here.

### Validation

```sh
python3 -m unittest discover -s citizen_science_research -p 'test_*.py'
python3 -m unittest discover -s eterna_research -p 'test_*.py'
```

Tests cover duplicate/overlap detection, invalid responses and dates, page
limits, and checkpoint recovery after an interrupted collection.

### Sources and attribution

Strasser et al. (2023), *Quantifying online citizen science: Dynamics and
demographics of public participation in science*, PLOS ONE.

- Paper: https://doi.org/10.1371/journal.pone.0293289
- Dataset: https://doi.org/10.26037/yareta:lklrzxq3njdhhh4hdzt6nrwdz4
- Historical dataset license: CC BY-NC 4.0. The source and extracted historical
  aggregate values retain this attribution and license; no repository-wide
  license is implied for third-party material.
- ERAS: https://zooniverse.github.io/eras/
- Panoptes: https://zooniverse.github.io/panoptes/
