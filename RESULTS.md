# Available results

Data inventory and descriptive results, 17 November 2026.

**The thesis focuses on active participation. We have one published active-account reference point, but no newly collected monthly active-user time series for the four platforms.** Registration series and classification totals below are supporting evidence and measure different things.

## Active participation: published 2021 reference point

The original study reports accounts completing at least one task during a 30-day window ending in June 2021. Exact UTC boundaries are not established. These values are a published snapshot, not our own current measurements or calendar-month estimates.

| Platform | Reported active accounts |
| --- | ---: |
| Zooniverse | 20,748 |
| EyeWire | 714 |
| Eterna | 614 |
| Foldit | 465 |

Source: [Strasser et al. (2023), Table 1 and methods](https://doi.org/10.1371/journal.pone.0293289). Article: CC BY. [Machine-readable reference and provenance](active_participation/published_2021_reference.json).

## Zooniverse: yearly scientific classifications

Classifications measure contributions, not distinct active accounts. The following counts were retrieved from ERAS on 17 November 2026. **2026 is a partial year and should not be compared directly with complete years.**

| Year | Classifications | Reporting period |
| --- | ---: | --- |
| 2007 | 42,518,751 | Calendar-year bucket |
| 2008 | 30,295,733 | Calendar-year bucket |
| 2009 | 13,909,368 | Calendar-year bucket |
| 2010 | 8,767,841 | Calendar-year bucket |
| 2011 | 13,004,683 | Calendar-year bucket |
| 2012 | 26,120,729 | Calendar-year bucket |
| 2013 | 39,162,399 | Calendar-year bucket |
| 2014 | 33,454,803 | Calendar-year bucket |
| 2015 | 23,603,544 | Calendar-year bucket |
| 2016 | 18,373,822 | Calendar-year bucket |
| 2017 | 60,286,395 | Calendar-year bucket |
| 2018 | 54,464,235 | Calendar-year bucket |
| 2019 | 58,868,401 | Calendar-year bucket |
| 2020 | 100,777,545 | Calendar-year bucket |
| 2021 | 88,165,326 | Calendar-year bucket |
| 2022 | 72,992,883 | Calendar-year bucket |
| 2023 | 72,297,332 | Calendar-year bucket |
| 2024 | 76,366,334 | Calendar-year bucket |
| 2025 | 86,371,817 | Calendar-year bucket |
| 2026 | 97,504,748 | Partial year |
| **Total returned** | **1,017,306,689** | **All returned buckets** |

The yearly buckets sum exactly to the API's reported total. This reconciliation checks the response arithmetic; it does not independently establish historical platform coverage.

[Raw ERAS response](zooniverse_research/eras_yearly_raw.json) · [Dated API validation](zooniverse_research/api_validation.json) · [ERAS documentation](https://zooniverse.github.io/eras/)

## Historical cumulative signup series

These are year-end values from the published study's included-account series. **They are not annual active-user counts or unfiltered totals of every account ever registered.** The study excludes zero-contribution accounts from its participation estimates.

| Year end | Zooniverse | Eterna | EyeWire | Foldit |
| --- | ---: | ---: | ---: | ---: |
| 2007 | 118,187 | — | — | 166 |
| 2008 | 168,693 | — | — | 8,898 |
| 2009 | 249,046 | 4 | — | 12,909 |
| 2010 | 365,494 | 377 | — | 28,059 |
| 2011 | 500,873 | 35,590 | — | 58,930 |
| 2012 | 733,542 | 67,131 | 22,651 | 81,451 |
| 2013 | 889,645 | 131,336 | 102,020 | 93,504 |
| 2014 | 1,250,894 | 200,982 | 170,228 | 101,157 |
| 2015 | 1,412,914 | 223,707 | 210,970 | 109,595 |
| 2016 | 1,545,652 | — | 240,741 | 113,722 |
| 2017 | 1,721,037 | — | 266,635 | 119,183 |
| 2018 | 1,847,666 | — | — | — |

“—” means no year-end value is displayed under the coverage rule; it does not mean zero participants. Unchanged trailing values after the last recorded change are withheld here pending source clarification. This is a conservative display rule, not proof of the exact date data collection ended.

The last changing monthly value is August 2019 for Zooniverse, May 2016 for Eterna, and December 2017 for EyeWire and Foldit. The complete published rows, including unchanged tails, remain available in the source files. Do not infer zero growth from those tails or splice these series onto current all-account totals.

[Published monthly values for all four platforms](citizen_science_research/all_four_historical_series.json) · [Original signup table](citizen_science_research/published_data/S1_Signup.csv) · [Dataset DOI](https://doi.org/10.26037/yareta:lklrzxq3njdhhh4hdzt6nrwdz4)

Historical source and derived signup values: Strasser, *Quantifying Online Citizen Science*, University of Geneva/Yareta, CC BY-NC 4.0.

## What remains unavailable

| Desired result | Status |
| --- | --- |
| Monthly active contributing accounts across all four platforms | Activity exports or official aggregates still needed |
| Annual distinct active accounts | Requires full-year events or separate annual unique-count aggregates; cannot sum monthly active counts |
| Participation trends through 2026 | Not established by the available reference point, signup data, or task totals |
| Completed, validated contemporary registration dataset | Not established; account-level download files remain local |

The event-analysis code has eight passing unit tests using explicitly synthetic fixtures. Test outputs are not research observations. [Research protocol](active_participation/research_protocol.md) · [Unsent activity-data request](active_participation/data_request_unsent.md)
