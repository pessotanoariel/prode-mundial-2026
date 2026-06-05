from config.translations import TEAM_TRANSLATIONS


def translate_team(team: str) -> str:
    return TEAM_TRANSLATIONS.get(
        team,
        team
    )


def format_percent(value: float) -> str:
    return f"{value:.0%}"

