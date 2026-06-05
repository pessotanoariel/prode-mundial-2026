from collections import Counter
from html import escape
from textwrap import dedent

import pandas as pd
import streamlit as st

from app.atlas_app.formatting import translate_team


ROUND_LABELS = [
    ("round_of_32", "Dieciseisavos"),
    ("round_of_16", "Octavos"),
    ("quarterfinals", "Cuartos"),
    ("semifinals", "Semifinales"),
    ("final", "Final"),
]


def _is_empty(df) -> bool:
    return df is None or df.empty


def _html(markup: str) -> str:
    return "\n".join(
        line.strip()
        for line in dedent(markup)
        .strip()
        .splitlines()
    )


def _team(team: str) -> str:
    return escape(
        translate_team(team)
    )


def _first_row(df):
    if _is_empty(df):
        return None

    return df.iloc[0]


def _forecast_winner(row) -> str:
    winner = row["predicted_winner"]

    if winner != "Draw":
        return winner

    if row["team_1_win_probability"] >= row["team_2_win_probability"]:
        return row["team_1"]

    return row["team_2"]


def _confidence_label(value: str) -> str:
    labels = {
        "High": "Alta",
        "Medium": "Media",
        "Low": "Baja",
    }

    return labels.get(
        value,
        value
    )


def render_knockout_overview(
    final_df,
    rounds: dict[str, pd.DataFrame]
) -> None:
    final = _first_row(final_df)
    projected_champion = "Pendiente"
    final_text = "Final pendiente"

    if final is not None:
        projected_champion = translate_team(
            _forecast_winner(final)
        )
        final_text = (
            f"{translate_team(final['team_1'])} vs "
            f"{translate_team(final['team_2'])}"
        )

    total_matches = sum(
        0 if _is_empty(df) else len(df)
        for df in rounds.values()
    )

    st.markdown(
        _html(f"""
        <section class="bracket-hero">
            <div class="atlas-kicker">01 / Cuadro eliminatorio</div>
            <h1>La pared del campeonato</h1>
            <p>
                El tramo directo del torneo, leído como una lámina de revista:
                rutas, cruces y el último partido de la simulación.
            </p>
            <div class="bracket-hero-grid">
                <div>
                    <div class="atlas-small-label">Campeón proyectado</div>
                    <strong>{escape(projected_champion)}</strong>
                </div>
                <div>
                    <div class="atlas-small-label">Final actual</div>
                    <span>{escape(final_text)}</span>
                </div>
                <div>
                    <div class="atlas-small-label">Partidos del cuadro</div>
                    <strong>{total_matches}</strong>
                </div>
            </div>
        </section>
        """),
        unsafe_allow_html=True
    )


def render_match_card(row) -> str:
    winner = translate_team(
        _forecast_winner(row)
    )

    return _html(f"""
    <article class="bracket-match-card">
        <div class="bracket-card-teams">
            <div>{_team(row['team_1'])}</div>
            <span>vs</span>
            <div>{_team(row['team_2'])}</div>
        </div>
        <div class="bracket-card-footer">
            <strong>{escape(str(row['predicted_score']))}</strong>
            <span>{escape(winner)}</span>
            <em>{escape(_confidence_label(row['confidence']))}</em>
        </div>
    </article>
    """)


def render_wall_chart(
    rounds: dict[str, pd.DataFrame]
) -> None:
    st.markdown(
        '<div class="atlas-section-number">02</div>',
        unsafe_allow_html=True
    )
    st.header("El mapa de cruces")

    columns = st.columns(5)

    for column, (key, label) in zip(columns, ROUND_LABELS):
        with column:
            st.markdown(
                _html(f"""
                <div class="bracket-round-title">
                    <span>{escape(label)}</span>
                </div>
                """),
                unsafe_allow_html=True
            )

            round_df = rounds.get(key)

            if _is_empty(round_df):
                st.info("Ronda pendiente.")
                continue

            for _, row in round_df.iterrows():
                st.markdown(
                    render_match_card(row),
                    unsafe_allow_html=True
                )


def render_final_poster(final_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">03</div>',
        unsafe_allow_html=True
    )
    st.header("Afiche de la final")

    final = _first_row(final_df)

    if final is None:
        st.info("La final proyectada todavía no está disponible.")
        return

    champion = translate_team(
        _forecast_winner(final)
    )

    st.markdown(
        _html(f"""
        <section class="bracket-final-poster">
            <div class="atlas-small-label">Final proyectada</div>
            <h2>{_team(final['team_1'])}<span>vs</span>{_team(final['team_2'])}</h2>
            <div class="bracket-final-score">{escape(str(final['predicted_score']))}</div>
            <div class="bracket-champion-call">
                Campeón proyectado: <strong>{escape(champion)}</strong>
            </div>
        </section>
        """),
        unsafe_allow_html=True
    )


def render_third_place_match(third_place_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">04</div>',
        unsafe_allow_html=True
    )
    st.header("Partido por el tercer puesto")

    match = _first_row(third_place_df)

    if match is None:
        st.info("El partido por el tercer puesto todavía no está disponible.")
        return

    st.markdown(
        _html(f"""
        <section class="bracket-third-place">
            {render_match_card(match)}
        </section>
        """),
        unsafe_allow_html=True
    )


def render_knockout_notes(
    rounds: dict[str, pd.DataFrame],
    final_df
) -> None:
    st.markdown(
        '<div class="atlas-section-number">05</div>',
        unsafe_allow_html=True
    )
    st.header("Notas del cuadro")

    notes = []
    final = _first_row(final_df)

    if final is not None:
        champion = translate_team(
            _forecast_winner(final)
        )
        notes.append(
            f"{champion} queda señalado como campeón proyectado del cuadro actual."
        )
        notes.append(
            f"La final simulada enfrenta a {translate_team(final['team_1'])} y {translate_team(final['team_2'])}."
        )

    winners = Counter()

    for df in rounds.values():
        if _is_empty(df):
            continue

        for _, row in df.iterrows():
            winners[translate_team(_forecast_winner(row))] += 1

    if winners:
        recurring_team, count = winners.most_common(1)[0]
        notes.append(
            f"{recurring_team} aparece {count} veces como ganador de partido en las rondas cargadas."
        )

    if not notes:
        st.info("Las notas del cuadro todavía no están disponibles.")
        return

    for note in notes[:4]:
        st.markdown(
            _html(f"""
            <div class="atlas-narrative-note">
                {escape(note)}
            </div>
            """),
            unsafe_allow_html=True
        )
