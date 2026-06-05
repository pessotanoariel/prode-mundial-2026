from config.translations import TEAM_TRANSLATIONS


def translate_team(team: str) -> str:
    if team is None:
        return "TBD"

    return TEAM_TRANSLATIONS.get(
        team,
        team
    )


def format_percent(value: float) -> str:
    if value is None:
        return "N/A"

    return f"{value:.0%}"
