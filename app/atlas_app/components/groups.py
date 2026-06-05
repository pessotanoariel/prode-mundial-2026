from html import escape
from textwrap import dedent

import pandas as pd
import streamlit as st

from app.atlas_app.formatting import translate_team


def _is_empty(df) -> bool:
    return df is None or df.empty


def _team_name(team: str) -> str:
    return escape(
        translate_team(team)
    )


def _html(markup: str) -> str:
    return "\n".join(
        line.strip()
        for line in dedent(markup)
        .strip()
        .splitlines()
    )


def _group_letters(groups_df, standings_df) -> list:
    if not _is_empty(groups_df) and "group" in groups_df.columns:
        return sorted(
            groups_df["group"]
            .dropna()
            .unique()
        )

    if not _is_empty(standings_df) and "group" in standings_df.columns:
        return sorted(
            standings_df["group"]
            .dropna()
            .unique()
        )

    return []


def _group_teams(groups_df, group) -> list:
    if _is_empty(groups_df):
        return []

    group_rows = groups_df[
        groups_df["group"] == group
    ]

    return (
        group_rows["country"]
        .dropna()
        .tolist()
    )


def _group_standings(standings_df, group) -> pd.DataFrame:
    if _is_empty(standings_df):
        return pd.DataFrame()

    return (
        standings_df[
            standings_df["group"] == group
        ]
        .sort_values("position")
    )


def _group_qualified(qualified_df, group) -> pd.DataFrame:
    if _is_empty(qualified_df):
        return pd.DataFrame()

    return (
        qualified_df[
            qualified_df["group"] == group
        ]
        .sort_values("position")
    )


def _group_matches(
    predictions_df,
    teams
) -> pd.DataFrame:
    if _is_empty(predictions_df) or not teams:
        return pd.DataFrame()

    return predictions_df[
        predictions_df["team_1"].isin(teams)
        &
        predictions_df["team_2"].isin(teams)
    ].copy()


