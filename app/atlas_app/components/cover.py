import streamlit as st

from app.atlas_app.formatting import format_percent
from app.atlas_app.formatting import render_team_name


def _is_empty(df) -> bool:
    return df is None or df.empty


def _first_row(df):
    if _is_empty(df):
        return None

    return df.iloc[0]


def _winner_label(value: str) -> str:
    if value == "Draw":
        return "Empate"

    return render_team_name(value)


def render_magazine_hero(
    champions_df,
    finals_df
) -> None:
    favorite = _first_row(champions_df)
    final = _first_row(finals_df)

    final_text = "Final pendiente"

    if favorite is not None:
        favorite_team = render_team_name(favorite["team"])
        favorite_probability = format_percent(favorite["probability"])
    else:
        favorite_team = "Simulación pendiente"
        favorite_probability = "N/A"

    if final is not None:
        final_text = (
            f"{render_team_name(final['team_1'])} vs "
            f"{render_team_name(final['team_2'])}"
        )

    st.markdown(
        f"""
        <section class="atlas-hero">
            <div class="atlas-kicker">World Cup Forecast Atlas 2026</div>
            <h1>World Cup<br>Forecast<br>Atlas</h1>
            <p class="atlas-deck">
                Una revista interactiva del Mundial futuro,
                construida con los resultados actuales de la simulación.
            </p>
            <div class="atlas-hero-strip">
                <div class="atlas-hero-favorite">
                    <div class="atlas-small-label">Favorito actual</div>
                    <div class="atlas-hero-team">{favorite_team}</div>
                    <div class="atlas-hero-percent">{favorite_probability}</div>
                </div>
                <div class="atlas-hero-final">
                    <div class="atlas-small-label">Final más probable</div>
                    <h3>{final_text}</h3>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )


def render_top_favorites(champions_df) -> None:
    st.markdown(
        '<div class="atlas-kicker">Órbita del título</div>',
        unsafe_allow_html=True
    )
    st.header("Tres candidatos principales")

    if _is_empty(champions_df):
        st.info("Las probabilidades de campeón todavía no están disponibles.")
        return

    for index, row in champions_df.head(3).reset_index(drop=True).iterrows():
        st.markdown(
            f"""
            <div class="atlas-rank">
                <div class="atlas-rank-number">{index + 1:02d}</div>
                <div class="atlas-rank-team">{render_team_name(row['team'])}</div>
                <div class="atlas-rank-value">{format_percent(row['probability'])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_most_likely_final(finals_df, final_predictions_df) -> None:
    st.markdown(
        '<div class="atlas-kicker">Una final del futuro</div>',
        unsafe_allow_html=True
    )
    st.header("Final más probable")

    likely_final = _first_row(finals_df)
    predicted_final = _first_row(final_predictions_df)

    if likely_final is None and predicted_final is None:
        st.info("Los datos de la final todavía no están disponibles.")
        return

    if likely_final is not None:
        team_1 = render_team_name(likely_final["team_1"])
        team_2 = render_team_name(likely_final["team_2"])
        probability = format_percent(likely_final["probability"])

        st.markdown(
            f"""
            <div class="atlas-panel atlas-panel-violet">
                <div class="atlas-small-label">Cruce Monte Carlo</div>
                <h2>{team_1} vs {team_2}</h2>
                <p>{probability} de las finales simuladas</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if predicted_final is not None:
        winner = _winner_label(predicted_final["predicted_winner"])
        score = predicted_final["predicted_score"]

        st.markdown(
            f"""
            <div class="atlas-panel">
                <div class="atlas-small-label">Final del cuadro actual</div>
                <h3>{render_team_name(predicted_final['team_1'])} vs {render_team_name(predicted_final['team_2'])}</h3>
                <p>Marcador proyectado: <strong>{score}</strong></p>
                <p>Lectura del pronóstico: <strong>{winner}</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_group_dispatch_grid(
    standings_df,
    qualified_df
) -> None:
    st.markdown(
        '<div class="atlas-kicker">Despachos de grupo</div>',
        unsafe_allow_html=True
    )
    st.header("Apuntes del primer acto")

    if _is_empty(standings_df):
        st.info("Las tablas de grupos todavía no están disponibles.")
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

            projected_winner = "Pendiente"
            qualified_names = []

            if not group_standings.empty:
                projected_winner = render_team_name(
                    group_standings.iloc[0]["team"]
                )

            if not _is_empty(group_qualified):
                qualified_names = [
                    render_team_name(team)
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
                    f'+{hidden_qualifiers_count} más'
                    f'</li>'
                )

            if not qualified_items:
                qualified_items = "<li>Clasificación pendiente</li>"

            with col:
                st.markdown(
                    f"""
                    <div class="atlas-group-card">
                        <div class="atlas-group-letter">{group}</div>
                        <div class="atlas-group-body">
                            <div>
                                <div class="atlas-small-label">Ganador proyectado</div>
                                <h4>{projected_winner}</h4>
                            </div>
                            <div>
                                <div class="atlas-small-label">Zona de avance</div>
                                <ul>{qualified_items}</ul>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def render_tournament_teaser(final_predictions_df, champions_df) -> None:
    st.markdown(
        '<div class="atlas-kicker">Camino al título</div>',
        unsafe_allow_html=True
    )
    st.header("El cuadro empieza acá")

    final = _first_row(final_predictions_df)
    champion = _first_row(champions_df)

    if final is None and champion is None:
        st.info("Los datos del adelanto del torneo todavía no están disponibles.")
        return

    left_col, right_col = st.columns([2, 1])

    with left_col:
        if final is not None:
            st.markdown(
                f"""
                <div class="atlas-panel atlas-panel-red">
                    <div class="atlas-small-label">Final proyectada del cuadro actual</div>
                    <h2>{render_team_name(final['team_1'])} vs {render_team_name(final['team_2'])}</h2>
                    <p>Marcador del modelo: <strong>{final['predicted_score']}</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with right_col:
        if champion is not None:
            st.markdown(
                f"""
                <div class="atlas-panel atlas-panel-green">
                    <div class="atlas-small-label">Equipo de portada</div>
                    <h2>{render_team_name(champion['team'])}</h2>
                    <p>{format_percent(champion['probability'])} de probabilidad de título</p>
                </div>
                """,
                unsafe_allow_html=True
            )
