# FIFA Three-Team Group Tiebreak Implementation

Status: Implemented in v1.0

## Mini-Table Approach

When three or more teams finish level on overall group points, FIFA rules apply head-to-head criteria using only matches played between the tied teams.

The implementation builds a mini-table for the tied teams and computes:

1. Head-to-head points
2. Head-to-head goal difference
3. Head-to-head goals scored

These values are calculated only from matches where both teams are part of the tied set.

## Criteria Order Implemented

The group ordering now follows this sequence:

1. Overall group points
2. If exactly two teams are tied, preserve the existing direct head-to-head behavior
3. If three or more teams are tied, build a tied-team mini-table
4. Apply mini-table head-to-head points
5. Apply mini-table head-to-head goal difference
6. Apply mini-table head-to-head goals scored
7. If this resolves some teams but leaves others tied, rebuild the mini-table only among the remaining tied teams and reapply the head-to-head criteria
8. If teams are still tied after head-to-head reapplication, fall back to current overall group metrics:
   - overall goal difference
   - overall goals scored
9. If teams are still tied after every currently implemented football criterion, use final deterministic fallback using Elo rating

Fair Play points and FIFA Ranking are intentionally not implemented yet.

## Final Deterministic Fallback Using Elo Rating

Fair Play points are not currently modeled in the project, and FIFA Ranking is not currently part of the group standings pipeline. To avoid unstable ordering when all implemented football criteria are tied, the standings builder uses Elo rating as a final deterministic fallback.

This is not labeled as FIFA Ranking and should not be interpreted as a replacement for the official FIFA criteria. It is only used after:

1. Overall group points
2. Head-to-head or tied-team mini-table criteria
3. Overall goal difference
4. Overall goals scored

If Elo ratings are also tied or unavailable, team name is used as the final stable ordering key so exports remain deterministic.

## Test Coverage

The test suite covers:

- A three-team tie fully resolved by head-to-head points
- A three-team tie resolved by head-to-head goal difference
- A three-team tie resolved by head-to-head goals scored
- A partial resolution where remaining tied teams require head-to-head criteria to be reapplied
- A two-team tie regression case where direct head-to-head still overrides overall goal difference
- A tie that remains unresolved after all football criteria and is resolved by Elo rating
- Deterministic ordering when Elo ratings also match
- A regression case proving overall goal difference remains ahead of the Elo fallback

The tests use synthetic standings and match results so the tiebreak behavior is isolated from the current tournament data.

This implementation is considered complete for Version 1.
Future versions may add Fair Play and FIFA Ranking criteria if disciplinary data becomes available.
