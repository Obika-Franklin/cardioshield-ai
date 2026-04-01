import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #08111f 0%, #0d1726 45%, #0f1d31 100%);
            color: #f5f7fb;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 1rem;
            border-radius: 18px;
        }
        .hero-card, .feature-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 22px;
            padding: 1.3rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
        }
        .risk-pill {
            display: inline-block;
            padding: 0.55rem 1rem;
            border-radius: 999px;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin-bottom: 1rem;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
        }
        .muted {
            color: #c8d3e3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero_section():
    st.markdown(
        """
        <div class="hero-card">
            <h1 style="margin-bottom:0.4rem;">CardioShield AI</h1>
            <p class="muted" style="font-size:1.1rem; margin-top:0;">
                A multimodal cardiovascular screening MVP built to look credible in front of investors, clinicians, and technical reviewers.
            </p>
            <p style="font-size:1rem; line-height:1.7;">
                The app combines structured patient data and ECG image analysis into a single, premium decision-support workflow.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_cards():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card"><h4>Clinical Engine</h4><p>Random Forest risk scoring from tabular patient variables.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card"><h4>ECG Vision Engine</h4><p>VGG16-based ECG image inference for multimodal screening.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card"><h4>Investor-grade UI</h4><p>Clean visual framing for demos, accelerators, and pilot conversations.</p></div>', unsafe_allow_html=True)


def result_badge(text: str):
    st.markdown(f'<div class="risk-pill">{text}</div>', unsafe_allow_html=True)


def probability_bar(value: float):
    st.progress(max(0.0, min(1.0, float(value))))


def disclaimer_box():
    st.warning("CardioShield AI is a screening and decision-support MVP. It does not replace medical diagnosis, emergency triage, or professional clinical judgment.")


def metric_strip(items):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)
