import sys
from pathlib import Path

import streamlit as st

from PIL import Image

icon = Image.open("app/assets/world-cup.png")

ROOT_PATH = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_PATH))

from app.atlas_app.data import load_atlas_data
from app.atlas_app.pages import atlas
from app.atlas_app.pages import bracket
from app.atlas_app.pages import cover
from app.atlas_app.pages import groups
from app.atlas_app.pages import matches
from app.atlas_app.pages import method
from app.atlas_app.styles import apply_global_styles


PAGES = {
    "Portada": cover.render,
    "Atlas": atlas.render,
    "Grupos": groups.render,
    "Partidos": matches.render,
    "Eliminatorias": bracket.render,
    "Método": method.render,
}


def render_navigation() -> str:
    st.sidebar.markdown(
        """
        <div class="atlas-sidebar-brand">
            <div class="atlas-sidebar-kicker">Copa del Mundo</div>
            <div class="atlas-sidebar-title">Atlas<br>Mundialista</div>
            <div class="atlas-sidebar-year">2026</div>
            <div class="atlas-sidebar-deck">Pronósticos y simulación del torneo</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    return st.sidebar.radio(
        "Secciones",
        list(PAGES.keys()),
        label_visibility="visible",
        key="sidebar_navigation"
    )


def scroll_to_top_on_page_change(selected_page: str) -> None:
    previous_page = st.session_state.get("selected_page")
    st.session_state["selected_page"] = selected_page

    if previous_page is None or previous_page == selected_page:
        return

    st.html(
        """
        <script>
        const scrollTargets = [
            window.parent,
            window.parent.document.documentElement,
            window.parent.document.body,
            window.parent.document.querySelector('[data-testid="stAppViewContainer"]'),
            window.parent.document.querySelector('[data-testid="stMain"]'),
            window.parent.document.querySelector('section.main')
        ];

        scrollTargets.forEach((target) => {
            if (!target) {
                return;
            }

            if (typeof target.scrollTo === 'function') {
                target.scrollTo(0, 0);
            } else {
                target.scrollTop = 0;
            }
        });
        </script>
        """,
        unsafe_allow_javascript=True
    )


def main() -> None:
    st.set_page_config(
        page_title="Atlas Mundial 2026",
        page_icon=icon,
        layout="wide"
    )

    apply_global_styles()

    selected_page = render_navigation()
    scroll_to_top_on_page_change(selected_page)
    data = load_atlas_data()

    PAGES[selected_page](data)


if __name__ == "__main__":
    main()
