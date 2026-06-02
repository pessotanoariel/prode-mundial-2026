# FIFA Annex C Implementation

## Overview

The FIFA World Cup 2026 introduces a 48-team format with 12 groups.

The knockout stage includes:

* 12 group winners
* 12 group runners-up
* 8 best third-placed teams

This creates multiple possible Round of 32 bracket configurations.

FIFA defines these configurations in Annex C of the tournament regulations.

---

## Problem

The Round of 32 bracket cannot be generated using fixed pairings.

The opponents of several group winners depend on which groups provide the best third-placed teams.

For example:

```text
1A vs Best Third Place Team
```

The actual opponent depends on the specific combination of qualifying third-placed teams.

---

## Solution

The project implements the official FIFA Annex C mapping table.

Input:

```python
[
    "A",
    "B",
    "C",
    "D",
    "G",
    "H",
    "I",
    "J"
]
```

Output:

```python
{
    "1A": "3A",
    "1B": "3J",
    ...
}
```

---

## Data Source

The mapping table is stored in:

```text
data/raw/annex_c.xlsx
```

Each row represents one valid combination of best third-placed groups.

---

## Implementation

Main module:

```text
src/knockout/annex_c.py
```

Key function:

```python
get_annex_c_matchups(best_third_groups)
```

Steps:

1. Sort qualifying groups.
2. Build a combination key.
3. Search the Annex C table.
4. Return the official FIFA mapping.

---

## Validation

The implementation includes automated tests that verify:

* Valid combinations return mappings.
* Invalid combinations raise exceptions.
* All Round of 32 assignments are generated dynamically.

---

## Integration

The Annex C mapping is applied during:

```text
build_round_of_32_complete.py
```

before the knockout simulation begins.

The resulting fixture is exported to:

```text
data/output/round_of_32_complete.csv
```
