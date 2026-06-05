from collections import Counter
from html import escape
from textwrap import dedent

import pandas as pd
import streamlit as st

from app.atlas_app.formatting import translate_team


CONFIDENCE_LABELS = {
    "High": "Alto",
    "Medium": "Medio",
    "Low": "Bajo",
}

RISK_LABELS = {
    "LOW": "Baja",
    "MEDIUM": "Media",
    "HIGH": "Alta",
    "EXTREME": "Extrema",
}

RISK_ORDER = {
    "EXTREME": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}


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


def _winner(value: str) -> str:
    if value == "Draw":
        return "Empate"

    return translate_team(value)


def _format_date(value) -> str:
    try:
        return pd.to_datetime(value).strftime("%d %b")
    except Exception:
        return str(value)


def render_editorial_hero(predictions_df) -> None:
    total_matches = 0
    coverage = "Sin cobertura disponible"

    if not _is_empty(predictions_df):
        total_matches = len(predictions_df)
        teams = pd.concat([
            predictions_df["team_1"],
            predictions_df["team_2"],
        ]).dropna().nunique()
        dates = predictions_df["match_date"].dropna().nunique()
        coverage = f"{teams} selecciones · {dates} jornadas"

    st.markdown(
        _html(f"""
        <section class="matches-hero">
            <div class="atlas-kicker">05 / Archivo de partidos</div>
            <h1>Archivo de pronósticos</h1>
            <p>
                Una colección editorial de resultados proyectados desde la
                simulación actual de la fase de grupos.
            </p>
            <div class="matches-hero-grid">
                <div>
                    <div class="atlas-small-label">Partidos simulados</div>
                    <strong>{total_matches}</strong>
                </div>
                <div>
                    <div class="atlas-small-label">Cobertura actual</div>
                    <span>{escape(coverage)}</span>
                </div>
            </div>
        </section>
        """),
        unsafe_allow_html=True
    )


def render_match_index(predictions_df) -> tuple[pd.DataFrame, str]:
    st.markdown(
        '<div class="atlas-section-number">02</div>',
        unsafe_allow_html=True
    )
    st.header("Índice de partidos")

    if _is_empty(predictions_df):
        st.info("Los pronósticos de partidos todavía no están disponibles.")
        return pd.DataFrame(), "12"

    teams = sorted(
        set(predictions_df["team_1"].dropna())
        | set(predictions_df["team_2"].dropna())
    )
    translated_teams = [
        translate_team(team)
        for team in teams
    ]
    team_lookup = dict(
        zip(
            translated_teams,
            teams
        )
    )
    dates = sorted(
        predictions_df["match_date"]
        .dropna()
        .unique()
    )
    formatted_dates = [
        _format_date(date)
        for date in dates
    ]
    date_lookup = dict(
        zip(
            formatted_dates,
            dates
        )
    )

    st.markdown(
        '<div class="match-index-panel">',
        unsafe_allow_html=True
    )

    col_1, col_2, col_3, col_4, col_5 = st.columns([1, 1, 1.1, 1, 0.8])

    with col_1:
        st.markdown(
            '<div class="match-filter-label">Tono del pronóstico</div>',
            unsafe_allow_html=True
        )
        confidence_filter = st.selectbox(
            "Tono del pronóstico",
            ["Todos", "Alto", "Medio", "Bajo"],
            label_visibility="collapsed"
        )

    with col_2:
        st.markdown(
            '<div class="match-filter-label">Alerta de sorpresa</div>',
            unsafe_allow_html=True
        )
        risk_filter = st.selectbox(
            "Alerta de sorpresa",
            ["Todas", "Baja", "Media", "Alta", "Extrema"],
            label_visibility="collapsed"
        )

    with col_3:
        st.markdown(
            '<div class="match-filter-label">Selección</div>',
            unsafe_allow_html=True
        )
        team_filter = st.selectbox(
            "Selección",
            ["Todas"] + translated_teams,
            label_visibility="collapsed"
        )

    with col_4:
        st.markdown(
            '<div class="match-filter-label">Jornada</div>',
            unsafe_allow_html=True
        )
        date_filter = st.selectbox(
            "Jornada",
            ["Todas"] + formatted_dates,
            label_visibility="collapsed"
        )

    with col_5:
        st.markdown(
            '<div class="match-filter-label">Mostrar</div>',
            unsafe_allow_html=True
        )
        display_limit = st.selectbox(
            "Mostrar",
            ["12", "24", "48", "Todos"],
            label_visibility="collapsed"
        )

    filtered = predictions_df.copy()

    if confidence_filter != "Todos":
        reverse_confidence = {
            value: key
            for key, value in CONFIDENCE_LABELS.items()
        }
        filtered = filtered[
            filtered["confidence"] == reverse_confidence[confidence_filter]
        ]

    if risk_filter != "Todas":
        reverse_risk = {
            value: key
            for key, value in RISK_LABELS.items()
        }
        filtered = filtered[
            filtered["upset_risk"] == reverse_risk[risk_filter]
        ]

    if team_filter != "Todas":
        selected_team = team_lookup[team_filter]
        filtered = filtered[
            (filtered["team_1"] == selected_team)
            |
            (filtered["team_2"] == selected_team)
        ]

    if date_filter != "Todas":
        filtered = filtered[
            filtered["match_date"] == date_lookup[date_filter]
        ]

    st.caption(
        f"{len(filtered)} partidos en esta selección editorial."
    )
    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    return filtered, display_limit


