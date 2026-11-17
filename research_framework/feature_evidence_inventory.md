# Game-inspired features: initial evidence inventory

Working question: **How do game-inspired features affect citizen-science engagement, learning, and data utility?**

This is a curated starting set, checked 17 November 2026, not a systematic review
or a completed comparison of current interfaces. Source dates and project scope
matter. A documented feature is not evidence that the feature caused an outcome.

## Feature and outcome evidence

| Platform / scope | Feature or mechanism documented | Outcome evidence reviewed | Design and permissible interpretation | Sources |
| --- | --- | --- | --- | --- |
| Eterna, historical RNA-design study | Puzzle cycles, design voting, experimental feedback, shared design rules | Community strategies and design performance improved through experimental cycles; resulting rules were tested in an algorithm | Longitudinal learning process and experimental design benchmarks. Supports task-specific learning and scientific utility; does not isolate feedback, voting, or rewards as the cause | [E1] |
| Foldit, historical recipe study | Creating, modifying, sharing, and reusing gameplay recipes | Player-developed optimization strategies were benchmarked against earlier methods | Usage analysis and computational benchmarking. Demonstrates useful strategy generation; does not estimate the causal effect of sharing on retention or general science learning | [F1] |
| EyeWire, interface described in 2014 | Points, daily/weekly/monthly leaderboard, achievements, progression, accuracy feedback | Feature implementation documented; accuracy information provides a potential quality measure | Official historical walkthrough. Confirms features at that time, not improvement caused by them or continuity into EyeWire II | [W1] |
| EyeWire, participant survey | Motivations in a gamified environment | Motivation themes and reported participation/interest in learning from a survey of 1,505 responses | Survey and thematic analysis. Self-report and selection limit causal claims. Seed entry based on indexed primary-paper abstract/methods; full-text verification remains pending | [W2] |
| Zooniverse, selected astronomy projects | Participation and opportunities to learn; no isolated game-feature intervention in this study | More engaged participants performed better on project-specific science quizzes after accounting for general science knowledge | Observational econometric analysis. Learning association, not evidence that points, badges, or a particular feature produced it | [Z1] |
| Zooniverse, configurable workflows | Correctness feedback on training subjects | Capability to deliver feedback is documented | Official implementation documentation. Project-specific exposure must be verified; an intended learning benefit is not a measured effect | [Z2] |
| Zooniverse, optional leveling framework | Gold-standard skill assessment and progression to harder workflows | Skill-based routing and progression are documented | Official implementation documentation, not an outcome evaluation. Does not mean every Zooniverse project uses levels | [Z3] |

Mechanisms such as feedback, collaboration, and scaffolding are not inherently
game mechanics. Record their specific implementation and explain why they are
classified as game-inspired in the thesis. Do not classify a whole platform as
uniformly gamified or treat a feature not found in this search as absent.

## External methodological example

[Q1] examines successive leaderboard conditions in **Quantum Moves**, outside
the four-platform sample. A leaderboard outage and subsequent implementations
enabled a comparison of player performance. It challenges a universal positive
leaderboard effect, but conditions occurred at different times rather than by
random assignment. It informs study design; it is not evidence about EyeWire,
Eterna, Foldit, or Zooniverse.

## What we can currently say

The reviewed material supports specific feature descriptions, examples of useful
scientific output, and some learning or motivation evidence. It does not support
a pooled estimate of the impact of game-inspired features across the four
platforms. User totals and the 2021 active-account snapshot remain context.

## Evidence extraction for the next papers

For each study record the platform/project, study dates, feature/version,
comparison condition, allocation method, sample and attrition, outcome instrument,
effect estimate and uncertainty, follow-up duration, task difficulty, missing data,
and confounders. Mark unreported fields unavailable. Separate measured learning
from self-reported learning and measured quality from raw contribution volume.

Use descriptive design labels—randomized comparison, nonrandomized comparison,
longitudinal observation, survey, benchmark, or feature documentation. Do not turn
these into an arbitrary numeric quality score. Assess the specific causal claim.

## Primary sources

- **[E1]** Lee et al. (2014), *RNA design rules from a massive open laboratory*, PNAS. [DOI](https://doi.org/10.1073/pnas.1313039111), [author-hosted full text](https://daslab.stanford.edu/assets/pdfs/2014_Lee_PNAS.pdf). Abstract, workflow, training and independent test sections reviewed.
- **[F1]** Khatib et al. (2011), *Algorithm discovery by protein folding game players*, PNAS. [DOI](https://doi.org/10.1073/pnas.1115898108), [author-hosted full text](https://homes.cs.washington.edu/~zoran/pnas-11.pdf). Abstract and recipe/benchmark descriptions reviewed.
- **[W1]** Amy Sterling (2014), *A Walk Through Eyewire*. [Official walkthrough](https://blog.eyewire.org/how-to-play-eyewire/). Historical feature documentation, not an intervention study.
- **[W2]** Tinati et al. (2017), *An investigation of player motivations in Eyewire, a gamified citizen science project*, Computers in Human Behavior. [DOI](https://doi.org/10.1016/j.chb.2016.12.074), [author manuscript record](https://eprints.soton.ac.uk/404286/). Indexed abstract/method excerpts reviewed; publisher and direct manuscript retrieval were blocked. Do not extract effect sizes without full-text verification.
- **[Z1]** Masters et al. (2016), *Science Learning via Participation in Online Citizen Science*. [Author manuscript and abstract](https://arxiv.org/abs/1601.05973). Abstract-level assessment; detailed model/sample extraction pending.
- **[Z2]** Zooniverse, *Feedback*. [Official documentation](https://help.zooniverse.org/next-steps/feedback/), accessed 17 November 2026. Capability description, not a historical deployment date or evaluation.
- **[Z3]** Zooniverse, *Leveling-Up framework for using volunteer skill*. [Official documentation](https://help.zooniverse.org/next-steps/leveling-up/), accessed 17 November 2026. Optional project configuration; requires gold-standard subjects and setup.
- **[Q1]** Pedersen et al. (2017), *Leaderboard Effects on Player Performance in a Citizen Science Game*. [Author manuscript and abstract](https://arxiv.org/abs/1707.03704). Abstract-level methods example outside the four platforms; detailed full-text assessment pending.
