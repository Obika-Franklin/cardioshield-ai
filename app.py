import streamlit as st
from utils.predictors import predict_tabular, predict_ecg, combine_predictions

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="CardioShield AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# SESSION STATE
# =========================
if "tabular_result" not in st.session_state:
    st.session_state.tabular_result = None

if "ecg_result" not in st.session_state:
    st.session_state.ecg_result = None

if "selected_demo_profile" not in st.session_state:
    st.session_state.selected_demo_profile = "default"


# =========================
# STYLING
# =========================
st.markdown("""
<style>
:root {
    --bg: #f4f7fb;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --border: #dbe4f0;
    --navy: #082a4d;
    --navy-2: #0b355f;
    --teal: #2ec4b6;
    --teal-dark: #1fa79a;
    --soft: #edf5ff;
    --danger: #ef4444;
    --warning: #f59e0b;
    --success: #10b981;
}

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: var(--bg);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1380px;
}

section[data-testid="stSidebar"] {
    display: none !important;
}

div[data-testid="stVerticalBlock"] > div:has(.top-hero) {
    margin-bottom: 1rem;
}

.top-hero {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%);
    border-radius: 24px;
    padding: 1.4rem 1.6rem 1.3rem 1.6rem;
    color: white;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 30px rgba(8,42,77,0.16);
}

.hero-grid {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: flex-start;
    flex-wrap: wrap;
}

.brand-wrap {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.brand-icon {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    background: linear-gradient(135deg, #2ec4b6 0%, #67e8f9 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.25);
}

.brand-title {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.05;
    margin: 0;
}

.brand-subtitle {
    margin-top: 0.25rem;
    font-size: 1rem;
    color: rgba(255,255,255,0.88);
}

.badge-row {
    margin-top: 0.75rem;
    display: flex;
    gap: 0.55rem;
    flex-wrap: wrap;
}

.badge {
    display: inline-block;
    background: rgba(46,196,182,0.16);
    color: #b7fff7;
    border: 1px solid rgba(46,196,182,0.35);
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 700;
}

.hero-actions {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    flex-wrap: wrap;
}

.hero-mini {
    text-align: right;
    color: rgba(255,255,255,0.9);
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

.early-access {
    font-weight: 800;
    color: #87f8e5;
    margin-left: 0.35rem;
}

.metric-grid {
    margin-top: 1rem;
}

.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 1rem 1.1rem;
    min-height: 106px;
}

.metric-label {
    color: rgba(255,255,255,0.78);
    font-size: 0.95rem;
    margin-top: 0.2rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: white;
    line-height: 1.05;
}

.metric-icon {
    font-size: 1.2rem;
    opacity: 0.9;
    margin-bottom: 0.25rem;
}

.nav-shell {
    margin-top: 1.2rem;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 0.4rem;
    box-shadow: 0 8px 24px rgba(15,23,42,0.05);
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.4rem;
    box-shadow: 0 10px 30px rgba(15,23,42,0.05);
}

.card-tight {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1rem 1.1rem;
    box-shadow: 0 8px 24px rgba(15,23,42,0.04);
}

.card-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 0.3rem;
}

.card-subtitle {
    color: var(--muted);
    font-size: 0.96rem;
    margin-bottom: 0.8rem;
}

.section-title {
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 0.3rem;
}

.section-subtitle {
    color: var(--muted);
    margin-bottom: 1.2rem;
}

.soft-badge {
    display: inline-block;
    background: #dff8f4;
    color: #0f766e;
    border-radius: 999px;
    padding: 0.35rem 0.7rem;
    font-size: 0.84rem;
    font-weight: 800;
    margin-bottom: 0.9rem;
}

.upload-shell {
    border: 2px dashed #cfd9e6;
    background: #fbfdff;
    border-radius: 22px;
    padding: 2rem 1rem;
    text-align: center;
}

.result-box-low {
    background: #ecfdf5;
    border: 1px solid #bbf7d0;
    border-radius: 18px;
    padding: 1rem;
}

.result-box-medium {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 18px;
    padding: 1rem;
}

.result-box-high {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 18px;
    padding: 1rem;
}

.disclaimer {
    background: #fff7ed;
    border: 1px solid #fdba74;
    border-left: 6px solid #f97316;
    border-radius: 18px;
    padding: 1rem;
    color: #7c2d12;
}

.investor-box {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: 0 10px 24px rgba(15,23,42,0.04);
}

.stButton > button {
    border-radius: 14px;
    border: 1px solid var(--border);
    padding: 0.62rem 1rem;
    font-weight: 700;
    background: white;
    color: var(--text);
}

.stDownloadButton > button {
    border-radius: 14px;
    font-weight: 700;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    border-radius: 14px !important;
}

div.row-widget.stRadio > div {
    gap: 0.75rem;
}

div[role="radiogroup"] label {
    background: transparent !important;
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--border);
    padding: 1rem;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(15,23,42,0.04);
}

hr {
    margin-top: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# =========================
# HELPERS
# =========================
def format_probability(prob: float) -> str:
    return f"{prob:.2%}"

def risk_recommendation(risk_label: str) -> str:
    if risk_label == "Low Risk":
        return "Current screening result suggests lower immediate risk. Maintain healthy habits and continue routine monitoring."
    elif risk_label == "Medium Risk":
        return "This screening indicates moderate risk. A clinician review and additional cardiovascular evaluation are advisable."
    return "This screening indicates elevated cardiovascular risk. Prompt medical follow-up is strongly recommended."

def result_box_class(risk_label: str) -> str:
    if risk_label == "Low Risk":
        return "result-box-low"
    elif risk_label == "Medium Risk":
        return "result-box-medium"
    return "result-box-high"

def load_demo_profile(profile_name: str):
    profiles = {
        "default": {
            "age": 45,
            "sex": 1,
            "chest pain type": 3,
            "resting bp s": 120,
            "cholesterol": 200,
            "fasting blood sugar": 0,
            "resting ecg": 1,
            "max heart rate": 150,
            "exercise angina": 0,
            "oldpeak": 1.0,
            "ST slope": 2,
        },
        "low": {
            "age": 34,
            "sex": 0,
            "chest pain type": 2,
            "resting bp s": 112,
            "cholesterol": 176,
            "fasting blood sugar": 0,
            "resting ecg": 0,
            "max heart rate": 168,
            "exercise angina": 0,
            "oldpeak": 0.4,
            "ST slope": 2,
        },
        "high": {
            "age": 61,
            "sex": 1,
            "chest pain type": 4,
            "resting bp s": 158,
            "cholesterol": 286,
            "fasting blood sugar": 1,
            "resting ecg": 2,
            "max heart rate": 108,
            "exercise angina": 1,
            "oldpeak": 2.8,
            "ST slope": 1,
        }
    }
    return profiles.get(profile_name, profiles["default"])

def render_hero():
    st.markdown("""
    <div class="top-hero">
        <div class="hero-grid">
            <div>
                <div class="brand-wrap">
                    <div class="brand-icon">🛡️</div>
                    <div>
                        <h1 class="brand-title">CardioShield AI</h1>
                        <div class="brand-subtitle">
                            Cardiovascular Risk Prediction
                        </div>
                        <div class="badge-row">
                            <span class="badge">RF+SMOTE 92.02%</span>
                            <span class="badge">VGG16 74.83%</span>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <div class="hero-mini">
                    0 of 50 signups <span class="early-access">EARLY ACCESS</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <div class="metric-value">92.02%</div>
            <div class="metric-label">RF + SMOTE Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">📈</div>
            <div class="metric-value">74.83%</div>
            <div class="metric-label">VGG16 ECG Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">⏱️</div>
            <div class="metric-value">&lt;2s</div>
            <div class="metric-label">Response Time</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🗂️</div>
            <div class="metric-value">1.2K</div>
            <div class="metric-label">Patient Records</div>
        </div>
        """, unsafe_allow_html=True)

def render_nav():
    st.markdown('<div class="nav-shell">', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Dual Mode (Data + ECG)", "ECG-Only Mode", "Data-Only Mode", "Investor Brief"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return page

def render_result_summary(result):
    css_class = result_box_class(result["risk_label"])
    st.markdown(
        f"""
        <div class="{css_class}">
            <div style="font-weight:800; font-size:1.05rem; margin-bottom:0.45rem;">
                Clinical Interpretation
            </div>
            <div style="color:#334155;">
                {risk_recommendation(result["risk_label"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# TOP HERO
# =========================
render_hero()

top_a, top_b = st.columns([8, 2])
with top_b:
    st.link_button("View Investor Brief", "#investor-brief", use_container_width=True)

page = render_nav()

st.markdown("")


# =========================
# DUAL MODE
# =========================
if page == "Dual Mode (Data + ECG)":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Dual Screening Workspace</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Run structured patient risk screening and ECG image analysis together for an investor-ready multimodal demo.</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1, 1], gap="large")

    # -------- Left: Tabular --------
    with left:
        st.markdown('<div class="card-tight">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Patient Vitals</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-subtitle">Structured data from the Heart Statlog Cleveland Hungary dataset with 11 clinical features.</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="soft-badge">RF + SMOTE</div>', unsafe_allow_html=True)

        d1, d2, d3 = st.columns([1, 1, 1])
        with d2:
            if st.button("Load Low Risk", use_container_width=True):
                st.session_state.selected_demo_profile = "low"
        with d3:
            if st.button("Load High Risk", use_container_width=True):
                st.session_state.selected_demo_profile = "high"

        demo = load_demo_profile(st.session_state.selected_demo_profile)

        with st.form("dual_clinical_form"):
            a1, a2 = st.columns(2)
            with a1:
                patient_name = st.text_input("Patient ID / Name", placeholder="Enter patient ID")
                age = st.number_input("Age", min_value=1, max_value=120, value=int(demo["age"]))
                sex = st.selectbox("Sex", [0, 1], index=[0, 1].index(demo["sex"]), format_func=lambda x: "Female" if x == 0 else "Male")
                chest_pain_type = st.selectbox("Chest Pain Type", [1, 2, 3, 4], index=[1, 2, 3, 4].index(demo["chest pain type"]))
                resting_bp_s = st.number_input("Resting BP", min_value=50, max_value=250, value=int(demo["resting bp s"]))
                cholesterol = st.number_input("Cholesterol", min_value=50, max_value=700, value=int(demo["cholesterol"]))

            with a2:
                fasting_blood_sugar = st.selectbox("Fasting Blood Sugar", [0, 1], index=[0, 1].index(demo["fasting blood sugar"]))
                resting_ecg = st.selectbox("Resting ECG", [0, 1, 2], index=[0, 1, 2].index(demo["resting ecg"]))
                max_heart_rate = st.number_input("Max Heart Rate", min_value=50, max_value=250, value=int(demo["max heart rate"]))
                exercise_angina = st.selectbox("Exercise Angina", [0, 1], index=[0, 1].index(demo["exercise angina"]))
                oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, value=float(demo["oldpeak"]), step=0.1)
                st_slope = st.selectbox("ST Slope", [1, 2, 3], index=[1, 2, 3].index(demo["ST slope"]))

            submitted_dual = st.form_submit_button("Run Clinical Screening", use_container_width=True)

        if submitted_dual:
            input_data = {
                "age": age,
                "sex": sex,
                "chest pain type": chest_pain_type,
                "resting bp s": resting_bp_s,
                "cholesterol": cholesterol,
                "fasting blood sugar": fasting_blood_sugar,
                "resting ecg": resting_ecg,
                "max heart rate": max_heart_rate,
                "exercise angina": exercise_angina,
                "oldpeak": oldpeak,
                "ST slope": st_slope
            }
            result = predict_tabular(input_data)
            st.session_state.tabular_result = result

        if st.session_state.tabular_result is not None:
            result = st.session_state.tabular_result
            st.markdown("")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Predicted Class", result["prediction"])
            with m2:
                st.metric("Risk Category", result["risk_label"])
            with m3:
                st.metric("Risk Probability", format_probability(result["probability"]))

            render_result_summary(result)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- Right: ECG --------
    with right:
        st.markdown('<div class="card-tight">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">ECG Image Source</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-subtitle">Upload a standard 12-lead ECG image or use a sample for CNN-based screening.</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="upload-shell">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload ECG Image",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed"
        )
        st.markdown("Drag and drop your ECG image here", unsafe_allow_html=True)
        st.caption("Accepted formats: PNG, JPG, JPEG")
        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded ECG", use_container_width=True)

            if st.button("Analyze ECG", use_container_width=True):
                result = predict_ecg(uploaded_file)
                st.session_state.ecg_result = result

        if st.session_state.ecg_result is not None:
            ecg = st.session_state.ecg_result
            if ecg.get("success"):
                e1, e2 = st.columns(2)
                with e1:
                    st.metric("Predicted ECG Class", ecg["class_name"])
                with e2:
                    st.metric("Confidence", format_probability(ecg["confidence"]))

                st.info(
                    "The ECG image has been processed by the CNN screening model. This is a decision-support output, not a final diagnosis."
                )
            else:
                st.warning("ECG analysis is currently unavailable. Clinical screening remains active.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="disclaimer"><strong>Clinical disclaimer:</strong> This MVP is intended for educational screening and decision support only. It does not replace clinician judgment, diagnostic testing, or formal cardiology review.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# ECG ONLY
# =========================
elif page == "ECG-Only Mode":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">ECG-Only Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Use the VGG16 image model independently to assess uploaded ECG images.</div>', unsafe_allow_html=True)

    ecg_left, ecg_right = st.columns([1.15, 0.85], gap="large")

    with ecg_left:
        st.markdown('<div class="card-tight">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Upload ECG Image</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Best results come from clear, upright ECG images with minimal shadows or blur.</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("ECG Upload", type=["png", "jpg", "jpeg"], key="ecg_only_upload")

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded ECG", use_container_width=True)
            if st.button("Run ECG Analysis", use_container_width=True):
                result = predict_ecg(uploaded_file)
                st.session_state.ecg_result = result

        st.markdown('</div>', unsafe_allow_html=True)

    with ecg_right:
        st.markdown('<div class="card-tight">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">ECG Result</div>', unsafe_allow_html=True)

        if st.session_state.ecg_result is not None:
            result = st.session_state.ecg_result
            if result.get("success"):
                st.metric("Predicted ECG Class", result["class_name"])
                st.metric("Confidence", format_probability(result["confidence"]))
                st.info("This output should be reviewed alongside patient history and expert ECG interpretation.")
            else:
                st.warning("ECG analysis is currently unavailable.")
        else:
            st.write("No ECG result available yet.")

        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# DATA ONLY
# =========================
elif page == "Data-Only Mode":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Data-Only Clinical Risk Screening</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Use structured patient variables alone to generate cardiovascular risk screening results.</div>', unsafe_allow_html=True)

    with st.form("data_only_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            age = st.number_input("Age", min_value=1, max_value=120, value=45, key="data_age")
            sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male", key="data_sex")
            chest_pain_type = st.selectbox("Chest Pain Type", [1, 2, 3, 4], key="data_cpt")
            resting_bp_s = st.number_input("Resting BP", min_value=50, max_value=250, value=120, key="data_bp")

        with c2:
            cholesterol = st.number_input("Cholesterol", min_value=50, max_value=700, value=200, key="data_chol")
            fasting_blood_sugar = st.selectbox("Fasting Blood Sugar", [0, 1], key="data_fbs")
            resting_ecg = st.selectbox("Resting ECG", [0, 1, 2], key="data_recg")
            max_heart_rate = st.number_input("Max Heart Rate", min_value=50, max_value=250, value=150, key="data_mhr")

        with c3:
            exercise_angina = st.selectbox("Exercise Angina", [0, 1], key="data_ea")
            oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, value=1.0, step=0.1, key="data_oldpeak")
            st_slope = st.selectbox("ST Slope", [1, 2, 3], key="data_sts")

        submitted = st.form_submit_button("Run Clinical Screening", use_container_width=True)

    if submitted:
        input_data = {
            "age": age,
            "sex": sex,
            "chest pain type": chest_pain_type,
            "resting bp s": resting_bp_s,
            "cholesterol": cholesterol,
            "fasting blood sugar": fasting_blood_sugar,
            "resting ecg": resting_ecg,
            "max heart rate": max_heart_rate,
            "exercise angina": exercise_angina,
            "oldpeak": oldpeak,
            "ST slope": st_slope
        }

        result = predict_tabular(input_data)
        st.session_state.tabular_result = result

    if st.session_state.tabular_result is not None:
        result = st.session_state.tabular_result
        d1, d2, d3 = st.columns(3)
        with d1:
            st.metric("Predicted Class", result["prediction"])
        with d2:
            st.metric("Risk Category", result["risk_label"])
        with d3:
            st.metric("Risk Probability", format_probability(result["probability"]))

        render_result_summary(result)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# INVESTOR BRIEF
# =========================
elif page == "Investor Brief":
    st.markdown('<div id="investor-brief"></div>', unsafe_allow_html=True)
    st.markdown('<div class="investor-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Investor Brief</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">CardioShield AI is positioned as an AI-assisted cardiovascular screening layer for faster triage, improved accessibility, and scalable early detection workflows.</div>', unsafe_allow_html=True)

    i1, i2, i3 = st.columns(3)
    with i1:
        st.metric("Primary Value", "Earlier screening")
    with i2:
        st.metric("Target Use Case", "Clinics + Telehealth")
    with i3:
        st.metric("Model Stack", "RF + CNN")

    st.markdown("### Why it matters")
    st.write(
        "Heart disease is often detected too late, especially in lower-resource settings. "
        "CardioShield AI demonstrates how structured clinical data and ECG imagery can be combined in a simple screening workflow."
    )

    st.markdown("### Core differentiation")
    st.write(
        "Unlike single-input screening demos, CardioShield AI presents a multimodal workflow: structured patient variables, ECG image intelligence, and a combined summary layer for decision support."
    )

    tabular_result = st.session_state.tabular_result
    ecg_result = st.session_state.ecg_result

    if tabular_result is not None or ecg_result is not None:
        st.markdown("### Live MVP Snapshot")
        combined = combine_predictions(
            tabular_result if tabular_result else {"probability": 0.0},
            ecg_result
        )
        j1, j2, j3 = st.columns(3)
        with j1:
            st.metric("Overall Risk", combined["overall_risk"])
        with j2:
            st.metric("Combined Score", format_probability(combined["combined_score"]))
        with j3:
            st.metric("Modalities Active", f"{int(tabular_result is not None) + int(ecg_result is not None)} / 2")

    st.markdown("### MVP positioning")
    st.write(
        "This is not positioned as a medical device at MVP stage. It is framed as a clinical decision-support and screening platform, which is more realistic for early pilots, product validation, and investor discussions."
    )

    st.markdown('<div class="disclaimer"><strong>Important:</strong> This product is an MVP for research, demonstration, and screening support. It is not a replacement for licensed medical diagnosis.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
