from pathlib import Path


FLAGS_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
    / "assets"
    / "flags"
)
UNKNOWN_FLAG_FILENAME = "unknown.svg"

TEAM_FLAG_CODES = {
    "Algeria": "dz",
    "Argentina": "ar",
    "Australia": "au",
    "Austria": "at",
    "Belgium": "be",
    "Bosnia and Herzegovina": "ba",
    "Brazil": "br",
    "Canada": "ca",
    "Cape Verde": "cv",
    "Colombia": "co",
    "Croatia": "hr",
    "Curacao": "cw",
    "Curaçao": "cw",
    "Czechia": "cz",
    "DR Congo": "cd",
    "Ecuador": "ec",
    "Egypt": "eg",
    "England": "gb-eng",
    "France": "fr",
    "Germany": "de",
    "Ghana": "gh",
    "Haiti": "ht",
    "Iran": "ir",
    "Iraq": "iq",
    "Ivory Coast": "ci",
    "Japan": "jp",
    "Jordan": "jo",
    "Mexico": "mx",
    "Morocco": "ma",
    "Netherlands": "nl",
    "New Zealand": "nz",
    "Nigeria": "ng",
    "Norway": "no",
    "Panama": "pa",
    "Paraguay": "py",
    "Poland": "pl",
    "Portugal": "pt",
    "Qatar": "qa",
    "Russia": "ru",
    "Saudi Arabia": "sa",
    "Scotland": "gb-sct",
    "Senegal": "sn",
    "Serbia": "rs",
    "South Africa": "za",
    "South Korea": "kr",
    "Spain": "es",
    "Sweden": "se",
    "Switzerland": "ch",
    "Tunisia": "tn",
    "Turkey": "tr",
    "United States": "us",
    "Uruguay": "uy",
    "Uzbekistan": "uz",
    "Wales": "gb-wls",
}


def get_flag_code(team_name) -> str:
    return TEAM_FLAG_CODES.get(
        str(team_name),
        "unknown"
    )


def get_flag_path(team_name) -> str:
    expected_path = FLAGS_DIR / f"{get_flag_code(team_name)}.svg"

    if expected_path.exists():
        return str(expected_path)

    return str(FLAGS_DIR / UNKNOWN_FLAG_FILENAME)
