import streamlit as st

from app.atlas_app.formatting import format_percent
from app.atlas_app.formatting import translate_team


def _is_empty(df) -> bool:
    return df is None or df.empty


def _first_row(df):
    if _is_empty(df):
        return None

    return df.iloc[0]


def render_magazine_hero(
    champions_df,
    finals_df
) -> None:
    favorite = _first_row(champions_df)
    final = _first_row(finals_df)

    final_text = "Final matchup pending"

    if favorite is not None:
        favorite_team = translate_team(favorite["team"])
        favorite_probability = format_percent(favorite["probability"])
    else:
        favorite_team = "Simulation pending"
        favorite_probability = "N/A"

    if final is not None:
        final_text = (
            f"{translate_team(final['team_1'])} vs "
            f"{translate_team(final['team_2'])}"
        )

    st.markdown(
        f"""
        <section class="atlas-hero">
            <div class="atlas-kicker">World Cup Forecast Atlas 2026</div>
            <h1>World Cup<br>Forecast<br>Atlas</h1>
            <p class="atlas-deck">
                An interactive tournament magazine from the future,
                built from the current simulation outputs.
            </p>
            <div class="atlas-hero-strip">
                <div class="atlas-hero-favorite">
                    <div class="atlas-small-label">Current tournament favorite</div>
                    <div class="atlas-hero-team">{favorite_team}</div>
                    <div class="atlas-hero-percent">{favorite_probability}</div>
                </div>
                <div class="atlas-hero-final">
                    <div class="atlas-small-label">Most likely final</div>
                    <h3>{final_text}</h3>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )


def render_top_favorites(champions_df) -> None:
    st.markdown(
        '<div class="atlas-kicker">The title orbit</div>',
        unsafe_allow_html=True
    )
    st.header("Top 3 Favorites")

    if _is_empty(champions_df):
        st.info("Champion probabilities are not available yet.")
        return

    for index, row in champions_df.head(3).reset_index(drop=True).iterrows():
        st.markdown(
            f"""
            <div class="atlas-rank">
                <div class="atlas-rank-number">{index + 1:02d}</div>
                <div class="atlas-rank-team">{translate_team(row['team'])}</div>
                <div class="atlas-rank-value">{format_percent(row['probability'])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_most_likely_final(finals_df, final_predictions_df) -> None:
    st.markdown(
        '<div class="atlas-kicker">A final from the future</div>',
        unsafe_allow_html=True
    )
    st.header("Most Likely Final")

    likely_final = _first_row(finals_df)
    predicted_final = _first_row(final_predictions_df)

    if likely_final is None and predicted_final is None:
        st.info("Final outputs are not available yet.")
        return

    if likely_final is not None:
        team_1 = translate_team(likely_final["team_1"])
        team_2 = translate_team(likely_final["team_2"])
        probability = format_percent(likely_final["probability"])

        st.markdown(
            f"""
            <div class="atlas-panel atlas-panel-violet">
                <div class="atlas-small-label">Monte Carlo pairing</div>
                <h2>{team_1} vs {team_2}</h2>
                <p>{probability} of simulated finals</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if predicted_final is not None:
        winner = translate_team(predicted_final["predicted_winner"])
        score = predicted_final["predicted_score"]

        st.markdown(
            f"""
            <div class="atlas-panel">
                <div class="atlas-small-label">Current bracket final</div>
                <h3>{translate_team(predicted_final['team_1'])} vs {translate_team(predicted_final['team_2'])}</h3>
                <p>Predicted score: <strong>{score}</strong></p>
                <p>Forecast call: <strong>{winner}</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_group_dispatch_grid(
    standings_df,
    qualified_df
) -> None:
    st.markdown(
        '<div class="atlas-kicker">Group dispatches</div>',
        unsafe_allow_html=True
    )
    st.header("First-Round Field Notes")

    if _is_empty(standings_df):
        st.info("Group standings are not available yet.")
        return

    groups = sorted(standings_df["group"].dropna().unique())

    for start in range(0, len(groups), 4):
        cols = st.columns(4)

        for col, group in zip(cols, groups[start:start + 4]):
            group_standings = (
                standings_df[
                    standings_df["group"] == group
                ]
                .sort_values("position")
            )

            group_qualified = qualified_df

            if not _is_empty(qualified_df):
                group_qualified = (
                    qualified_df[
                        qualified_df["group"] == group
                    ]
                    .sort_values("position")
                )

            projected_winner = "TBD"
            qualified_names = []

            if not group_standings.empty:
                projected_winner = translate_team(
                    group_standings.iloc[0]["team"]
                )

            if not _is_empty(group_qualified):
                qualified_names = [
                    translate_team(team)
                    for team in group_qualified["team"].tolist()
                ]

            visible_qualifiers = qualified_names[:2]
            hidden_qualifiers_count = max(
                len(qualified_names) - len(visible_qualifiers),
                0
            )
            qualified_items = "".join(
                f"<li>{team}</li>"
                for team in visible_qualifiers
            )

            if hidden_qualifiers_count:
                qualified_items += (
                    f'<li class="atlas-more-qualifiers">'
                    f'+{hidden_qualifiers_count} more'
                    f'</li>'
                )

            if not qualified_items:
                qualified_items = "<li>Qualification pending</li>"

            with col:
                st.markdown(
                    f"""
                    <div class="atlas-group-card">
                        <div class="atlas-group-letter">{group}</div>
                        <div class="atlas-group-body">
                            <div>
                                <div class="atlas-small-label">Projected winner</div>
                                <h4>{projected_winner}</h4>
                            </div>
                            <div>
                                <div class="atlas-small-label">Advance watch</div>
                                <ul>{qualified_items}</ul>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def render_tournament_teaser(final_predictions_df, champions_df) -> None:
    st.markdown(
        '<div class="atlas-kicker">Tournament teaser</div>',
        unsafe_allow_html=True
    )
    st.header("The Wall Chart Begins Here")

    final = _first_row(final_predictions_df)
    champion = _first_row(champions_df)

    if final is None and champion is None:
        st.info("Tournament teaser data is not available yet.")
        return

    left_col, right_col = st.columns([2, 1])

    with left_col:
        if final is not None:
            st.markdown(
                f"""
                <div class="atlas-panel atlas-panel-red">
                    <div class="atlas-small-label">Projected final on the current bracket</div>
                    <h2>{translate_team(final['team_1'])} vs {translate_team(final['team_2'])}</h2>
                    <p>Scoreline from the engine: <strong>{final['predicted_score']}</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with right_col:
        if champion is not None:
            st.markdown(
                f"""
                <div class="atlas-panel atlas-panel-green">
                    <div class="atlas-small-label">Cover star</div>
                    <h2>{translate_team(champion['team'])}</h2>
                    <p>{format_percent(champion['probability'])} title probability</p>
                </div>
                """,
                unsafe_allow_html=True
            )
