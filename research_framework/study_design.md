# Study design: engagement, learning, and data utility

## Scope and questions

The thesis examines the impact of game-inspired features, not simply platform
popularity. Eterna, Zooniverse, EyeWire, and Foldit are case settings, not four
randomly assigned treatment groups. Engagement remains an important outcome
alongside learning and data utility.

1. Which specific features are documented, for which projects and dates?
2. What evidence connects each feature to engagement, learning, or data utility?
3. Where a credible comparison exists, how large is the effect and how uncertain?
4. Are engagement gains accompanied by learning, useful data, or trade-offs?

An initial evidence map is in `feature_evidence_inventory.md`. Current material
does not establish a feature-level causal effect across the four platforms.

## Outcomes to operationalize

| Domain | Candidate primary measure | Additional measures | Interpretation constraint |
| --- | --- | --- | --- |
| Engagement | Return to a scientific task within a prespecified follow-up window after feature exposure | Weekly/monthly active accounts, time to disengagement, contributions per active account | Pick the window before analysis; logins and registrations alone are insufficient |
| Learning | Change in performance on comparable held-out knowledge or transfer tasks | Delayed retention, task-specific proficiency; self-reported learning reported separately | More points or repeated success on the same items does not independently demonstrate learning |
| Data utility | Independently validated scientific task performance | Error/completeness, accepted usable contributions, review effort, downstream suitability | More submissions, consensus agreement, or papers alone are not interchangeable with accuracy or usefulness |

These measures are candidates, not outcomes already obtained. Final selection
depends on source availability and should be fixed before estimating effects.
Preserve project-specific units and definitions. Use an independent quality
reference where possible: scoring against the same consensus used for rewards
can make apparent reward-quality associations circular.

## Exposure record

Prefer volunteer-by-project-by-period records with stable pseudonymous IDs.
For each candidate feature, obtain rollout/withdrawal timestamps, version,
eligibility and assignment rules, and actual exposure if logged. Record the
combination of features: a simultaneous interface overhaul cannot identify the
effect of one badge. Distinguish exposure from voluntary uptake, since motivated
participants may select into a feature.

The existing monthly/annual active-account tool measures one engagement component.
It does not contain feature exposure, a learning test, quality validation, or a
counterfactual, and is not an impact estimator.

## Choose a design after checking the data

| Available comparison | Possible analysis | Required checks |
| --- | --- | --- |
| Randomly assigned feature exposure | Intention-to-treat comparison of prespecified outcomes | Assignment integrity, attrition, spillovers, uncertainty and clustering |
| Rollout with a suitable comparison group | Difference-in-differences/event study | Pretrends, adoption timing, common shocks, no simultaneous relevant changes; project/task comparability |
| Single rollout with enough before/after observations | Interrupted time series, with causal claims limited by design | Seasonality, publicity, task supply/difficulty, platform outages, other changes |
| Surveys, cross-sectional logs, or unmatched platform counts | Descriptive/associational analysis | Selection, reverse causality, measurement differences; no causal impact claim |

No design is selected merely because its name sounds causal. Check its identifying
assumptions against the actual rollout and data. Learning and utility may require
a separate study design from retention. Do not force them into the same aggregate
model if they are measured on different people or periods.

## Data acquisition priorities

1. Obtain dated feature histories and eligible/exposed populations for at least
   one viable project, alongside scientific activity logs or consistent aggregates.
2. Request learning assessments and independent data-quality/utility measures
   for the same intervention or carefully document a separate sample.
3. Validate period coverage, staff/test/bot/tutorial inclusion, task difficulty,
   anonymous activity, missing observations, and account/platform migrations.
4. Prespecify outcomes and comparisons, then analyze and report uncertainty.

The first empirical milestone is **one auditable feature–outcome comparison**,
not downloading every public profile. The registration download can support
recruitment context but cannot answer the central question by itself.

## Planned thesis structure

Introduction and conceptual definitions; transparent evidence-search and
extraction methods; four case inventories; evidence for engagement; evidence for
learning; evidence for data utility and trade-offs; any feasible empirical
comparison; limitations and implications. The current inventory is a curated seed,
so a reproducible search and screening process is still needed before describing
the review as systematic.
