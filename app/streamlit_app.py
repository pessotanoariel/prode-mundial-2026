import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_PATH))

import pandas as pd
import streamlit as st

from config.translations import (
    TEAM_TRANSLATIONS
)


PREDICTIONS_PATH = Path(
    "data/output/predictions.csv"
)

GROUPS_PATH = Path(
    "data/raw/world_cup_groups.csv"
)

st.set_page_config(
    page_title="Prode Mundial 2026",
    page_icon="⚽",
    layout="wide"
)

@st.cache_data
def load_predictions():

    df = pd.read_csv(PREDICTIONS_PATH)

    return df


df = load_predictions()

groups_df = pd.read_csv(GROUPS_PATH)

group_mapping = (
    groups_df
    .groupby("group")["country"]
    .apply(list)
    .to_dict()
)

total_matches = len(df)

total_bardos = (
    df["upset_risk"] == "EXTREME"
).sum()

most_unbalanced_match = (
    df.sort_values(
        by="team_1_win_probability",
        ascending=False
    )
    .iloc[0]
)

most_unbalanced_team_1 = TEAM_TRANSLATIONS.get(
    most_unbalanced_match["team_1"],
    most_unbalanced_match["team_1"]
)

most_unbalanced_team_2 = TEAM_TRANSLATIONS.get(
    most_unbalanced_match["team_2"],
    most_unbalanced_match["team_2"]
)

most_unbalanced_label = (
    f"{most_unbalanced_team_1} vs {most_unbalanced_team_2}"
)

st.title("⚽ Prode Mundial 2026")
st.subheader("Predicciones IA del Mundial")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Partidos simulados",
    total_matches
)

col2.metric(
    "Posibles batacazos",
    total_bardos
)

col3.metric(
    "Partido más desparejo",
    most_unbalanced_label
)

confidence_filter = st.selectbox(
    "Filtrar por confianza",
    ["Todas", "Alta", "Media", "Baja"]
)

risk_filter = st.selectbox(
    "Filtrar por riesgo batacazo",
    ["Todos", "Bajo", "Medio", "Alto", "Bardo"]
)

st.write("## Predicciones de partidos")

display_df = df[
    [
        "match_date",
        "team_1",
        "team_2",
        "predicted_winner",
        "predicted_score",
        "confidence",
        "upset_risk"
    ]
].copy()


display_df.columns = [
    "Fecha",
    "Equipo 1",
    "Equipo 2",
    "Predicción",
    "Resultado Estimado",
    "Confianza",
    "Riesgo Batacazo"
]

dates = sorted(
    display_df["Fecha"].unique()
)

formatted_dates = pd.to_datetime(
    dates
).strftime("%d %b")

date_filter = st.selectbox(
    "Filtrar por fecha",
    ["Todas"] + list(formatted_dates)
)

group_filter = st.selectbox(
    "Filtrar por grupo",
    ["Todos"] + sorted(group_mapping.keys())
)

display_df["Equipo 1"] = (
    display_df["Equipo 1"]
    .replace(TEAM_TRANSLATIONS)
)

display_df["Equipo 2"] = (
    display_df["Equipo 2"]
    .replace(TEAM_TRANSLATIONS)
)

display_df["Predicción"] = (
    display_df["Predicción"]
    .replace(TEAM_TRANSLATIONS)
)

teams = sorted(
    list(
        set(display_df["Equipo 1"])
        | set(display_df["Equipo 2"])
    )
)

team_filter = st.selectbox(
    "Filtrar por selección",
    ["Todas"] + teams
)

display_df["Fecha"] = pd.to_datetime(
    display_df["Fecha"]
).dt.strftime("%d %b")

display_df["Confianza"] = (
    display_df["Confianza"]
    .replace({
        "High": "Alta",
        "Medium": "Media",
        "Low": "Baja"
    })
)

display_df["Riesgo Batacazo"] = (
    display_df["Riesgo Batacazo"]
    .replace({
        "LOW": "Bajo",
        "MEDIUM": "Medio",
        "HIGH": "Alto",
        "EXTREME": "Bardo"
    })
)

display_df["Predicción"] = (
    display_df["Predicción"]
    .replace({
        "Draw": "Empate"
    })
)

if confidence_filter != "Todas":

    display_df = display_df[
        display_df["Confianza"] == confidence_filter
    ]


if risk_filter != "Todos":

    display_df = display_df[
        display_df["Riesgo Batacazo"] == risk_filter
    ]

if team_filter != "Todas":

    display_df = display_df[
        (
            display_df["Equipo 1"] == team_filter
        )
        |
        (
            display_df["Equipo 2"] == team_filter
        )
    ]

if date_filter != "Todas":

    display_df = display_df[
        display_df["Fecha"] == date_filter
    ]

if group_filter != "Todos":

    selected_teams = group_mapping[group_filter]

    selected_teams = [
        TEAM_TRANSLATIONS.get(
            team,
            team
        )
        for team in selected_teams
   ]

    display_df = display_df[
        (
            display_df["Equipo 1"]
            .isin(selected_teams)
        )
        &
        (
            display_df["Equipo 2"]
            .isin(selected_teams)
        )
    ]

display_df = display_df.reset_index(
    drop=True
)

styled_df = (
    display_df.style
    .map(
        lambda x:
            "color: #00C853; font-weight: bold"
            if x == "Alta"
            else (
                "color: #FFD600; font-weight: bold"
                if x == "Media"
                else (
                    "color: #FF5252; font-weight: bold"
                    if x == "Baja"
                    else ""
                )
            ),
        subset=["Confianza"]
    )
    .map(
        lambda x:
            "color: #00C853; font-weight: bold"
            if x == "Bajo"
            else (
                "color: #FFD600; font-weight: bold"
                if x == "Medio"
                else (
                    "color: #FF9100; font-weight: bold"
                    if x == "Alto"
                    else (
                        "color: #FF1744; font-weight: bold"
                        if x == "Bardo"
                        else ""
                    )
                )
            ),
        subset=["Riesgo Batacazo"]
    )
)

st.table(
    styled_df.hide(axis="index")
)