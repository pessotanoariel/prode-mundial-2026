from app.atlas_app.components.groups import render_editorial_hero
from app.atlas_app.components.groups import render_group_dispatch_grid
from app.atlas_app.components.groups import render_group_spreads
from app.atlas_app.components.groups import render_qualification_notes
from app.atlas_app.components.groups import render_third_place_race


def render(data: dict) -> None:
    groups_df = data.get("groups")
    standings_df = data.get("standings")
    qualified_df = data.get("qualified")
    predictions_df = data.get("predictions")

    render_editorial_hero(
        groups_df,
        standings_df,
        qualified_df
    )

    render_group_dispatch_grid(
        groups_df,
        standings_df,
        qualified_df
    )

    render_group_spreads(
        groups_df,
        standings_df,
        qualified_df,
        predictions_df
    )

    render_third_place_race(
        standings_df
    )

    render_qualification_notes(
        standings_df
    )
