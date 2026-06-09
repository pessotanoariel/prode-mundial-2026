from app.atlas_app.components.bracket import render_final_poster
from app.atlas_app.components.bracket import render_knockout_notes
from app.atlas_app.components.bracket import render_knockout_overview
from app.atlas_app.components.bracket import render_third_place_match
from app.atlas_app.components.bracket import render_wall_chart
from app.atlas_app.venues import enrich_matches_with_venues


def render(data: dict) -> None:
    rounds = {
        "round_of_32": enrich_matches_with_venues(
            data.get("round_of_32"),
            "round_of_32"
        ),
        "round_of_16": enrich_matches_with_venues(
            data.get("round_of_16"),
            "round_of_16"
        ),
        "quarterfinals": enrich_matches_with_venues(
            data.get("quarterfinals"),
            "quarterfinals"
        ),
        "semifinals": enrich_matches_with_venues(
            data.get("semifinals"),
            "semifinals"
        ),
        "final": enrich_matches_with_venues(
            data.get("final"),
            "final"
        ),
    }
    final_df = rounds["final"]
    third_place_df = enrich_matches_with_venues(
        data.get("third_place"),
        "third_place"
    )

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
