from collections import Counter
from html import escape
from textwrap import dedent

import streamlit as st

from app.atlas_app.formatting import format_percent
from app.atlas_app.formatting import render_team_name
from app.atlas_app.cities import host_city_narratives


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
            <div class="atlas-kicker">02 / ATLAS DEL MUNDIAL</div>
            <h1>El mapa del torneo</h1>
            <p>
                El centro analítico de la revista: gravedad de campeón,
                finales proyectadas y selecciones que empiezan a tomar forma.
            </p>
            <div class="atlas-analysis-hero-grid">
                <div>
                    <div class="atlas-small-label">Máximo favorito</div>
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
    st.header("Favoritos al título")

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
    st.header("Finales más probables")

    if _is_empty(finals_df):
        st.info("Las finales más probables todavía no están disponibles.")
        return

    top_finals = finals_df.head(3).reset_index(drop=True)
    cols = st.columns(3)

    for index, (col, (_, row)) in enumerate(
        zip(cols, top_finals.iterrows())
    ):
        with col:
            st.markdown(
                f"""
                <article class="atlas-final-card">
                    <div class="atlas-small-label">#{index + 1}</div>
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
    st.header("Probabilidad de llegar a la final")

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


def render_host_city_profiles(profiles_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">05</div>',
        unsafe_allow_html=True
    )
    st.header("Ciudades sede del Mundial")

    if _is_empty(profiles_df):
        st.info("Sede por confirmar")
        return

    profiles = profiles_df.copy()
    total_cities = profiles["host_city"].nunique()
    total_stadiums = profiles["stadium"].nunique()
    host_countries = profiles["country"].nunique()

    final_city = profiles[
        profiles["is_final_venue"].astype(bool)
    ].head(1)
    opening_city = profiles[
        profiles["is_opening_match_venue"].astype(bool)
    ].head(1)
    busiest_city = profiles.sort_values(
        ["matches", "knockout_matches"],
        ascending=False
    ).head(1)

    featured = [
        ("Final", final_city),
        ("Inauguración", opening_city),
        ("Sede con más partidos", busiest_city),
    ]

    cards = []

    for label, city_df in featured:
        if city_df.empty:
            cards.append(
                _html(f"""
                    <article class="atlas-city-summary-card">
                        <div class="atlas-small-label">{label}</div>
                        <h3>Sede por confirmar</h3>
                    <strong>Sede por confirmar</strong>
                        <span>Calendario pendiente</span>
                    </article>
                """)
            )
            continue

        row = city_df.iloc[0]
        cards.append(
            _html(f"""
            <article class="atlas-city-summary-card">
                <div class="atlas-small-label">{escape(label)}</div>
                <h3>{escape(str(row['host_city']))}</h3>
                <strong>{escape(str(row['stadium']))}</strong>
                <span>{int(row['matches'])} partidos</span>
                <small>{escape(str(row['country']))}</small>
            </article>
            """)
        )

    notes = host_city_narratives(profiles)[:3]
    narrative = " ".join(
        escape(str(note))
        for note in notes
    )

    st.markdown(
        _html(f"""
        <section class="atlas-city-summary">
            <div class="atlas-city-summary-stats">
                <div>
                    <strong>{total_cities}</strong>
                    <span>ciudades sede</span>
                </div>
                <div>
                    <strong>{total_stadiums}</strong>
                    <span>estadios</span>
                </div>
                <div>
                    <strong>{host_countries}</strong>
                    <span>países anfitriones</span>
                </div>
            </div>
            <div class="atlas-city-summary-grid">
                {''.join(cards)}
            </div>
            <p>{narrative}</p>
        </section>
        """),
        unsafe_allow_html=True
    )

def render_forecast_notes() -> None:
    st.markdown(
        '<div class="atlas-section-number">06</div>',
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
