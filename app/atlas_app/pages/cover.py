import streamlit as st

from app.atlas_app.components.layout import render_page_title


def render(data: dict) -> None:
    render_page_title("Cover")
    st.caption("World Cup Forecast Atlas 2026")

