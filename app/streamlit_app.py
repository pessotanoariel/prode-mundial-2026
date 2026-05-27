import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_PATH))

import pandas as pd
import streamlit as st

from config.translations import TEAM_TRANSLATIONS


PREDICTIONS_PATH = Path(
    "data/output/predictions.csv"
)


st.set_page_config(
    page_title="Prode Mundial 2026",
    page_icon="⚽",
    layout="wide"
)


st.title("⚽ Prode Mundial 2026")
st.subheader("Predicciones IA del Mundial")


@st.cache_data
def load_predictions():

    df = pd.read_csv(PREDICTIONS_PATH)

    return df


df = load_predictions()


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


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)