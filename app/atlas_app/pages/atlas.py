import runpy
from pathlib import Path


def render(data: dict) -> None:
    legacy_path = (
        Path(__file__)
        .resolve()
        .parents[2]
        / "legacy_dashboard.py"
    )

    runpy.run_path(str(legacy_path))

