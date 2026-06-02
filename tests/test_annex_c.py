from src.knockout.annex_c import (
    get_annex_c_matchups
)


def test_valid_annex_c_combination():

    groups = [
        "G",
        "J",
        "D",
        "H",
        "B",
        "A",
        "C",
        "I"
    ]

    result = get_annex_c_matchups(
        groups
    )

    assert len(result) == 8

    assert "1A" in result
    assert "1B" in result
    assert "1D" in result
    assert "1E" in result
    assert "1G" in result
    assert "1I" in result
    assert "1K" in result
    assert "1L" in result

import pytest

from src.knockout.annex_c import (
    get_annex_c_matchups
)


def test_invalid_annex_c_combination():

    groups = [
        "A",
        "B"
    ]

    with pytest.raises(ValueError):

        get_annex_c_matchups(
            groups
        )