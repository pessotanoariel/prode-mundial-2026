import streamlit as st

from app.atlas_app.components.layout import render_page_title


def render(data: dict) -> None:
    render_page_title("Matches")
    st.caption("Placeholder page for match forecast cards.")

