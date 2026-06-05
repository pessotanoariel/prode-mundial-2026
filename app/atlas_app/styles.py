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

        .stApp {
            background: var(--atlas-paper);
            color: var(--atlas-ink);
        }

        .atlas-kicker {
            color: var(--atlas-red);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08rem;
            text-transform: uppercase;
        }

        .atlas-hero {
            border: 3px solid var(--atlas-ink);
            background:
                linear-gradient(135deg, rgba(217, 75, 53, 0.18) 0 25%, transparent 25% 50%, rgba(75, 163, 199, 0.18) 50% 75%, transparent 75%),
                var(--atlas-paper);
            padding: 2rem;
            margin-bottom: 1.25rem;
        }

        .atlas-hero h1 {
            color: var(--atlas-ink);
            font-size: clamp(3.2rem, 9vw, 7rem);
            font-weight: 950;
            letter-spacing: 0;
            line-height: 0.88;
            margin: 0.2rem 0 1rem;
            text-transform: uppercase;
        }

        .atlas-deck {
            color: var(--atlas-ink);
            font-size: 1.1rem;
            max-width: 54rem;
        }

        .atlas-hero-strip {
            display: grid;
            gap: 1rem;
            grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
            margin-top: 1.5rem;
        }

        .atlas-hero-favorite,
        .atlas-hero-final {
            border: 2px solid var(--atlas-ink);
            padding: 1rem;
        }

        .atlas-hero-favorite {
            background: var(--atlas-yellow);
        }

        .atlas-hero-final {
            background: var(--atlas-violet);
            color: var(--atlas-paper);
        }

        .atlas-hero-team {
            font-size: clamp(2.25rem, 5vw, 4.5rem);
            font-weight: 950;
            line-height: 0.95;
            margin-top: 0.4rem;
            text-transform: uppercase;
        }

        .atlas-hero-percent {
            color: var(--atlas-red);
            font-size: clamp(1.8rem, 4vw, 3.2rem);
            font-weight: 950;
            line-height: 1;
            margin-top: 0.25rem;
        }

        .atlas-panel {
            border: 2px solid var(--atlas-ink);
            background: rgba(255, 255, 255, 0.22);
            padding: 1rem;
            min-height: 100%;
        }

        .atlas-panel-red {
            background: var(--atlas-red);
            color: var(--atlas-paper);
        }

        .atlas-panel-yellow {
            background: var(--atlas-yellow);
            color: var(--atlas-ink);
        }

        .atlas-panel-green {
            background: var(--atlas-green);
            color: var(--atlas-paper);
        }

        .atlas-panel-violet {
            background: var(--atlas-violet);
            color: var(--atlas-paper);
        }

        .atlas-rank {
            align-items: baseline;
            border-bottom: 2px solid var(--atlas-ink);
            display: flex;
            gap: 1rem;
            justify-content: space-between;
            padding: 0.65rem 0;
        }

        .atlas-rank-number {
            color: var(--atlas-red);
            font-size: 2.1rem;
            font-weight: 950;
            line-height: 1;
        }

        .atlas-rank-team {
            flex: 1;
            font-size: 1.25rem;
            font-weight: 850;
            text-transform: uppercase;
        }

        .atlas-rank-value {
            font-size: 1.4rem;
            font-weight: 950;
        }

        .atlas-group-card {
            border: 2px solid var(--atlas-ink);
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            height: 11.25rem;
            justify-content: flex-start;
            overflow: hidden;
            padding: 0.75rem;
            background: rgba(255, 255, 255, 0.18);
        }

        .atlas-group-letter {
            color: var(--atlas-red);
            font-size: 2.1rem;
            font-weight: 950;
            line-height: 1;
        }

        .atlas-group-body {
            display: flex;
            flex: 1;
            flex-direction: column;
            justify-content: space-between;
            min-height: 0;
        }

        .atlas-group-body h4 {
            font-size: 0.96rem;
            line-height: 1.15;
            margin: 0.2rem 0 0.45rem;
        }

        .atlas-group-body ul {
            font-size: 0.82rem;
            line-height: 1.15;
            list-style: none;
            margin: 0.2rem 0 0;
            padding: 0;
        }

        .atlas-group-body li {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .atlas-more-qualifiers {
            color: var(--atlas-red);
            font-size: 0.76rem;
            font-weight: 850;
            margin-top: 0.12rem;
        }

        .atlas-small-label {
            font-size: 0.72rem;
            font-weight: 850;
            letter-spacing: 0.06rem;
            text-transform: uppercase;
        }

        .atlas-sidebar-brand {
            border-bottom: 3px solid var(--atlas-ink);
            border-top: 3px solid var(--atlas-ink);
            margin: 0 0 1.25rem;
            padding: 1rem 0;
        }

        .atlas-sidebar-kicker {
            color: var(--atlas-red);
            font-size: 0.78rem;
            font-weight: 900;
            letter-spacing: 0.08rem;
            text-transform: uppercase;
        }

        .atlas-sidebar-title {
            color: var(--atlas-ink);
            font-size: 2rem;
            font-weight: 950;
            letter-spacing: 0;
            line-height: 0.9;
            text-transform: uppercase;
        }

        .atlas-sidebar-year {
            background: var(--atlas-yellow);
            border: 2px solid var(--atlas-ink);
            color: var(--atlas-ink);
            display: inline-block;
            font-size: 1.15rem;
            font-weight: 950;
            margin-top: 0.55rem;
            padding: 0.05rem 0.35rem;
        }

        .atlas-sidebar-deck {
            color: var(--atlas-ink);
            font-size: 0.85rem;
            line-height: 1.2;
            margin-top: 0.7rem;
        }

        [data-testid="stSidebar"] {
            background: var(--atlas-paper);
        }

        [data-testid="stSidebar"],
        [data-testid="stSidebar"] * {
            color: var(--atlas-ink);
        }

        [data-testid="stSidebar"] .atlas-sidebar-kicker {
            color: var(--atlas-red);
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: var(--atlas-ink);
        }

        @media (max-width: 760px) {
            .atlas-hero-strip {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
