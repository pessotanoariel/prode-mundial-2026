import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --atlas-paper: #F4E8C8;
            --atlas-ink: #171412;
            --atlas-red: #D94B35;
            --atlas-yellow: #F2C230;
            --atlas-green: #008C45;
            --atlas-sky: #4BA3C7;
            --atlas-violet: #4B3B78;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

