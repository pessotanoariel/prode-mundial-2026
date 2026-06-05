from app.atlas_app.components.bracket import render_final_poster
from app.atlas_app.components.bracket import render_knockout_notes
from app.atlas_app.components.bracket import render_knockout_overview
from app.atlas_app.components.bracket import render_third_place_match
from app.atlas_app.components.bracket import render_wall_chart


def render(data: dict) -> None:
    rounds = {
        "round_of_32": data.get("round_of_32"),
        "round_of_16": data.get("round_of_16"),
        "quarterfinals": data.get("quarterfinals"),
        "semifinals": data.get("semifinals"),
        "final": data.get("final"),
    }
    final_df = data.get("final")
    third_place_df = data.get("third_place")

    render_knockout_overview(
        final_df,
        rounds
    )

    render_wall_chart(
        rounds
    )

    render_final_poster(
        final_df
    )

    render_third_place_match(
        third_place_df
    )

    render_knockout_notes(
        rounds,
        final_df
    )
