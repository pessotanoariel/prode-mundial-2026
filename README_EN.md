# ⚠️ README_EN pending update

Current implementation includes:

- Full World Cup 2026 simulation
- FIFA Annex C implementation
- Dynamic Elo ratings
- Poisson score model
- Monte Carlo tournament simulation
- Streamlit dashboard

## Prode Mundial 2026 Predictor

A modular football prediction pipeline built for the FIFA World Cup 2026.

The project consumes live Elo-based football datasets, processes international team statistics, and generates automated match predictions for World Cup fixtures.

Initially created as a hobby side-project for a workplace betting pool ("prode"), the project evolved into a small-scale sports analytics and data engineering experiment.

---

## Features

## Current MVP

- External football dataset ingestion
- Automated TSV → CSV pipelines
- Team strength dataset generation
- World Cup fixture filtering
- Hybrid Elo-based prediction engine
- Match winner prediction
- Basic score prediction
- Confidence classification

---

## Project Structure

```text
project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── output/
│
├── src/
│   ├── ingestion/
│   ├── processing/
│   └── predictor/
│
├── requirements.txt
└── README.md
```

---

## Data Sources

The project currently uses public datasets from:

- World Football Elo Ratings
- TSV endpoints discovered through browser network inspection

Main datasets:

| Dataset | Purpose |

|---|---|

| `World.tsv` | Global Elo rankings and team statistics |
| `en.teams.tsv` | Team name lookup |
| `fixtures.tsv` | Upcoming fixtures and Elo probabilities |
| `latest.tsv` | Recent international match results |

---

## Pipeline Overview

```text
External TSV datasets
        ↓
Ingestion scripts
        ↓
Raw CSV storage
        ↓
Processing & feature engineering
        ↓
Prediction engine
        ↓
World Cup predictions
```

---

## Current Prediction Logic

The current MVP uses a hybrid heuristic model based on:

- Elo expected win probability
- Dynamic draw probability
- Relative team strength
- Simple confidence rules

Example:

| Match | Prediction |

|---|---|

| Brazil vs Morocco | Brazil 2-0 |
| Japan vs Netherlands | Draw 1-1 |
| Argentina vs Algeria | Argentina 2-1 |

---

## How To Run

## 1. Create virtual environment

```bash
python -m venv .venv
```

## 2. Activate environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run Data Ingestion

```bash
python -m src.ingestion.update_elo
python -m src.ingestion.update_teams
python -m src.ingestion.update_fixtures
python -m src.ingestion.update_latest_results
```

---

## Run Processing

```bash
python -m src.processing.build_team_strength
python -m src.processing.build_upcoming_matches
```

---

## Generate Predictions

```bash
python -m src.predictor.generate_predictions
```

Predictions are exported to:

```text
data/output/predictions.csv
```

---

## Example Output

| Match | Predicted Winner | Score | Confidence |

|---|---|---|---|

| Brazil vs Morocco | Brazil | 2-0 | High |
| Australia vs Turkey | Turkey | 1-2 | Medium |
| Japan vs Netherlands | Draw | 1-1 | Low |

---

## Roadmap

## Near-Term Improvements

### V1.1 — Recent Form Adjustment

- Last 5 matches
- Momentum score
- Recent win/loss streaks

### V1.2 — Better Score Simulation

- Poisson goal distribution
- Expected goals estimation

### V1.3 — Group Stage Simulation

- Group standings
- Qualification probabilities
- Tournament progression

---

## Mid-Term Improvements

### Monte Carlo Tournament Simulation

- 1000+ tournament runs
- Champion probabilities
- Upset simulations

### Streamlit Dashboard

- Match explorer
- Prediction viewer
- Team analytics

---

## Long-Term Ideas

### ML-Based Predictor

- Historical match training datasets
- Feature engineering
- Ensemble models
- Automated calibration

---

## Technical Notes

This project intentionally prioritizes:

- reproducibility
- modular pipelines
- simple architecture
- incremental experimentation

over heavy ML complexity in early stages.

---

## Disclaimer

Predictions are experimental and intended for educational and entertainment purposes only.
