from collections import Counter
from html import escape
from textwrap import dedent

import streamlit as st

from app.atlas_app.formatting import format_percent
from app.atlas_app.formatting import render_team_name


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


def _html(markup: str) -> str:
    return "\n".join(
        line.strip()
        for line in dedent(markup)
        .strip()
        .splitlines()
    )


def render_editorial_hero(
    champions_df,
    finals_df
) -> None:
    favorite = _first_row(champions_df)
    final = _first_row(finals_df)

    favorite_team = "Simulación pendiente"
    favorite_probability = "N/A"
    final_text = "Final pendiente"

    if favorite is not None:
        favorite_team = render_team_name(favorite["team"])
        favorite_probability = format_percent(favorite["probability"])

    if final is not None:
        final_text = (
            f"{render_team_name(final['team_1'])} vs "
            f"{render_team_name(final['team_2'])}"
        )

    st.markdown(
        f"""
        <section class="atlas-analysis-hero">
            <div class="atlas-kicker">02 / WORLD CUP FORECAST ATLAS</div>
            <h1>El mapa del torneo</h1>
            <p>
                El centro analítico de la revista: gravedad de campeón,
                finales proyectadas y selecciones que empiezan a tomar forma.
            </p>
            <div class="atlas-analysis-hero-grid">
                <div>
                    <div class="atlas-small-label">Favorito actual</div>
                    <div class="atlas-analysis-team">{favorite_team}</div>
                    <div class="atlas-analysis-percent">{favorite_probability}</div>
                </div>
                <div>
                    <div class="atlas-small-label">Final más probable</div>
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
    st.header("Órbita del campeonato")

    if _is_empty(champions_df):
        st.info("Las probabilidades de campeón todavía no están disponibles.")
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
                        <span>{render_team_name(row['team'])}</span>
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
    st.header("Finales del futuro")

    if _is_empty(finals_df):
        st.info("Las finales más probables todavía no están disponibles.")
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
                        <div class="atlas-small-label">Final proyectada #{start + offset + 1}</div>
                        <h3>{render_team_name(row['team_1'])}<br>vs<br>{render_team_name(row['team_2'])}</h3>
                        <p>{format_percent(row['probability'])} de las finales simuladas</p>
                    </article>
                    """,
                    unsafe_allow_html=True
                )


def render_finalist_probabilities(finalists_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">03</div>',
        unsafe_allow_html=True
    )
    st.header("Candidatos a finalista")

    if _is_empty(finalists_df):
        st.info("Las probabilidades de finalista todavÃ­a no estÃ¡n disponibles.")
        return

    top_finalists = finalists_df.head(8)

    for _, row in top_finalists.iterrows():
        st.markdown(
            f"""
            <div class="atlas-tier-row atlas-tier-row-muted">
                <strong>{render_team_name(row['team'])}</strong>
                <span>{format_percent(row['final_probability'])}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_contenders_and_challengers(champions_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">04</div>',
        unsafe_allow_html=True
    )
    st.header("Favoritos y perseguidores")

    if _is_empty(champions_df):
        st.info("Los datos de favoritos todavía no están disponibles.")
        return

    contenders = champions_df.head(3)
    challengers = champions_df.iloc[3:8]

    contenders_col, challengers_col = st.columns(2)

    with contenders_col:
        st.markdown(
            '<div class="atlas-kicker">Favoritos al título</div>',
            unsafe_allow_html=True
        )

        for index, row in contenders.reset_index(drop=True).iterrows():
            st.markdown(
                f"""
                <div class="atlas-tier-row atlas-tier-row-featured">
                    <em>{index + 1:02d}</em>
                    <strong>{render_team_name(row['team'])}</strong>
                    <span>{format_percent(row['probability'])}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    with challengers_col:
        st.markdown(
            '<div class="atlas-kicker">Segunda línea</div>',
            unsafe_allow_html=True
        )

        if challengers.empty:
            st.caption("No hay perseguidores disponibles todavía.")
            return

        for _, row in challengers.iterrows():
            st.markdown(
                f"""
                <div class="atlas-tier-row atlas-tier-row-muted">
                    <strong>{render_team_name(row['team'])}</strong>
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
        '<div class="atlas-section-number">05</div>',
        unsafe_allow_html=True
    )
    st.header("Narrativa del torneo")

    notes = []
    favorite = _first_row(champions_df)

    if favorite is not None:
        notes.append(
            f"{render_team_name(favorite['team'])} aparece como favorito de la simulación con {format_percent(favorite['probability'])}."
        )

    if not _is_empty(champions_df) and len(champions_df) > 1:
        second = champions_df.iloc[1]
        notes.append(
            f"{render_team_name(second['team'])} queda a tiro, todavía dentro del primer anillo de candidatos."
        )

    if not _is_empty(finals_df):
        teams = Counter()

        for _, row in finals_df.head(10).iterrows():
            teams[row["team_1"]] += 1
            teams[row["team_2"]] += 1

        recurring_team, appearances = teams.most_common(1)[0]
        notes.append(
            f"{render_team_name(recurring_team)} se repite en {appearances} de las diez finales proyectadas más frecuentes."
        )

    if not _is_empty(progression_df):
        finalist = (
            progression_df
            .sort_values("final", ascending=False)
            .iloc[0]
        )
        notes.append(
            f"{render_team_name(finalist['team'])} muestra el perfil más fuerte para llegar a la final: {format_percent(finalist['final'])}."
        )

    final = _first_row(final_predictions_df)

    if final is not None:
        notes.append(
            f"El cuadro actual desemboca en una final {render_team_name(final['team_1'])} vs {render_team_name(final['team_2'])}."
        )

    if not notes:
        st.info("Las notas narrativas todavía no están disponibles.")
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


def render_world_cup_venues(stadiums_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">06</div>',
        unsafe_allow_html=True
    )
    st.header("World Cup Venues")

    if _is_empty(stadiums_df):
        st.info("Venue TBD")
        return

    venues = stadiums_df.sort_values(
        ["country", "host_city"]
    )

    cards = []

    for _, row in venues.iterrows():
        cards.append(
            _html(f"""
            <article class="atlas-venue-card">
                <div class="atlas-small-label">{escape(str(row['country']))}</div>
                <strong>{escape(str(row['stadium']))}</strong>
                <span>{escape(str(row['host_city']))}</span>
            </article>
            """)
        )

    st.markdown(
        _html(f"""
        <div class="atlas-venues-grid">
            {''.join(cards)}
        </div>
        """),
        unsafe_allow_html=True
    )

def render_forecast_notes() -> None:
    st.markdown(
        '<div class="atlas-section-number">07</div>',
        unsafe_allow_html=True
    )
    st.header("Notas metodológicas")
    st.markdown(
        """
        <div class="atlas-forecast-note">
            Estas lecturas salen de los outputs actuales del pronóstico:
            probabilidades de campeón, finales probables, progresión por ronda
            cuando está disponible y la última final simulada. Es una capa de
            simulación para explorar el torneo y construir relato, no una
            recomendación de apuestas ni una cobertura de resultados en vivo.
        </div>
        """,
        unsafe_allow_html=True
    )