def render_editorial_hero(
    groups_df,
    standings_df,
    qualified_df
) -> None:
    groups = _group_letters(
        groups_df,
        standings_df
    )
    group_count = len(groups)

    team_count = 0

    if not _is_empty(groups_df) and "country" in groups_df.columns:
        team_count = (
            groups_df["country"]
            .dropna()
            .nunique()
        )
    elif not _is_empty(standings_df):
        team_count = (
            standings_df["team"]
            .dropna()
            .nunique()
        )

    qualified_count = 0

    if not _is_empty(qualified_df):
        qualified_count = len(qualified_df)

    st.markdown(
        f"""
        <section class="groups-hero">
            <div class="atlas-kicker">03 / Fase de grupos</div>
            <h1>Los grupos del torneo</h1>
            <p>
                El primer acto del Mundial: doce zonas, cuarenta y ocho
                selecciones y una carrera corta hacia los dieciseisavos.
            </p>
            <div class="groups-hero-grid">
                <div>
                    <div class="atlas-small-label">Grupos</div>
                    <strong>{group_count}</strong>
                </div>
                <div>
                    <div class="atlas-small-label">Selecciones</div>
                    <strong>{team_count}</strong>
                </div>
                <div>
                    <div class="atlas-small-label">Formato</div>
                    <span>Clasifican 1º, 2º y los 8 mejores 3º</span>
                </div>
                <div>
                    <div class="atlas-small-label">Clasificados proyectados</div>
                    <strong>{qualified_count}</strong>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )


def render_group_dispatch_grid(
    groups_df,
    standings_df,
    qualified_df
) -> None:
    st.markdown(
        '<div class="atlas-section-number">01</div>',
        unsafe_allow_html=True
    )
    st.header("Mapa de grupos")

    groups = _group_letters(
        groups_df,
        standings_df
    )

    if not groups:
        st.info("Los grupos todavía no están disponibles.")
        return

    for start in range(0, len(groups), 4):
        cols = st.columns(4)

        for col, group in zip(cols, groups[start:start + 4]):
            standings = _group_standings(
                standings_df,
                group
            )
            qualified = _group_qualified(
                qualified_df,
                group
            )

            winner = "Pendiente"
            qualifiers = []

            if not standings.empty:
                winner = translate_team(
                    standings.iloc[0]["team"]
                )

            if not qualified.empty:
                qualifiers = [
                    translate_team(team)
                    for team in qualified["team"].head(3)
                ]

            qualifier_items = "".join(
                f"<li>{escape(team)}</li>"
                for team in qualifiers
            )

            if not qualifier_items:
                qualifier_items = "<li>Clasificación pendiente</li>"

            with col:
                st.markdown(
                    f"""
                    <article class="groups-dispatch-card">
                        <div class="groups-dispatch-letter">{escape(str(group))}</div>
                        <div>
                            <div class="atlas-small-label">Ganador proyectado</div>
                            <h3>{escape(winner)}</h3>
                        </div>
                        <div>
                            <div class="atlas-small-label">Zona de avance</div>
                            <ul>{qualifier_items}</ul>
                        </div>
                    </article>
                    """,
                    unsafe_allow_html=True
                )


def _render_standings_table(standings: pd.DataFrame) -> str:
    rows = []

    for _, row in standings.iterrows():
        position = int(row["position"])
        class_name = (
            "groups-qualified-row"
            if position <= 2
            else (
                "groups-third-row"
                if position == 3
                else ""
            )
        )

        rows.append(
            _html(f"""
            <div class="groups-standing-row {class_name}">
                <div class="groups-standing-rank">{position}</div>
                <div class="groups-standing-team">{_team_name(row['team'])}</div>
                <div>{int(row['PJ'])}</div>
                <div>{int(row['DG'])}</div>
                <div>{int(row['PTS'])}</div>
            </div>
            """)
        )

    return _html(f"""
    <div class="groups-standings">
        <div class="groups-standing-header">
            <div>Pos</div>
            <div>Selección</div>
            <div>PJ</div>
            <div>DG</div>
            <div>PTS</div>
        </div>
        {''.join(rows)}
    </div>
    """)


def _render_match_cards(matches: pd.DataFrame) -> None:
    if matches.empty:
        st.caption("No hay predicciones de partidos para este grupo.")
        return

    for _, row in matches.iterrows():
        winner = (
            "Empate"
            if row["predicted_winner"] == "Draw"
            else translate_team(row["predicted_winner"])
        )

        st.markdown(
            f"""
            <div class="groups-match-card">
                <div class="atlas-small-label">{escape(str(row['match_date']))}</div>
                <h4>{_team_name(row['team_1'])} vs {_team_name(row['team_2'])}</h4>
                <p><strong>{escape(str(row['predicted_score']))}</strong> · {escape(winner)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_group_spreads(
    groups_df,
    standings_df,
    qualified_df,
    predictions_df
) -> None:
    st.markdown(
        '<div class="atlas-section-number">02</div>',
        unsafe_allow_html=True
    )
    st.header("Crónicas de grupo")

    groups = _group_letters(
        groups_df,
        standings_df
    )

    if not groups:
        st.info("Las crónicas de grupo todavía no están disponibles.")
        return

    selected_group = st.radio(
        "Seleccionar grupo",
        groups,
        index=0,
        horizontal=True
    )

    teams = _group_teams(
        groups_df,
        selected_group
    )
    standings = _group_standings(
        standings_df,
        selected_group
    )
    matches = _group_matches(
        predictions_df,
        teams
    )

    st.markdown(
        f"""
        <section class="groups-spread">
            <div class="groups-spread-heading">
                <span>GRUPO</span>
                <strong>{escape(str(selected_group))}</strong>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )

    standings_col, matches_col = st.columns([1, 1.35])

    with standings_col:
        st.markdown(
            '<div class="atlas-kicker">Tabla proyectada</div>',
            unsafe_allow_html=True
        )

        if standings.empty:
            st.info("Tabla no disponible.")
        else:
            st.markdown(
                _render_standings_table(standings),
                unsafe_allow_html=True
            )

    with matches_col:
        st.markdown(
            '<div class="atlas-kicker">Partidos simulados</div>',
            unsafe_allow_html=True
        )
        _render_match_cards(matches)


def render_third_place_race(standings_df) -> None:
    st.markdown(
        '<div class="atlas-section-number">03</div>',
        unsafe_allow_html=True
    )
    st.header("La carrera de los terceros")

    if _is_empty(standings_df):
        st.info("El ranking de terceros todavía no está disponible.")
        return

    thirds = (
        standings_df[
            standings_df["position"] == 3
        ]
        .copy()
        .sort_values(
            by=["PTS", "DG", "GF"],
            ascending=[False, False, False]
        )
        .reset_index(drop=True)
    )

    rows = []

    for index, row in thirds.iterrows():
        rank = index + 1
        qualified = rank <= 8
        class_name = (
            "third-qualified"
            if qualified
            else "third-eliminated"
        )
        marker = (
            "CLASIFICA"
            if qualified
            else "FUERA"
        )

        rows.append(
            _html(f"""
            <div class="third-race-row {class_name}">
                <div class="third-race-rank">{rank:02d}</div>
                <div class="third-race-team">{_team_name(row['team'])}</div>
                <div class="third-race-points">{int(row['PTS'])} pts</div>
                <div class="third-race-status">{marker}</div>
            </div>
            """)
        )

        if rank == 8:
            rows.append(
                _html("""
                <div class="third-cutoff">Corte de clasificación</div>
                """)
            )

    st.markdown(
        _html(f"""
        <div class="third-race-ranking">
            <div class="third-race-header">
                <div>Rank</div>
                <div>Selección</div>
                <div>Puntos</div>
                <div>Estado</div>
            </div>
            {''.join(rows)}
        </div>
        """),
        unsafe_allow_html=True
    )


def render_qualification_notes(
    standings_df
) -> None:
    st.markdown(
        '<div class="atlas-section-number">04</div>',
        unsafe_allow_html=True
    )
    st.header("Notas de clasificación")

    if _is_empty(standings_df):
        st.info("Las notas de clasificación todavía no están disponibles.")
        return

    notes = []

    group_winners = (
        standings_df[
            standings_df["position"] == 1
        ]
        .sort_values("group")
    )

    for _, row in group_winners.head(3).iterrows():
        notes.append(
            f"{translate_team(row['team'])} lidera el Grupo {row['group']} con {int(row['PTS'])} puntos."
        )

    thirds = (
        standings_df[
            standings_df["position"] == 3
        ]
        .sort_values(
            by=["PTS", "DG", "GF"],
            ascending=[False, False, False]
        )
        .reset_index(drop=True)
    )

    if len(thirds) >= 9:
        eighth = thirds.iloc[7]
        ninth = thirds.iloc[8]
        notes.append(
            f"El corte de mejores terceros queda entre {translate_team(eighth['team'])} y {translate_team(ninth['team'])}."
        )

    if len(notes) < 4 and not group_winners.empty:
        strongest = group_winners.sort_values(
            by=["PTS", "DG", "GF"],
            ascending=[False, False, False]
        ).iloc[0]
        notes.append(
            f"{translate_team(strongest['team'])} firma una de las fases de grupo más sólidas del mapa."
        )

    for note in notes[:4]:
        st.markdown(
            f"""
            <div class="atlas-narrative-note">
                {escape(note)}
            </div>
            """,
            unsafe_allow_html=True
        )
