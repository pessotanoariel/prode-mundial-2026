from pathlib import Path

from app.atlas_app.flags import get_flag_code
from app.atlas_app.flags import get_flag_path
from app.atlas_app.formatting import render_team_name
from app.atlas_app.formatting import translate_team


def test_get_flag_code_supports_special_case_teams():
    assert get_flag_code("United States") == "us"
    assert get_flag_code("South Korea") == "kr"
    assert get_flag_code("Bosnia and Herzegovina") == "ba"
    assert get_flag_code("Czechia") == "cz"
    assert get_flag_code("Cape Verde") == "cv"
    assert get_flag_code("Curacao") == "cw"
    assert get_flag_code("Curaçao") == "cw"
    assert get_flag_code("DR Congo") == "cd"
    assert get_flag_code("Ivory Coast") == "ci"
    assert get_flag_code("England") == "gb-eng"
    assert get_flag_code("Scotland") == "gb-sct"
    assert get_flag_code("Wales") == "gb-wls"


def test_get_flag_path_falls_back_to_unknown_svg():
    assert Path(get_flag_path("Unknown Team")).name == "unknown.svg"
    assert translate_team("Unknown Team") == "Unknown Team"


def test_translate_team_preserves_draw_label_without_flag():
    assert translate_team("Draw") == "Draw"


def test_render_team_name_uses_svg_asset_and_plain_team_name():
    rendered = render_team_name("Spain")

    assert "data:image/svg+xml;base64," in rendered
    assert "España" in rendered
    assert "\U0001f1ea\U0001f1f8" not in rendered
