# Prode Mundial 2026 — Internal Roadmap

---

## Current Branch

`feature/automation`

---

## PHASE 1 — MVP Dashboard

Status: COMPLETED

### Completed

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

### Group Stage

* [x] Generate group standings table
* [x] Calculate points
* [x] Calculate goals for / against
* [x] Calculate goal difference
* [x] Simulate all group matches
* [x] Determine top 2 teams
* [x] Determine best 3rd placed teams
* [x] Head-to-head tie breaker (2-team ties)
* [x] Export qualified teams dataset

### Knockout Stage

* [x] Create knockout structure dataset
* [x] Implement FIFA Annex C combinations (495 scenarios)
* [x] Build Round of 32 simulation
* [x] Build Round of 16 simulation
* [x] Build Quarterfinal simulation
* [x] Build Semifinal simulation
* [x] Build Third Place simulation
* [x] Build Final simulation
* [x] Generate champion probability

---

## PHASE 2.5 — Refactor & Stabilization

Status: COMPLETED

### Architecture

* [x] Remove duplicated knockout scripts
* [x] Create generic build_next_stage()
* [x] Centralize stage structures
* [x] Generate round_of_32_winners.csv before Round of 16
* [x] Create tournament orchestrator
* [x] Remove hardcoded match mappings
* [x] Standardize input/output paths

### Code Quality

* [x] Add validation tests
* [x] Add logging
* [x] Improve error handling
* [x] Review naming consistency

### Documentation

* [x] Update README architecture section
* [x] Document FIFA Annex C implementation
* [x] Document knockout pipeline

---

## PHASE 3 — Advanced Modeling

Status: COMPLETED

### Host Advantage

* [x] Host advantage boost

### Dynamic Elo System

* [x] Create Elo update engine
* [x] Add Elo update tests
* [x] Create dynamic ratings lookup
* [x] Update ratings after simulated matches
* [x] Prepare feature generation for dynamic ratings
* [x] Integrate ratings lookup into tournament pipeline
* [x] Create stage ratings updater
* [x] Integrate dynamic Elo into knockout stages

### Score Modeling

* [x] Decouple score prediction from winner prediction
* [x] Create Expected Goals Model
* [x] Create Poisson Probability Model
* [x] Integrate Poisson into score prediction
* [x] Align score prediction with winner prediction
* [x] Export tournament champion
* [x] Validate form weighting

### Tournament Simulation

* [x] Create stochastic Poisson sampler
* [x] Create stochastic score simulator
* [x] Route simulation_mode through pipeline
* [x] Enable stochastic score generation
* [x] Derive winner from simulated score
* [x] Resolve simulated knockout draws
* [x] Monte Carlo tournament simulation
* [x] Champion probability table
* [x] Most likely finals
* [x] Team progression probabilities

---

## PHASE 4 — Editorial Atlas Experience

Status: COMPLETED

### Editorial Product

* [x] Editorial Cover page
* [x] Tournament Atlas page
* [x] Groups magazine section
* [x] Knockout wall chart
* [x] Match archive
* [x] Methodology section
* [x] Unified navigation
* [x] Editorial visual system
* [x] Spanish localization
* [x] Responsive desktop experience

### Visual Storytelling

* [x] Champion probability narratives
* [x] Most likely final visualization
* [x] Group qualification storytelling
* [x] Third-place qualification race
* [x] Knockout path visualization
* [x] Editorial tournament notes

---

## PHASE 5 — Release Preparation

Status: COMPLETED

### Documentation Review

* [x] Rewrite README
* [x] Create screenshots gallery
* [x] Document simulation methodology
* [x] Create installation guide

### Quality Assurance

* [x] Verify FIFA Annex C outputs
* [x] Verify progression probabilities
* [x] Verify champion probabilities
* [x] Review translations and editorial copy

### Deployment

* [x] Streamlit Cloud deployment
* [x] Production configuration
* [x] Public URL

### Post-Release Backlog

* [ ] Refresh architecture diagrams
* [ ] Environment variables

---

## PHASE 6 — Automation & Operations

Status: COMPLETED

### Pipeline Automation

* [X] Full tournament regression test
* [X] Create end-to-end pipeline orchestrator
* [X] Create single-command execution flow
* [X] Validate full pipeline execution
* [X] Standardize pipeline logging

### Data Refresh

* [X] Automate Elo updates
* [X] Automate fixtures updates
* [X] Automate results ingestion
* [X] Automate feature generation

### Simulation Refresh

* [X] Automate predictions generation
* [X] Automate tournament simulation
* [X] Automate Monte Carlo execution
* [X] Regenerate Atlas datasets

### Deployment Automation

* [X] GitHub Actions workflow
* [X] Scheduled daily execution

### Monitoring

* [X] Execution reports
* [X] Data freshness validation

---

## PHASE 7 — Simulation Improvements

Status: IN PROGRESS

### FIFA Rules

* [ ] Head-to-head tie breaker (3+ team ties)
* [ ] Fair Play tie breaker
* [ ] FIFA Ranking tie breaker

### Model Improvements

* [X] Dynamic Elo in group stage
* [x] Generalized Elo match updates
* [x] Finalist tracking
* [x] Finalist probability export
* [ ] Upset calibration tuning
* [ ] Track actual finalists instead of final winners
* [ ] Validate Elo evolution across tournament
* [ ] Hybrid tournament simulation
* [ ] Correct knockout progression probabilities
* [ ] Probability calibration

### Tournament Analytics

* [ ] Team path analysis
* [ ] Elimination probability analysis
* [ ] Scenario explorer
* [ ] Sensitivity testing

---

## PHASE 8 — Product Expansion

Status: IDEAS

### Product Features

* [ ] Interactive bracket
* [ ] Tournament timeline
* [ ] Flags support
* [ ] Stadium information
* [ ] Host city profiles

### Community Features

* [ ] User predictions
* [ ] Leaderboards
* [ ] Shareable forecasts
* [ ] AI vs user predictions

### Long-Term Platform

* [ ] Next.js frontend
* [ ] API layer
* [ ] Vercel deployment
* [ ] Public domain

---

### Notes

* Simulation engine is considered feature-complete for v1.
* Editorial Atlas experience is considered complete for v1.
* Current priority is automation, operational stability, and data refresh workflows.
* Streamlit remains the primary platform for v1.
* Future work should prioritize simulation correctness over new visual features.
* Next.js remains a possible long-term evolution, not a short-term priority.