def render_match_card(row) -> str:
    confidence = CONFIDENCE_LABELS.get(
        row["confidence"],
        row["confidence"]
    )
    risk = RISK_LABELS.get(
        row["upset_risk"],
        row["upset_risk"]
    )

    return _html(f"""
    <article class="match-forecast-card">
        <div class="match-card-date">{escape(_format_date(row['match_date']))}</div>
        <h3>{_team(row['team_1'])}<span>vs</span>{_team(row['team_2'])}</h3>
        <div class="match-card-score">{escape(str(row['predicted_score']))}</div>
        <div class="match-card-winner">Gana: <strong>{escape(_winner(row['predicted_winner']))}</strong></div>
        <div class="match-card-badges">
            <span>Tono {escape(confidence)}</span>
            <span>Sorpresa {escape(risk)}</span>
        </div>
    </article>
    """)


def render_forecast_cards(
    filtered_df,
    display_limit="12"
) -> None:
    st.markdown(
        '<div class="atlas-section-number">05</div>',
        unsafe_allow_html=True
    )
    st.header("Archivo de tarjetas")

    if _is_empty(filtered_df):
        st.info("No hay partidos para los filtros seleccionados.")
        return

    visible_df = filtered_df

    if display_limit != "Todos":
        visible_df = filtered_df.head(
            int(display_limit)
        )

    st.caption(
        f"Mostrando {len(visible_df)} de {len(filtered_df)} partidos filtrados."
    )

    cards_per_row = 3

    for start in range(0, len(visible_df), cards_per_row):
        cols = st.columns(cards_per_row)

        for col, (_, row) in zip(
            cols,
            visible_df.iloc[start:start + cards_per_row].iterrows()
        ):
            with col:
                st.markdown(
                    render_match_card(row),
                    unsafe_allow_html=True
                )


def _risk_sorted(df) -> pd.DataFrame:
    if _is_empty(df):
        return pd.DataFrame()

    ranked = df.copy()
    ranked["risk_rank"] = ranked["upset_risk"].map(RISK_ORDER).fillna(0)

    return ranked.sort_values(
        by=["risk_rank", "draw_probability"],
        ascending=[False, False]
    )


def render_surprise_watch(predictions_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">03</div>',
        unsafe_allow_html=True
    )
    st.header("Alerta de sorpresa")

    ranked = _risk_sorted(predictions_df)

    if ranked.empty:
        st.info("No hay alertas de sorpresa disponibles.")
        return

    for _, row in ranked.head(4).iterrows():
        st.markdown(
            _html(f"""
            <div class="match-callout">
                <div class="atlas-small-label">{escape(RISK_LABELS.get(row['upset_risk'], row['upset_risk']))}</div>
                <strong>{_team(row['team_1'])} vs {_team(row['team_2'])}</strong>
                <span>{escape(str(row['predicted_score']))} · {_winner(row['predicted_winner'])}</span>
            </div>
            """),
            unsafe_allow_html=True
        )


def render_strongest_forecasts(predictions_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">04</div>',
        unsafe_allow_html=True
    )
    st.header("Pronósticos más firmes")

    if _is_empty(predictions_df):
        st.info("No hay pronósticos firmes disponibles.")
        return

    strongest = predictions_df[
        predictions_df["confidence"] == "High"
    ].copy()

    if strongest.empty:
        strongest = predictions_df.copy()

    strongest["probability_peak"] = strongest[
        [
            "team_1_win_probability",
            "team_2_win_probability",
        ]
    ].max(axis=1)

    strongest = strongest.sort_values(
        "probability_peak",
        ascending=False
    )

    for _, row in strongest.head(4).iterrows():
        st.markdown(
            _html(f"""
            <div class="match-callout match-callout-yellow">
                <div class="atlas-small-label">Tono {escape(CONFIDENCE_LABELS.get(row['confidence'], row['confidence']))}</div>
                <strong>{_team(row['team_1'])} vs {_team(row['team_2'])}</strong>
                <span>{escape(str(row['predicted_score']))} · {_winner(row['predicted_winner'])}</span>
            </div>
            """),
            unsafe_allow_html=True
        )


def render_match_notes(filtered_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">06</div>',
        unsafe_allow_html=True
    )
    st.header("Notas del archivo")

    if _is_empty(filtered_df):
        st.info("No hay notas para esta selección.")
        return

    notes = []
    high_confidence = filtered_df[
        filtered_df["confidence"] == "High"
    ]
    surprise_matches = filtered_df[
        filtered_df["upset_risk"].isin(["HIGH", "EXTREME"])
    ]

    if not high_confidence.empty:
        winners = Counter(
            high_confidence["predicted_winner"]
            .replace("Draw", "Empate")
        )
        team, count = winners.most_common(1)[0]
        notes.append(
            f"{translate_team(team)} aparece en {count} de los pronósticos más firmes de esta selección."
        )

    if not surprise_matches.empty:
        notes.append(
            f"{len(surprise_matches)} partidos quedan en zona alta de sorpresa."
        )

    if len(filtered_df) > 0:
        first = filtered_df.iloc[0]
        notes.append(
            f"{translate_team(first['team_1'])} vs {translate_team(first['team_2'])} abre esta página del archivo."
        )

    for note in notes[:4]:
        st.markdown(
            _html(f"""
            <div class="atlas-narrative-note">
                {escape(note)}
            </div>
            """),
            unsafe_allow_html=True
        )
