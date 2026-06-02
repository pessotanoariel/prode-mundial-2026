# Knockout Pipeline

This document describes how the FIFA World Cup 2026 knockout stage is simulated.

## Overview

The knockout simulation is executed through the tournament orchestrator:

```bash
python -m src.knockout.tournament
```

The pipeline generates all knockout rounds from the Round of 32 through the Final.

---

## Round of 32

1. Generate the Round of 32 bracket structure.
2. Resolve qualified teams and best third-placed teams.
3. Apply FIFA Annex C mappings.
4. Generate real matchups.

Output:

```text
data/output/round_of_32_complete.csv
```

---

## Match Simulation

For every knockout round:

1. Build stage features.
2. Generate match predictions.
3. Resolve winners.
4. Build the next round.

Outputs:

```text
features.csv
predictions.csv
winners.csv
```

---

## Tournament Flow

Round of 32

↓

Round of 16

↓

Quarterfinals

↓

Semifinals

↓

Third Place Match

↓

Final

---

## Winner Resolution

Knockout matches cannot end in a draw.

If a prediction results in a draw:

* Higher win probability advances.
* Probability gap ≥ 0.08 → Extra Time.
* Probability gap < 0.08 → Penalties.

---

## Main Components

* tournament.py
* build_next_stage.py
* stage_features.py
* stage_predictions.py
* resolve_knockout_winners.py
* annex_c.py
