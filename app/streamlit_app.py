import sys
from pathlib import Path

import streamlit as st


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
    "Cover": cover.render,
    "Atlas": atlas.render,
    "Groups": groups.render,
    "Bracket": bracket.render,
    "Matches": matches.render,
    "Method": method.render,
}


def render_navigation() -> str:
    st.sidebar.title("Forecast Atlas 2026")
    st.sidebar.caption("A simulated tournament magazine")

    return st.sidebar.radio(
        "Sections",
        list(PAGES.keys()),
        label_visibility="collapsed"
    )


def main() -> None:
    st.set_page_config(
        page_title="World Cup Forecast Atlas 2026",
        page_icon="⚽",
        layout="wide"
    )

    apply_global_styles()

    selected_page = render_navigation()
    data = load_atlas_data()

    PAGES[selected_page](data)


if __name__ == "__main__":
    main()
