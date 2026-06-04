# Prode Mundial 2026 — Internal Roadmap

## Current Branch

`feature/streamlit-dashboard`

---

## PHASE 1 — MVP Dashboard

Status: COMPLETED

## Completed

* [x] Elo data ingestion
* [x] Teams lookup ingestion
* [x] Latest results ingestion
* [x] Fixtures ingestion
* [x] Team strength dataset
* [x] Recent form calculation
* [x] Prediction engine
* [x] Confidence scoring
* [x] Upset risk scoring
* [x] Streamlit dashboard
* [x] Filters by confidence
* [x] Filters by upset risk
* [x] Filters by team
* [x] Filters by date
* [x] Official FIFA 2026 groups
* [x] Group filtering

---

## PHASE 2 — Tournament Simulation

Status: COMPLETED

## Group Stage

* [X] Generate group standings table
* [X] Calculate points
* [X] Calculate goals for / against
* [X] Calculate goal difference
* [X] Simulate all group matches
* [X] Determine top 2 teams
* [X] Determine best 3rd placed teams
* [X] Head-to-head tie breaker (2-team ties)
* [X] Export qualified teams dataset

## Knockout Stage

* [X] Create knockout structure dataset
* [X] Implement FIFA Annex C combinations (495 scenarios)
* [X] Build Round of 32 simulation
* [X] Build Round of 16 simulation
* [X] Build Quarterfinal simulation
* [X] Build Semifinal simulation
* [X] Build Third Place simulation
* [X] Build Final simulation
* [X] Generate champion probability

---

## PHASE 2.5 — Refactor & Stabilization

Status: COMPLETED

### Architecture

* [X] Remove duplicated knockout scripts
* [X] Create generic build_next_stage()
* [X] Centralize stage structures
* [X] Generate round_of_32_winners.csv before Round of 16
* [X] Create tournament orchestrator
* [X] Remove hardcoded match mappings
* [X] Standardize input/output paths

### Code Quality

* [X] Add validation tests
* [X] Add logging
* [X] Improve error handling
* [X] Review naming consistency

### Documentation

* [X] Update README architecture section
* [X] Document FIFA Annex C implementation
* [X] Document knockout pipeline

---

## PHASE 3 — Advanced Modeling

Status: IN PROGRESS

### Host Advantage

[X] Host advantage boost

### Dynamic Elo System

[X] Create Elo update engine
[X] Add Elo update tests
[X] Create dynamic ratings lookup
[X] Update ratings after simulated matches
[X] Prepare feature generation for dynamic ratings
[X] Integrate ratings lookup into tournament pipeline
[X] Create stage ratings updater
[X] Integrate dynamic Elo into knockout stages

### Score Modeling

[X] Decouple score prediction from winner prediction
[X] Create Expected Goals Model
[X] Create Poisson Probability Model
[X] Integrate Poisson into score prediction
[X] Align score prediction with winner prediction
[X] Export tournament champion

### Tournament Simulation

[X] Create stochastic Poisson sampler
[X] Create stochastic score simulator
[X] Route simulation_mode through pipeline
[X] Enable stochastic score generation
[X] Derive winner from simulated score
[X] Resolve simulated knockout draws
[X] Monte Carlo tournament simulation
[X] Champion probability table
[X] Most likely finals
[X] Team progression probabilities

[ ] Integrate dynamic Elo into group stage
[ ] Validate Elo evolution across tournament

### Existing Model Improvements

[X] Validate form weighting
[ ] Upset calibration tuning

### FIFA Rules Backlog

* [ ] Head-to-head tie breaker (3+ team ties)
* [ ] Fair Play tie breaker
* [ ] FIFA Ranking tie breaker

### Future Improvement

[ ] Track actual finalists instead of final winners

---

## PHASE 4 — UX / Product

Status: FUTURE

## Dashboard Improvements

* [ ] Group tabs
* [ ] Cards instead of plain table
* [ ] Bracket visualization
* [ ] Tournament timeline
* [ ] Match cards
* [ ] Retro World Cup styling
* [ ] Mobile responsiveness

## Visual Features

* [ ] Flags support
* [ ] Stadium visualization
* [ ] Host cities
* [ ] Heatmaps
* [ ] Charts and analytics

---

## PHASE 5 — Deployment

Status: FUTURE

## Infrastructure

* [ ] Streamlit Cloud deployment
* [ ] Environment configs
* [ ] Scheduled automatic data refresh
* [ ] Logging system

## Frontend Evolution

* [ ] Next.js frontend
* [ ] API layer
* [ ] Vercel deployment
* [ ] Public domain

---

## PHASE 6 — Community / Game Features

Status: IDEAS

* [ ] User predictions
* [ ] IA vs users
* [ ] Leaderboards
* [ ] Shareable predictions
* [ ] Daily simulations
* [ ] Historical World Cup mode
* [ ] Alternate universe simulations

---

## Notes

* Current focus: build solid tournament simulation core.
* Avoid premature frontend complexity.
* Prioritize simulation correctness over visuals.
* Streamlit remains the main prototype environment.
