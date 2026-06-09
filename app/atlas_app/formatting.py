from base64 import b64encode
from html import escape
from pathlib import Path

from config.translations import TEAM_TRANSLATIONS

from app.atlas_app.flags import get_flag_path


NON_TEAM_VALUES = {
    "Draw",
    "Empate",
    "Pendiente",
}


def translate_team(team: str) -> str:
    if team is None:
        return "Pendiente"

    if team in NON_TEAM_VALUES:
        return TEAM_TRANSLATIONS.get(
            team,
            team
        )

    translated_team = TEAM_TRANSLATIONS.get(
        team,
        team
    )

    return translated_team


def _svg_data_uri(path: str) -> str:
    flag_path = Path(path)
    encoded_svg = b64encode(
        flag_path.read_bytes()
    ).decode("ascii")

    return f"data:image/svg+xml;base64,{encoded_svg}"


def render_team_name(team: str) -> str:
    translated_team = translate_team(team)

    if team is None or translated_team in NON_TEAM_VALUES:
        return escape(translated_team)

    flag_uri = _svg_data_uri(
        get_flag_path(team)
    )

    return (
        '<span class="atlas-team-name">'
        f'<img class="atlas-team-flag" src="{flag_uri}" alt="" loading="lazy">'
        f'<span>{escape(translated_team)}</span>'
        '</span>'
    )


def format_percent(value: float) -> str:
    if value is None:
        return "N/A"

    return f"{value:.0%}"
