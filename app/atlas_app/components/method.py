from html import escape
from textwrap import dedent

import streamlit as st


def _html(markup: str) -> str:
    return "\n".join(
        line.strip()
        for line in dedent(markup)
        .strip()
        .splitlines()
    )


def render_method_hero() -> None:
    st.markdown(
        _html("""
        <section class="method-hero">
            <div class="atlas-kicker">06 / Método</div>
            <h1>Cómo leer el atlas</h1>
            <p>
                Una guía editorial para entender de dónde salen los pronósticos,
                cómo viajan por el torneo y qué significan sus señales.
            </p>
        </section>
        """),
        unsafe_allow_html=True
    )


def _render_process_cards(cards) -> None:
    for start in range(0, len(cards), 2):
        cols = st.columns(2)

        for col, card in zip(cols, cards[start:start + 2]):
            with col:
                st.markdown(
                    _html(f"""
                    <article class="method-card">
                        <div class="method-card-number">{escape(card["number"])}</div>
                        <h3>{escape(card["title"])}</h3>
                        <p>{escape(card["body"])}</p>
                    </article>
                    """),
                    unsafe_allow_html=True
                )


def render_forecast_engine() -> None:
    st.markdown(
        '<div class="atlas-section-number">01</div>',
        unsafe_allow_html=True
    )
    st.header("El motor del pronóstico")
    _render_process_cards([
        {
            "number": "01",
            "title": "Fuerza base",
            "body": "Los ratings Elo funcionan como una primera medida de potencia entre selecciones.",
        },
        {
            "number": "02",
            "title": "Forma reciente",
            "body": "Los resultados más cercanos ajustan la lectura: no todo equipo llega al torneo igual.",
        },
        {
            "number": "03",
            "title": "Probabilidades de partido",
            "body": "La diferencia de fuerza entre equipos se convierte en chances de victoria, empate o derrota.",
        },
        {
            "number": "04",
            "title": "Marcador proyectado",
            "body": "Las expectativas de gol traducen esas chances en resultados estimados para cada cruce.",
        },
    ])


def render_tournament_flow() -> None:
    st.markdown(
        '<div class="atlas-section-number">02</div>',
        unsafe_allow_html=True
    )
    st.header("De grupos a campeón")
    st.markdown(
        _html("""
        <div class="method-flow">
            <div>Fase de grupos</div>
            <span></span>
            <div>Tablas</div>
            <span></span>
            <div>Mejores terceros</div>
            <span></span>
            <div>Anexo C FIFA</div>
            <span></span>
            <div>Eliminatorias</div>
            <span></span>
            <div>Campeón</div>
        </div>
        """),
        unsafe_allow_html=True
    )
    _render_process_cards([
        {
            "number": "A",
            "title": "Primera ronda",
            "body": "Cada grupo genera una tabla proyectada con puntos, goles y diferencia de gol.",
        },
        {
            "number": "B",
            "title": "Terceros lugares",
            "body": "El formato 2026 abre una carrera especial: los ocho mejores terceros también avanzan.",
        },
        {
            "number": "C",
            "title": "Mapa oficial",
            "body": "El Anexo C define cómo se ordenan ciertos cruces según qué terceros clasifican.",
        },
        {
            "number": "D",
            "title": "Camino directo",
            "body": "Desde dieciseisavos, cada ronda alimenta la siguiente hasta llegar a la final.",
        },
    ])


def render_monte_carlo() -> None:
    st.markdown(
        '<div class="atlas-section-number">03</div>',
        unsafe_allow_html=True
    )
    st.header("Torneo Monte Carlo")
    _render_process_cards([
        {
            "number": "MC",
            "title": "Muchos Mundiales posibles",
            "body": "El atlas repite el torneo muchas veces para observar patrones, no una única historia.",
        },
        {
            "number": "%",
            "title": "Probabilidad de campeón",
            "body": "Cada título simulado suma peso a la chance final de una selección.",
        },
        {
            "number": "F",
            "title": "Finales frecuentes",
            "body": "Las finales más repetidas muestran qué cruces aparecen con más fuerza en el modelo.",
        },
        {
            "number": "R",
            "title": "Progresión",
            "body": "Las estimaciones por ronda cuentan qué equipos suelen seguir vivos más tiempo.",
        },
    ])


def render_number_meanings() -> None:
    st.markdown(
        '<div class="atlas-section-number">04</div>',
        unsafe_allow_html=True
    )
    st.header("Qué significan los números")
    _render_process_cards([
        {
            "number": "T",
            "title": "Tono del pronóstico",
            "body": "Resume cuán clara aparece una lectura de partido: alto, medio o bajo.",
        },
        {
            "number": "S",
            "title": "Alerta de sorpresa",
            "body": "Señala partidos donde la diferencia esperada se vuelve estrecha o inestable.",
        },
        {
            "number": "C",
            "title": "Chance de campeón",
            "body": "No es una certeza: es la frecuencia con que un equipo levanta la copa en las simulaciones.",
        },
        {
            "number": "F",
            "title": "Final más probable",
            "body": "Es el cruce que más se repite entre finales simuladas, no una predicción cerrada.",
        },
    ])


def render_editorial_notes() -> None:
    st.markdown(
        '<div class="atlas-section-number">05</div>',
        unsafe_allow_html=True
    )
    st.header("Notas editoriales")
    st.markdown(
        _html("""
        <section class="method-editorial-note">
            <strong>Este atlas es una simulación.</strong>
            <p>
                Los resultados nacen del modelo actual de pronóstico y sirven
                para explorar escenarios, rutas y relatos posibles del Mundial.
                No son consejos de apuesta, no son resultados en vivo y pueden
                diferir por completo de lo que ocurra en la cancha.
            </p>
        </section>
        """),
        unsafe_allow_html=True
    )
