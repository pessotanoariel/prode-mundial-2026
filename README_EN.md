# Prode Mundial 2026

Interactive World Cup Forecast Atlas for the FIFA World Cup 2026.

Built with Python, Elo Ratings, Monte Carlo simulation, Expected Goals modeling, and Streamlit.

The project started as a simple office prediction pool and evolved into a complete tournament forecasting platform capable of simulating the entire FIFA World Cup 2026, including group-stage qualification, best third-placed teams, official FIFA Annex C knockout paths, and probabilistic tournament outcomes.

---

## Atlas Experience

The project includes an editorial-style interactive Atlas that transforms simulation outputs into a digital tournament magazine.

### Included Sections

- Cover
- Atlas
- Groups
- Bracket
- Matches
- Method

Instead of presenting predictions as traditional dashboards, the Atlas organizes forecasts, standings, probabilities, and knockout projections into a narrative experience inspired by classic World Cup guides.

---

## Project Goals

- Consume and process international football datasets based on Elo Ratings.
- Generate match forecasts using team strength and recent form.
- Simulate the complete FIFA World Cup 2026.
- Determine qualification using the official 48-team format.
- Implement FIFA Annex C knockout mapping.
- Simulate all knockout rounds through the Final.
- Explore tournament outcomes through Monte Carlo simulation.
- Serve as a practical project for Python, data engineering, simulation modeling, testing, and product design.

---

## Key Features

### Forecast Engine

- Elo-based team strength
- Recent form adjustment
- Dynamic draw probability
- Expected Goals estimation
- Poisson score modeling
- Confidence scoring
- Upset risk detection

### Tournament Simulation

- Full group-stage simulation
- Group standings generation
- Best third-place qualification
- Official FIFA 2026 tournament format
- FIFA Annex C implementation
- Complete knockout simulation
- Extra-time and penalty resolution
- Tournament champion prediction

### Monte Carlo Analytics

- Stochastic score generation
- Tournament reruns
- Champion probabilities
- Most likely finals
- Team progression probabilities

### Editorial Atlas

- Interactive tournament cover
- Championship probability rankings
- Group-stage storytelling
- Third-place qualification race
- Knockout wall chart
- Match forecast archive
- Methodology guide

---

## Architecture

### Data Pipeline

```text
External Datasets
        ↓
Ingestion
        ↓
Processing
        ↓
Team Strength + Recent Form
        ↓
Match Forecasts
        ↓
Group Simulation
        ↓
Qualification
        ↓
FIFA Annex C
        ↓
Knockout Simulation
        ↓
Monte Carlo Analysis
        ↓
Atlas Experience
```

---

## Project Structure

```text
prode-mundial-2026/
│
├── app/
│   ├── atlas_app/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── data.py
│   │   ├── formatting.py
│   │   └── styles.py
│   │
│   ├── legacy_dashboard.py
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── output/
│
├── docs/
│   ├── annex_c.md
│   └── knockout_pipeline.md
│
├── src/
│   ├── analysis/
│   ├── ingestion/
│   ├── knockout/
│   ├── predictor/
│   ├── processing/
│   └── simulation/
│
├── tests/
│
├── README.md
├── README_EN.md
└── requirements.txt
```

---

## Running the Atlas

Launch the Streamlit application:

```bash
streamlit run app/streamlit_app.py
```

---

## Running Tournament Simulation

Execute the complete tournament pipeline:

```bash
python -m src.knockout.tournament
```

---

## Installation

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Testing

Run all tests:

```bash
pytest
```

Current coverage includes:

- Knockout winner resolution
- Stage construction
- FIFA Annex C implementation
- Elo updates
- Score simulation
- Probability calculations

---

## Documentation

Additional technical documentation:

- `docs/annex_c.md`
- `docs/knockout_pipeline.md`

---

## Screenshots

### Cover Page

`docs/screenshots/cover.png`

### Atlas Page

`docs/screenshots/atlas.png`

### Groups Page

`docs/screenshots/groups.png`

### Bracket Page

`docs/screenshots/bracket.png`

### Method Page

`docs/screenshots/method.png`

---

## Current Roadmap

### Simulation Improvements

- Three-team tie breakers
- Fair Play tie breakers
- FIFA Ranking tie breakers
- Dynamic Elo integration in group stage
- Probability calibration

### Product Improvements

- Interactive bracket
- Tournament timeline
- Host cities visualization
- Mobile responsiveness

### Deployment

- Streamlit Cloud deployment
- Automated data refresh
- Scheduled simulations

### Long-Term Ideas

- Next.js frontend
- Scenario explorer
- Historical World Cup mode
- Team comparison tools

---

## Disclaimer

This project is intended for educational, analytical, and entertainment purposes.

Forecasts are generated through simulation models and probabilistic methods. They do not constitute betting advice and should not be interpreted as predictions of actual future results.
