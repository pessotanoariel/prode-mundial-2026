from collections import Counter
from html import escape
from textwrap import dedent

import pandas as pd
import streamlit as st

from app.atlas_app.formatting import render_team_name
from app.atlas_app.venues import venue_label


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
    return render_team_name(team)


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
    simulation_champion = "Pendiente"
    final_text = "Final simulada pendiente"

    if final is not None:
        simulation_champion = render_team_name(
            _forecast_winner(final)
        )
        final_text = (
            f"{render_team_name(final['team_1'])} vs "
            f"{render_team_name(final['team_2'])}"
        )

    total_matches = sum(
        0 if _is_empty(df) else len(df)
        for df in rounds.values()
    )

    st.markdown(
        _html(f"""
        <section class="bracket-hero">
            <div class="atlas-kicker">05 / Cuadro eliminatorio</div>
            <h1>Una ruta simulada al título</h1>
            <p>
                Este cuadro representa una simulación individual del torneo.
                Las probabilidades agregadas se muestran en Atlas.
            </p>
            <div class="bracket-hero-grid">
                <div>
                    <div class="atlas-small-label">Campeón de la simulación</div>
                    <strong>{simulation_champion}</strong>
                </div>
                <div>
                    <div class="atlas-small-label">Final simulada</div>
                    <span>{final_text}</span>
                </div>
                <div>
                    <div class="atlas-small-label">Partidos eliminatorios</div>
                    <strong>{total_matches}</strong>
                </div>
            </div>
        </section>
        """),
        unsafe_allow_html=True
    )


def render_match_card(row) -> str:
    winner = render_team_name(
        _forecast_winner(row)
    )

    return _html(f"""
    <article class="bracket-match-card">
        <div class="bracket-card-teams">
            <div>{_team(row['team_1'])}</div>
            <span>vs</span>
            <div>{_team(row['team_2'])}</div>
        </div>
        <div class="bracket-card-venue">{escape(venue_label(row))}</div>
        <div class="bracket-card-footer">
            <strong>{escape(str(row['predicted_score']))}</strong>
            <span>{winner}</span>
            <em>{escape(_confidence_label(row['confidence']))}</em>
        </div>
    </article>
    """)


def _round_label_index(round_df) -> str:
    if _is_empty(round_df):
        return "0 partidos"

    match_count = len(round_df)

    if match_count == 1:
        return "1 partido"

    return f"{match_count} partidos"


def render_wall_chart(
    rounds: dict[str, pd.DataFrame]
) -> None:
    st.markdown(
        '<div class="atlas-section-number">02</div>',
        unsafe_allow_html=True
    )
    st.header("Ruta simulada del cuadro")

    stage_columns = []

    for index, (key, label) in enumerate(ROUND_LABELS, start=1):
        round_df = rounds.get(key)
        match_cards = []

        if _is_empty(round_df):
            match_cards.append(
                '<div class="bracket-stage-empty">Ronda pendiente</div>'
            )
        else:
            for _, row in round_df.iterrows():
                match_cards.append(
                    render_match_card(row)
                )

        stage_columns.append(
            _html(f"""
            <section class="bracket-stage-column bracket-stage-{escape(key)}">
                <div class="bracket-stage-heading">
                    <em>{index:02d}</em>
                    <div>
                        <strong>{escape(label)}</strong>
                        <span>{escape(_round_label_index(round_df))}</span>
                    </div>
                </div>
                <div class="bracket-stage-matches">
                    {''.join(match_cards)}
                </div>
            </section>
            """)
        )

    st.markdown(
        _html(f"""
        <div class="bracket-stage-grid">
            {''.join(stage_columns)}
        </div>
        """),
        unsafe_allow_html=True
    )


def render_final_poster(final_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">03</div>',
        unsafe_allow_html=True
    )
    st.header("Afiche de la final simulada")

    final = _first_row(final_df)

    if final is None:
        st.info("La final simulada todavía no está disponible.")
        return

    champion = render_team_name(
        _forecast_winner(final)
    )

    st.markdown(
        _html(f"""
        <section class="bracket-final-poster">
            <div class="atlas-small-label">Final simulada</div>
            <h2>{_team(final['team_1'])}<span>vs</span>{_team(final['team_2'])}</h2>
            <div class="bracket-final-venue">{escape(venue_label(final))}</div>
            <div class="bracket-final-score">{escape(str(final['predicted_score']))}</div>
            <div class="bracket-champion-call">
                Campeón de esta simulación: <strong>{champion}</strong>
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
        champion = render_team_name(
            _forecast_winner(final)
        )
        notes.append(
            f"{champion} queda señalado como campeón de esta simulación."
        )
        notes.append(
            f"La final simulada enfrenta a {render_team_name(final['team_1'])} y {render_team_name(final['team_2'])}."
        )

    winners = Counter()

    for df in rounds.values():
        if _is_empty(df):
            continue

        for _, row in df.iterrows():
            winners[render_team_name(_forecast_winner(row))] += 1

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
                {note}
            </div>
            """),
            unsafe_allow_html=True
        )
