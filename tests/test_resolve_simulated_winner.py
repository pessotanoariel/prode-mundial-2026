from src.simulation.resolve_simulated_winner import (
    resolve_simulated_winner
)


def test_home_win():

    winner = resolve_simulated_winner(
        "France",
        "Spain",
        2,
        1
    )

    assert winner == "France"


def test_away_win():

    winner = resolve_simulated_winner(
        "France",
        "Spain",
        1,
        2
    )

    assert winner == "Spain"


def test_draw_resolution():

    winner = resolve_simulated_winner(
        "France",
        "Spain",
        1,
        1
    )

    assert winner in [
        "France",
        "Spain"
    ]