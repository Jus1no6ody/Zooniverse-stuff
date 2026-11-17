# EyeWire and Foldit participation records

Checked 17 November 2026.

## Downloaded historical source

Strasser et al. (2023), *Quantifying online citizen science: Dynamics and demographics of public participation in science*, PLOS ONE.

- Paper: https://doi.org/10.1371/journal.pone.0293289
- Open data: https://doi.org/10.26037/yareta:lklrzxq3njdhhh4hdzt6nrwdz4
- Archive: https://yareta.unige.ch/archives/641248dc-f321-4b4e-a9b6-972535e8f6d3
- Download URL: https://access.yareta.unige.ch/access/metadata/641248dc-f321-4b4e-a9b6-972535e8f6d3/download
- License: CC BY-NC 4.0. Credit the dataset and paper when reusing it.

The unmodified signup CSV is saved under `published_data/`; download the full archive from the source URL above.
`historical_signup_review.json` contains the extracted monthly values and year-end snapshots.
`all_four_historical_series.json` preserves the monthly values for all four platforms.

The right-hand table in `S1_Signup.csv` contains separate cumulative signup series for Foldit and EyeWire, as well as Eterna and Zooniverse. Its first six rows are descriptive material. The monthly column for this table is the second column named Month; the left-hand table has a different, more sparse time axis. The extraction uses the correct right-hand dates.

Foldit's series starts in November 2007 and EyeWire's in January 2012. Both last change in December 2017, then repeat the same values through October 2019. Exclude those repeated tails from claims about growth unless the authors clarify them. The archive's overall description covers 1998–2021; this does not establish full 2021 coverage for each platform.

## What these counts measure

The paper excludes accounts with zero contributions from its participation estimates. For Foldit, it explicitly distinguishes 533,322 created accounts from 119,183 accounts that completed at least one task. Thus the Foldit series cannot be compared directly to unfiltered Panoptes user-directory totals.

These are cumulative published signup counts for the study's included accounts. They are neither total task counts nor numbers of active participants in each year. The archive's separate `S3_Active.csv` concerns SETI@home, not EyeWire or Foldit. Do not use it as an active-user series for these platforms.

December 2017 values in the signup file:

| Platform | Published cumulative signup-series count |
| --- | ---: |
| EyeWire | 266,635 |
| Foldit | 119,183 |

## EyeWire live API check

- Public documentation: https://eyewire.org/apidoc
- Official sample API repository: https://github.com/seung-lab/eyewire-public-api

The reviewed documentation focuses on neuron data, tasks, cells, meshes, and authentication. No platform-wide historical registration-count endpoint was identified in those sources. This is a limit of the search, not proof that no other endpoint exists.

The study says EyeWire data were supplied by its organizers. For an update after 2017, an organizer-provided annual/monthly aggregate is the clearest route. Ask for all registrations and contributing accounts separately, with the activity definition, date boundaries, and treatment of deleted/spam accounts. Treat original EyeWire and EyeWire II separately until account continuity is established.

## Foldit live directory check

- Public player directory: https://fold.it/users
- Inspected profile: https://fold.it/users/415886

The directory responds to an ordinary public HTTP GET. It links to paginated user pages and profiles. The inspected profile has a `Started March 28, 2012` field and separate puzzle-score activity tables. This is evidence that account start dates can be read, not validation of complete historical coverage or an annual aggregate API.

The directory's last-page link was `/users?page=102409`, with ten profiles on the first page. That is a substantial crawl, and should not be converted into an exact account count without fetching the last page and establishing scope. No full user crawl was started. An official aggregate/export is preferable for validating completeness and excluding spam consistently with the historical paper.

## Remaining work

For a comparable four-platform analysis, choose one population definition and collect it consistently. Suggested separate outcomes are all new registrations by year, new registrants who ever contributed, and annual active contributors. The historical dataset provides a useful baseline but does not supply a verified current series through 2026. Do not splice it directly onto contemporary account-directory counts.
