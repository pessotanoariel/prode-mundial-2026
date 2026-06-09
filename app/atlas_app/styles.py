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

        .atlas-analysis-hero {
            border-bottom: 3px solid var(--atlas-ink);
            border-top: 3px solid var(--atlas-ink);
            margin-bottom: 1.5rem;
            padding: 1.25rem 0 1.5rem;
        }

        .atlas-analysis-hero h1 {
            color: var(--atlas-ink);
            font-size: clamp(2.8rem, 7vw, 6rem);
            font-weight: 950;
            letter-spacing: 0;
            line-height: 0.9;
            margin: 0.25rem 0 0.75rem;
            text-transform: uppercase;
        }

        .atlas-analysis-hero p {
            color: var(--atlas-ink);
            font-size: 1.05rem;
            max-width: 48rem;
        }

        .atlas-analysis-hero-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
            margin-top: 1.2rem;
        }

        .atlas-analysis-hero-grid > div {
            border: 2px solid var(--atlas-ink);
            padding: 1.15rem;
        }

        .atlas-analysis-hero-grid > div:first-child {
            background: var(--atlas-yellow);
        }

        .atlas-analysis-hero-grid > div:last-child {
            background: var(--atlas-violet);
            color: var(--atlas-paper);
        }

        .atlas-analysis-team {
            color: var(--atlas-ink);
            font-size: clamp(2.45rem, 5vw, 4.65rem);
            font-weight: 950;
            line-height: 0.96;
            margin-top: 0.35rem;
            text-transform: uppercase;
        }

        .atlas-analysis-percent {
            color: var(--atlas-red);
            font-size: clamp(2.05rem, 3.8vw, 3.4rem);
            font-weight: 950;
            line-height: 1;
            margin-top: 0.25rem;
        }

        .atlas-section-number {
            color: var(--atlas-red);
            font-size: 3.4rem;
            font-weight: 950;
            line-height: 0.9;
            margin-top: 1.4rem;
        }

        .atlas-orbit-row {
            align-items: center;
            border-bottom: 2px solid var(--atlas-ink);
            display: grid;
            gap: 1rem;
            grid-template-columns: 4.25rem minmax(0, 1fr);
            padding: 0.7rem 0;
        }

        .atlas-orbit-rank {
            color: var(--atlas-red);
            font-size: 2.25rem;
            font-weight: 950;
            line-height: 1;
        }

        .atlas-orbit-topline {
            align-items: baseline;
            display: flex;
            gap: 1rem;
            justify-content: space-between;
            margin-bottom: 0.35rem;
        }

        .atlas-orbit-topline span,
        .atlas-orbit-topline strong {
            color: var(--atlas-ink);
            font-weight: 950;
            text-transform: uppercase;
        }

        .atlas-orbit-track {
            background: rgba(23, 20, 18, 0.15);
            border: 1px solid var(--atlas-ink);
            height: 0.72rem;
        }

        .atlas-orbit-bar {
            background: var(--atlas-red);
            height: 100%;
        }

        .atlas-final-card {
            background: rgba(255, 255, 255, 0.18);
            border: 2px solid var(--atlas-ink);
            min-height: 10.5rem;
            padding: 0.95rem;
        }

        .atlas-final-card h3 {
            color: var(--atlas-ink);
            font-size: clamp(1.55rem, 2.6vw, 2.25rem);
            font-weight: 950;
            line-height: 0.98;
            margin: 0.45rem 0;
            text-transform: uppercase;
        }

        .atlas-final-card p {
            color: var(--atlas-ink);
            font-weight: 800;
            margin-bottom: 0;
        }

        .atlas-tier-row {
            align-items: center;
            border-bottom: 2px solid var(--atlas-ink);
            display: flex;
            gap: 0.75rem;
            justify-content: space-between;
            padding: 0.7rem 0;
        }

        .atlas-tier-row strong,
        .atlas-tier-row span {
            color: var(--atlas-ink);
            font-size: 1.05rem;
        }

        .atlas-tier-row em {
            color: var(--atlas-red);
            font-size: 1.65rem;
            font-style: normal;
            font-weight: 950;
            line-height: 1;
        }

        .atlas-tier-row strong {
            flex: 1;
            text-transform: uppercase;
        }

        .atlas-tier-row-featured strong,
        .atlas-tier-row-featured span {
            font-size: 1.2rem;
            font-weight: 950;
        }

        .atlas-tier-row-muted strong,
        .atlas-tier-row-muted span {
            color: rgba(23, 20, 18, 0.76);
        }

        .atlas-narrative-note {
            border-left: 0.45rem solid var(--atlas-red);
            color: var(--atlas-ink);
            font-size: 1.05rem;
            font-weight: 750;
            margin: 0.65rem 0;
            padding: 0.35rem 0 0.35rem 0.75rem;
        }

        .atlas-forecast-note {
            background: var(--atlas-yellow);
            border: 2px solid var(--atlas-ink);
            color: var(--atlas-ink);
            font-weight: 750;
            line-height: 1.45;
            padding: 1rem;
        }

        .atlas-city-summary {
            border-bottom: 3px solid var(--atlas-ink);
            border-top: 3px solid var(--atlas-ink);
            padding: 0.9rem 0;
        }

        .atlas-city-summary-stats {
            display: grid;
            gap: 0.6rem;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin-bottom: 0.85rem;
        }

        .atlas-city-summary-stats div,
        .atlas-city-summary-card {
            background: rgba(255, 255, 255, 0.18);
            border: 2px solid var(--atlas-ink);
            box-sizing: border-box;
            padding: 0.68rem;
        }

        .atlas-city-summary-stats strong {
            color: var(--atlas-red);
            display: block;
            font-size: 2rem;
            font-weight: 950;
            line-height: 1;
        }

        .atlas-city-summary-stats span {
            color: var(--atlas-ink);
            display: block;
            font-size: 0.74rem;
            font-weight: 950;
            letter-spacing: 0.04rem;
            margin-top: 0.18rem;
            text-transform: uppercase;
        }

        .atlas-city-summary-grid {
            display: grid;
            gap: 0.75rem;
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        .atlas-city-summary-card {
            min-height: 8.2rem;
        }

        .atlas-city-summary-card h3,
        .atlas-city-summary-card strong,
        .atlas-city-summary-card span,
        .atlas-city-summary-card small {
            display: block;
        }

        .atlas-city-summary-card h3 {
            color: var(--atlas-ink);
            font-size: 1.12rem;
            font-weight: 950;
            line-height: 1;
            margin: 0.34rem 0 0.35rem;
            text-transform: uppercase;
        }

        .atlas-city-summary-card strong {
            color: var(--atlas-ink);
            font-size: 0.86rem;
            font-weight: 850;
            line-height: 1.12;
        }

        .atlas-city-summary-card span {
            color: var(--atlas-red);
            font-size: 1.15rem;
            font-weight: 950;
            line-height: 1;
            margin-top: 0.5rem;
            text-transform: uppercase;
        }

        .atlas-city-summary-card small {
            color: rgba(23, 20, 18, 0.72);
            font-size: 0.72rem;
            font-weight: 850;
            margin-top: 0.18rem;
            text-transform: uppercase;
        }

        .atlas-city-summary p {
            color: var(--atlas-ink);
            font-size: 0.95rem;
            font-weight: 760;
            line-height: 1.35;
            margin: 0.75rem 0 0;
        }

        .groups-hero {
            border-bottom: 3px solid var(--atlas-ink);
            border-top: 3px solid var(--atlas-ink);
            margin-bottom: 1.5rem;
            padding: 1.25rem 0 1.5rem;
        }

        .groups-hero h1 {
            color: var(--atlas-ink);
            font-size: clamp(2.8rem, 7vw, 6rem);
            font-weight: 950;
            letter-spacing: 0;
            line-height: 0.9;
            margin: 0.25rem 0 0.75rem;
            text-transform: uppercase;
        }

        .groups-hero p {
            color: var(--atlas-ink);
            font-size: 1.05rem;
            max-width: 50rem;
        }

        .groups-hero-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin-top: 1.2rem;
        }

        .groups-hero-grid > div {
            border: 2px solid var(--atlas-ink);
            padding: 0.9rem;
        }

        .groups-hero-grid strong {
            color: var(--atlas-red);
            display: block;
            font-size: 2.5rem;
            font-weight: 950;
            line-height: 1;
            margin-top: 0.35rem;
        }

        .groups-hero-grid span {
            color: var(--atlas-ink);
            display: block;
            font-weight: 850;
            line-height: 1.15;
            margin-top: 0.35rem;
        }

        .groups-dispatch-card {
            background: rgba(255, 255, 255, 0.18);
            border: 2px solid var(--atlas-ink);
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            height: 12.75rem;
            justify-content: space-between;
            margin-bottom: 1rem;
            overflow: hidden;
            padding: 0.8rem;
        }

        .groups-dispatch-letter {
            color: var(--atlas-red);
            font-size: 2.25rem;
            font-weight: 950;
            line-height: 1;
        }

        .groups-dispatch-card h3 {
            color: var(--atlas-ink);
            font-size: 1rem;
            font-weight: 950;
            line-height: 1.1;
            margin: 0.2rem 0 0.45rem;
            overflow: hidden;
            text-overflow: ellipsis;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .groups-dispatch-card ul {
            font-size: 0.8rem;
            line-height: 1.12;
            list-style: none;
            margin: 0.2rem 0 0;
            padding: 0;
        }

        .groups-dispatch-card li {
            color: var(--atlas-ink);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .groups-spread {
            border-top: 3px solid var(--atlas-ink);
            margin-top: 1.75rem;
            padding-top: 0.9rem;
        }

        .groups-spread-heading {
            align-items: baseline;
            display: flex;
            gap: 0.75rem;
            margin-bottom: 0.8rem;
        }

        .groups-spread-heading span {
            color: var(--atlas-red);
            font-size: 0.86rem;
            font-weight: 950;
            letter-spacing: 0.08rem;
        }

        .groups-spread-heading strong {
            color: var(--atlas-ink);
            font-size: 3.4rem;
            font-weight: 950;
            line-height: 0.9;
        }

        [data-testid="stRadio"] {
            margin-bottom: 0.85rem;
        }

        [data-testid="stRadio"] label {
            color: var(--atlas-ink);
            font-weight: 950;
        }

        [data-testid="stRadio"] div[role="radiogroup"] {
            gap: 0.45rem;
        }

        [data-testid="stRadio"] div[role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.18);
            border: 2px solid var(--atlas-ink);
            color: var(--atlas-ink);
            padding: 0.15rem 0.45rem;
        }

        [data-testid="stRadio"] div[role="radiogroup"] label p,
        [data-testid="stRadio"] div[role="radiogroup"] label span {
            color: var(--atlas-ink);
            font-weight: 950;
        }

        .groups-standings,
        .third-race-ranking {
            background: rgba(255, 255, 255, 0.14);
            border-top: 2px solid var(--atlas-ink);
            color: var(--atlas-ink);
            width: 100%;
        }

        .groups-standing-header,
        .groups-standing-row {
            align-items: center;
            display: grid;
            gap: 0.65rem;
            grid-template-columns: 2.5rem minmax(0, 1fr) 2.25rem 2.25rem 2.75rem;
        }

        .groups-standing-header,
        .third-race-header {
            border-bottom: 2px solid var(--atlas-ink);
            color: var(--atlas-red);
            font-size: 0.72rem;
            font-weight: 950;
            letter-spacing: 0.05rem;
            padding: 0.55rem 0.45rem;
            text-transform: uppercase;
        }

        .groups-standing-row {
            border-bottom: 1px solid rgba(23, 20, 18, 0.3);
            font-size: 1rem;
            padding: 0.68rem 0.45rem;
        }

        .groups-standing-rank {
            color: var(--atlas-red);
            font-size: 1.25rem;
            font-weight: 950;
            line-height: 1;
        }

        .groups-standing-team {
            font-weight: 950;
            overflow: hidden;
            text-overflow: ellipsis;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .groups-table,
        .third-race-table {
            border-collapse: collapse;
            color: var(--atlas-ink);
            font-size: 1rem;
            width: 100%;
        }

        .groups-table th,
        .groups-table td,
        .third-race-table th,
        .third-race-table td {
            border-bottom: 1px solid rgba(23, 20, 18, 0.35);
            padding: 0.62rem 0.5rem;
            text-align: left;
        }

        .groups-table th,
        .third-race-table th {
            color: var(--atlas-red);
            font-size: 0.72rem;
            font-weight: 950;
            letter-spacing: 0.05rem;
            text-transform: uppercase;
        }

        .groups-qualified-row {
            background: rgba(0, 140, 69, 0.14);
            font-weight: 850;
        }

        .groups-third-row {
            background: rgba(242, 194, 48, 0.22);
            font-weight: 800;
        }

        .groups-qualifier-list {
            list-style: none;
            margin: 0;
            padding: 0;
        }

        .groups-qualifier-list li {
            border-bottom: 1px solid rgba(23, 20, 18, 0.35);
            padding: 0.55rem 0;
        }

        .groups-qualifier-list strong {
            color: var(--atlas-ink);
            display: block;
            font-weight: 950;
            text-transform: uppercase;
        }

        .groups-qualifier-list span {
            color: var(--atlas-red);
            font-size: 0.75rem;
            font-weight: 850;
            text-transform: uppercase;
        }

        .groups-match-card {
            border-bottom: 2px solid var(--atlas-ink);
            padding: 0.7rem 0;
        }

        .groups-match-card h4 {
            color: var(--atlas-ink);
            font-size: 1.12rem;
            font-weight: 950;
            line-height: 1.1;
            margin: 0.28rem 0;
            text-transform: uppercase;
        }

        .groups-match-card p {
            color: var(--atlas-ink);
            margin: 0;
        }

        .third-qualified {
            background: rgba(0, 140, 69, 0.14);
            font-weight: 850;
        }

        .third-eliminated {
            color: rgba(23, 20, 18, 0.58);
        }

        .third-race-header,
        .third-race-row {
            align-items: center;
            display: grid;
            gap: 0.8rem;
            grid-template-columns: 4rem minmax(0, 1fr) 5.5rem 6.5rem;
        }

        .third-race-row {
            border-bottom: 1px solid rgba(23, 20, 18, 0.3);
            padding: 0.65rem 0.5rem;
        }

        .third-race-rank {
            color: var(--atlas-red);
            font-size: 1.45rem;
            font-weight: 950;
            line-height: 1;
        }

        .third-race-team {
            font-size: 1rem;
            font-weight: 950;
            overflow: hidden;
            text-overflow: ellipsis;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .third-race-points {
            font-weight: 900;
        }

        .third-race-status {
            font-size: 0.76rem;
            font-weight: 950;
            letter-spacing: 0.04rem;
        }

        .third-cutoff {
            background: var(--atlas-red);
            color: var(--atlas-paper);
            font-size: 0.75rem;
            font-weight: 950;
            letter-spacing: 0.08rem;
            padding: 0.35rem;
            text-align: center;
            text-transform: uppercase;
        }

        .bracket-hero {
            border-bottom: 3px solid var(--atlas-ink);
            border-top: 3px solid var(--atlas-ink);
            margin-bottom: 1.5rem;
            padding: 1.25rem 0 1.5rem;
        }

        .bracket-hero h1 {
            color: var(--atlas-ink);
            font-size: clamp(2.8rem, 7vw, 6rem);
            font-weight: 950;
            letter-spacing: 0;
            line-height: 0.9;
            margin: 0.25rem 0 0.75rem;
            text-transform: uppercase;
        }

        .bracket-hero p {
            color: var(--atlas-ink);
            font-size: 1.05rem;
            max-width: 52rem;
        }

        .bracket-hero-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: minmax(0, 1.1fr) minmax(0, 1.35fr) minmax(0, 0.7fr);
            margin-top: 1.2rem;
        }

        .bracket-hero-grid > div {
            border: 2px solid var(--atlas-ink);
            padding: 1rem;
        }

        .bracket-hero-grid strong,
        .bracket-hero-grid span {
            color: var(--atlas-ink);
            display: block;
            font-size: clamp(1.45rem, 3vw, 2.6rem);
            font-weight: 950;
            line-height: 0.98;
            margin-top: 0.35rem;
            text-transform: uppercase;
        }

        .bracket-round-title {
            background: var(--atlas-yellow);
            border: 2px solid var(--atlas-ink);
            margin-bottom: 0.7rem;
            padding: 0.45rem 0.55rem;
        }

        .bracket-round-title span {
            color: var(--atlas-ink);
            font-size: 0.88rem;
            font-weight: 950;
            letter-spacing: 0.04rem;
            text-transform: uppercase;
        }

        .bracket-match-card {
            background: rgba(255, 255, 255, 0.16);
            border: 2px solid var(--atlas-ink);
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            height: 9.35rem;
            justify-content: space-between;
            margin-bottom: 0.65rem;
            overflow: hidden;
            padding: 0.7rem;
        }

        .bracket-card-teams {
            color: var(--atlas-ink);
            font-size: 0.92rem;
            font-weight: 950;
            line-height: 1.08;
            text-transform: uppercase;
        }

        .bracket-card-teams div {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .bracket-card-teams span {
            color: var(--atlas-red);
            display: block;
            font-size: 0.7rem;
            font-weight: 950;
            margin: 0.12rem 0;
        }

        .bracket-card-venue {
            color: rgba(23, 20, 18, 0.72);
            font-size: 0.68rem;
            font-weight: 850;
            line-height: 1.05;
            margin-top: 0.18rem;
            overflow: hidden;
            text-overflow: ellipsis;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .bracket-card-footer {
            border-top: 1px solid rgba(23, 20, 18, 0.38);
            display: grid;
            gap: 0.3rem;
            grid-template-columns: auto minmax(0, 1fr) auto;
            padding-top: 0.45rem;
        }

        .bracket-card-footer strong {
            color: var(--atlas-red);
            font-size: 1.15rem;
            font-weight: 950;
            line-height: 1;
        }

        .bracket-card-footer span {
            color: var(--atlas-ink);
            font-size: 0.76rem;
            font-weight: 900;
            overflow: hidden;
            text-overflow: ellipsis;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .bracket-card-footer em {
            color: var(--atlas-ink);
            font-size: 0.68rem;
            font-style: normal;
            font-weight: 950;
            text-transform: uppercase;
        }

        .bracket-final-poster {
            background: var(--atlas-violet);
            border: 3px solid var(--atlas-ink);
            color: var(--atlas-paper);
            margin-bottom: 1rem;
            padding: 1.25rem;
        }

        .bracket-final-poster h2 {
            color: var(--atlas-paper);
            font-size: clamp(2.6rem, 7vw, 6rem);
            font-weight: 950;
            line-height: 0.9;
            margin: 0.4rem 0;
            text-transform: uppercase;
        }

        .bracket-final-poster h2 span {
            color: var(--atlas-yellow);
            display: block;
            font-size: 1.2rem;
            letter-spacing: 0.1rem;
            margin: 0.35rem 0;
        }

        .bracket-final-score {
            color: var(--atlas-yellow);
            font-size: clamp(2rem, 5vw, 4rem);
            font-weight: 950;
            line-height: 1;
        }

        .bracket-final-venue {
            color: var(--atlas-paper);
            font-size: 0.9rem;
            font-weight: 850;
            margin: 0.35rem 0 0.55rem;
            text-transform: uppercase;
        }

        .bracket-champion-call {
            border-top: 2px solid var(--atlas-paper);
            font-size: 1.1rem;
            font-weight: 850;
            margin-top: 0.8rem;
            padding-top: 0.8rem;
        }

        .bracket-champion-call strong {
            color: var(--atlas-yellow);
            text-transform: uppercase;
        }

        .bracket-third-place {
            max-width: 28rem;
        }

        .matches-hero {
            border-bottom: 3px solid var(--atlas-ink);
            border-top: 3px solid var(--atlas-ink);
            margin-bottom: 1.5rem;
            padding: 1.25rem 0 1.5rem;
        }

        .matches-hero h1 {
            color: var(--atlas-ink);
            font-size: clamp(2.8rem, 7vw, 6rem);
            font-weight: 950;
            letter-spacing: 0;
            line-height: 0.9;
            margin: 0.25rem 0 0.75rem;
            text-transform: uppercase;
        }

        .matches-hero p {
            color: var(--atlas-ink);
            font-size: 1.05rem;
            max-width: 52rem;
        }

        .matches-hero-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
            margin-top: 1.2rem;
        }

        .matches-hero-grid > div {
            border: 2px solid var(--atlas-ink);
            padding: 1rem;
        }

        .matches-hero-grid strong,
        .matches-hero-grid span {
            color: var(--atlas-ink);
            display: block;
            font-size: clamp(1.45rem, 3vw, 2.8rem);
            font-weight: 950;
            line-height: 1;
            margin-top: 0.35rem;
            text-transform: uppercase;
        }

        .match-index-panel {
            background: rgba(255, 255, 255, 0.14);
            border-bottom: 2px solid var(--atlas-ink);
            border-top: 2px solid var(--atlas-ink);
            margin-bottom: 0.9rem;
            padding: 0.75rem 0.65rem 0.1rem;
        }

        .match-index-panel label {
            color: var(--atlas-ink);
            font-weight: 950;
        }

        .match-filter-label {
            color: var(--atlas-red);
            font-size: 0.74rem;
            font-weight: 950;
            letter-spacing: 0.06rem;
            line-height: 1;
            margin-bottom: 0.22rem;
            text-transform: uppercase;
        }

        .match-forecast-card {
            background: rgba(255, 255, 255, 0.16);
            border: 2px solid var(--atlas-ink);
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            height: 14.75rem;
            justify-content: space-between;
            margin-bottom: 0.8rem;
            overflow: hidden;
            padding: 0.78rem;
        }

        .match-card-date {
            color: var(--atlas-red);
            font-size: 0.72rem;
            font-weight: 950;
            letter-spacing: 0.06rem;
            text-transform: uppercase;
        }

        .match-forecast-card h3 {
            color: var(--atlas-ink);
            font-size: clamp(1.12rem, 2vw, 1.55rem);
            font-weight: 950;
            line-height: 1;
            margin: 0.32rem 0;
            text-transform: uppercase;
        }

        .match-forecast-card h3 span {
            color: var(--atlas-red);
            display: block;
            font-size: 0.7rem;
            letter-spacing: 0.08rem;
            margin: 0.18rem 0;
        }

        .match-card-score {
            color: var(--atlas-red);
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 950;
            line-height: 1;
        }

        .match-card-venue {
            color: rgba(23, 20, 18, 0.72);
            font-size: 0.72rem;
            font-weight: 850;
            line-height: 1.12;
            overflow: hidden;
            text-overflow: ellipsis;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .match-card-winner {
            color: var(--atlas-ink);
            font-size: 0.84rem;
            font-weight: 800;
        }

        .match-card-winner strong {
            text-transform: uppercase;
        }

        .match-card-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 0.3rem;
        }

        .match-card-badges span {
            border: 2px solid var(--atlas-ink);
            color: var(--atlas-ink);
            font-size: 0.64rem;
            font-weight: 950;
            letter-spacing: 0.04rem;
            padding: 0.08rem 0.28rem;
            text-transform: uppercase;
        }

        .match-callout {
            border-bottom: 2px solid var(--atlas-ink);
            color: var(--atlas-ink);
            padding: 0.75rem 0;
        }

        .match-callout strong {
            display: block;
            font-size: 1.25rem;
            font-weight: 950;
            line-height: 1.05;
            text-transform: uppercase;
        }

        .match-callout span {
            display: block;
            font-weight: 850;
            margin-top: 0.25rem;
        }

        .match-callout small {
            color: rgba(23, 20, 18, 0.72);
            display: block;
            font-size: 0.72rem;
            font-weight: 850;
            margin-top: 0.18rem;
            text-transform: uppercase;
        }

        .match-callout-yellow {
            background: rgba(242, 194, 48, 0.16);
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }

        .method-hero {
            border-bottom: 3px solid var(--atlas-ink);
            border-top: 3px solid var(--atlas-ink);
            margin-bottom: 1.5rem;
            padding: 1.25rem 0 1.5rem;
        }

        .method-hero h1 {
            color: var(--atlas-ink);
            font-size: clamp(2.8rem, 7vw, 6rem);
            font-weight: 950;
            letter-spacing: 0;
            line-height: 0.9;
            margin: 0.25rem 0 0.75rem;
            text-transform: uppercase;
        }

        .method-hero p {
            color: var(--atlas-ink);
            font-size: 1.05rem;
            max-width: 52rem;
        }

        .method-card {
            background: rgba(255, 255, 255, 0.16);
            border: 2px solid var(--atlas-ink);
            box-sizing: border-box;
            display: grid;
            gap: 0.55rem;
            grid-template-columns: 3.2rem minmax(0, 1fr);
            margin-bottom: 0.9rem;
            min-height: 8.6rem;
            padding: 0.9rem;
        }

        .method-card-number {
            color: var(--atlas-red);
            font-size: 2rem;
            font-weight: 950;
            line-height: 1;
        }

        .method-card h3 {
            color: var(--atlas-ink);
            font-size: 1.2rem;
            font-weight: 950;
            line-height: 1;
            margin: 0;
            text-transform: uppercase;
        }

        .method-card p {
            color: var(--atlas-ink);
            font-weight: 760;
            grid-column: 2;
            line-height: 1.35;
            margin: 0;
        }

        .method-flow {
            align-items: stretch;
            display: grid;
            gap: 0.45rem;
            grid-template-columns: repeat(11, auto);
            margin: 0.6rem 0 1rem;
            overflow-x: auto;
        }

        .method-flow div {
            background: var(--atlas-yellow);
            border: 2px solid var(--atlas-ink);
            color: var(--atlas-ink);
            font-size: 0.78rem;
            font-weight: 950;
            min-width: 8rem;
            padding: 0.45rem 0.55rem;
            text-align: center;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .method-flow span {
            align-self: center;
            background: var(--atlas-red);
            display: block;
            height: 0.2rem;
            width: 1.2rem;
        }

        .method-editorial-note {
            background: var(--atlas-violet);
            border: 3px solid var(--atlas-ink);
            color: var(--atlas-paper);
            padding: 1.1rem;
        }

        .method-editorial-note strong {
            color: var(--atlas-yellow);
            display: block;
            font-size: clamp(1.6rem, 3vw, 2.7rem);
            font-weight: 950;
            line-height: 0.95;
            margin-bottom: 0.6rem;
            text-transform: uppercase;
        }

        .method-editorial-note p {
            color: var(--atlas-paper);
            font-size: 1.05rem;
            font-weight: 760;
            line-height: 1.45;
            margin: 0;
            max-width: 62rem;
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

        .atlas-team-name {
            align-items: center;
            color: inherit;
            display: inline-flex;
            gap: 0.38em;
            max-width: 100%;
            min-width: 0;
            vertical-align: -0.08em;
        }

        .atlas-team-name > span {
            color: inherit !important;
            display: inline !important;
            font-size: inherit !important;
            font-weight: inherit !important;
            letter-spacing: 0 !important;
            margin: 0 !important;
            min-width: 0;
            overflow: hidden;
            text-overflow: ellipsis;
            text-transform: inherit !important;
            white-space: nowrap;
        }

        .atlas-team-flag {
            aspect-ratio: 3 / 2;
            border: 1px solid rgba(23, 20, 18, 0.38);
            box-shadow: 0 0 0 1px rgba(244, 232, 200, 0.28);
            flex: 0 0 auto;
            height: 0.86em;
            object-fit: cover;
            width: 1.29em;
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

            .atlas-analysis-hero-grid {
                grid-template-columns: 1fr;
            }

            .groups-hero-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .bracket-hero-grid {
                grid-template-columns: 1fr;
            }

            .matches-hero-grid {
                grid-template-columns: 1fr;
            }

            .atlas-city-summary-stats,
            .atlas-city-summary-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
