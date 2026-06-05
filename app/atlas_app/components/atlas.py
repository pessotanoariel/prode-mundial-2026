from collections import Counter

import streamlit as st

from app.atlas_app.formatting import format_percent
from app.atlas_app.formatting import translate_team


def _is_empty(df) -> bool:
    return df is None or df.empty


def _first_row(df):
    if _is_empty(df):
        return None

    return df.iloc[0]


def _probability_width(value: float, max_value: float) -> int:
    if not max_value:
        return 0

    return max(
        int((value / max_value) * 100),
        3
    )


def render_editorial_hero(
    champions_df,
    finals_df
) -> None:
    favorite = _first_row(champions_df)
    final = _first_row(finals_df)

    favorite_team = "Simulation pending"
    favorite_probability = "N/A"
    final_text = "Final matchup pending"

    if favorite is not None:
        favorite_team = translate_team(favorite["team"])
        favorite_probability = format_percent(favorite["probability"])

    if final is not None:
        final_text = (
            f"{translate_team(final['team_1'])} vs "
            f"{translate_team(final['team_2'])}"
        )

    st.markdown(
        f"""
        <section class="atlas-analysis-hero">
            <div class="atlas-kicker">02 / Tournament Atlas</div>
            <h1>The Shape of the Forecast</h1>
            <p>
                The analytical center of the magazine: title gravity,
                projected finals, and the teams gathering momentum.
            </p>
            <div class="atlas-analysis-hero-grid">
                <div>
                    <div class="atlas-small-label">Current favorite</div>
                    <div class="atlas-analysis-team">{favorite_team}</div>
                    <div class="atlas-analysis-percent">{favorite_probability}</div>
                </div>
                <div>
                    <div class="atlas-small-label">Most likely final</div>
                    <h3>{final_text}</h3>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )


def render_championship_orbit(champions_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">01</div>',
        unsafe_allow_html=True
    )
    st.header("Championship Orbit")

    if _is_empty(champions_df):
        st.info("Champion probabilities are not available yet.")
        return

    top_10 = champions_df.head(10).reset_index(drop=True)
    max_probability = top_10["probability"].max()

    for index, row in top_10.iterrows():
        width = _probability_width(
            row["probability"],
            max_probability
        )

        st.markdown(
            f"""
            <div class="atlas-orbit-row">
                <div class="atlas-orbit-rank">{index + 1:02d}</div>
                <div class="atlas-orbit-body">
                    <div class="atlas-orbit-topline">
                        <span>{translate_team(row['team'])}</span>
                        <strong>{format_percent(row['probability'])}</strong>
                    </div>
                    <div class="atlas-orbit-track">
                        <div class="atlas-orbit-bar" style="width: {width}%"></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_finals_from_future(finals_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">02</div>',
        unsafe_allow_html=True
    )
    st.header("Finals From The Future")

    if _is_empty(finals_df):
        st.info("Most likely finals are not available yet.")
        return

    top_finals = finals_df.head(6).reset_index(drop=True)

    for start in range(0, len(top_finals), 3):
        cols = st.columns(3)

        for offset, (col, (_, row)) in enumerate(
            zip(cols, top_finals.iloc[start:start + 3].iterrows())
        ):
            with col:
                st.markdown(
                    f"""
                    <article class="atlas-final-card">
                        <div class="atlas-small-label">Projected final #{start + offset + 1}</div>
                        <h3>{translate_team(row['team_1'])}<br>vs<br>{translate_team(row['team_2'])}</h3>
                        <p>{format_percent(row['probability'])} of simulated finals</p>
                    </article>
                    """,
                    unsafe_allow_html=True
                )


def render_contenders_and_challengers(champions_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">03</div>',
        unsafe_allow_html=True
    )
    st.header("Contenders And Challengers")

    if _is_empty(champions_df):
        st.info("Contender data is not available yet.")
        return

    contenders = champions_df.head(3)
    challengers = champions_df.iloc[3:8]

    contenders_col, challengers_col = st.columns(2)

    with contenders_col:
        st.markdown(
            '<div class="atlas-kicker">Title favorites</div>',
            unsafe_allow_html=True
        )

        for _, row in contenders.iterrows():
            st.markdown(
                f"""
                <div class="atlas-tier-row">
                    <strong>{translate_team(row['team'])}</strong>
                    <span>{format_percent(row['probability'])}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    with challengers_col:
        st.markdown(
            '<div class="atlas-kicker">Second tier</div>',
            unsafe_allow_html=True
        )

        if challengers.empty:
            st.caption("No challenger tier available yet.")
            return

        for _, row in challengers.iterrows():
            st.markdown(
                f"""
                <div class="atlas-tier-row atlas-tier-row-muted">
                    <strong>{translate_team(row['team'])}</strong>
                    <span>{format_percent(row['probability'])}</span>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_tournament_narrative(
    champions_df,
    finals_df,
    progression_df,
    final_predictions_df
) -> None:
    st.markdown(
        '<div class="atlas-section-number">04</div>',
        unsafe_allow_html=True
    )
    st.header("Tournament Narrative")

    notes = []
    favorite = _first_row(champions_df)

    if favorite is not None:
        notes.append(
            f"{translate_team(favorite['team'])} enters as the simulation favorite at {format_percent(favorite['probability'])}."
        )

    if not _is_empty(champions_df) and len(champions_df) > 1:
        second = champions_df.iloc[1]
        notes.append(
            f"{translate_team(second['team'])} remains within striking distance at {format_percent(second['probability'])}."
        )

    if not _is_empty(finals_df):
        teams = Counter()

        for _, row in finals_df.head(10).iterrows():
            teams[row["team_1"]] += 1
            teams[row["team_2"]] += 1

        recurring_team, appearances = teams.most_common(1)[0]
        notes.append(
            f"{translate_team(recurring_team)} appears in {appearances} of the ten most common projected finals."
        )

    if not _is_empty(progression_df):
        finalist = (
            progression_df
            .sort_values("final", ascending=False)
            .iloc[0]
        )
        notes.append(
            f"{translate_team(finalist['team'])} owns the strongest current final-reaching profile at {format_percent(finalist['final'])}."
        )

    final = _first_row(final_predictions_df)

    if final is not None:
        notes.append(
            f"The current bracket path lands on {translate_team(final['team_1'])} vs {translate_team(final['team_2'])}."
        )

    if not notes:
        st.info("Narrative outputs are not available yet.")
        return

    for note in notes[:5]:
        st.markdown(
            f"""
            <div class="atlas-narrative-note">
                {note}
            </div>
            """,
            unsafe_allow_html=True
        )


def render_forecast_notes() -> None:
    st.markdown(
        '<div class="atlas-section-number">05</div>',
        unsafe_allow_html=True
    )
    st.header("Forecast Notes")
    st.markdown(
        """
        <div class="atlas-forecast-note">
            These readings come from the current forecast outputs:
            champion probabilities, likely finals, progression probabilities
            when available, and the latest simulated final. They are a
            tournament simulation layer for exploration and storytelling,
            not betting advice or live-score coverage.
        </div>
        """,
        unsafe_allow_html=True
    )
