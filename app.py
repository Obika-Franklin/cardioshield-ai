import streamlit as st
from utils.predictors import predict_tabular, predict_ecg, combine_predictions, load_cnn_model

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="CardioShield AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# PRELOAD MODEL (smooth UX)
# =========================
with st.spinner("Initializing AI systems..."):
    _ = load_cnn_model()

# =========================
# SESSION STATE
# =========================
if "tabular_result" not in st.session_state:
    st.session_state.tabular_result = None

if "ecg_result" not in st.session_state:
    st.session_state.ecg_result = None

# =========================
# LIGHT THEME CSS
# =========================
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Hero */
.hero-card {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    padding: 2rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 1.5rem;
}

/* Cards */
.section-box {
    background: #ffffff;
    padding: 1.2rem;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 1rem;
}

/* Metrics */
.metric-card {
    background: #ffffff;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

/* Warning */
.disclaimer-box {
    background: #fff7ed;
    border-left: 5px solid #f97316;
    padding: 1rem;
    border-radius: 10px;
    margin-top: 1rem;
}

/* Buttons */
.stButton > button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    border: none;
}

.stButton > button:hover {
    background: #1d4ed8;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f8fafc;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
def render_header():
    st.markdown("""
    <div class="hero-card">
        <h1>CardioShield AI</h1>
        <p>AI-powered cardiovascular screening for early detection.</p>
        <p>Combining clinical data and ECG intelligence.</p>
    </div>
    """, unsafe_allow_html=True)

def format_probability(p):
    return f"{p:.2%}"

def recommendation(risk):
    if risk == "Low Risk":
        return "Maintain healthy lifestyle and periodic checkups."
    elif risk == "Medium Risk":
        return "Further clinical evaluation is recommended."
    return "Urgent medical consultation is strongly advised."

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to", [
        "Home",
        "Clinical Risk",
        "ECG Analysis",
        "Combined Result",
        "About"
    ])

# =========================
# HEADER
# =========================
render_header()

# =========================
# HOME
# =========================
if page == "Home":
    st.markdown("## Overview")
    st.write("CardioShield AI enables early detection of heart disease risk using multimodal AI.")

    col1, col2 = st.columns(2)

    col1.metric("Models", "2")
    col1.metric("Modalities", "Tabular + ECG")

    col2.metric("Deployment", "Cloud-ready")
    col2.metric("Use Case", "Early Screening")

# =========================
# TABULAR
# =========================
elif page == "Clinical Risk":
    st.markdown("## Clinical Risk Prediction")

    with st.form("form"):
        age = st.number_input("Age", 1, 120, 45)
        sex = st.selectbox("Sex", [0,1])
        cholesterol = st.number_input("Cholesterol", 100, 600, 200)

        submitted = st.form_submit_button("Run Prediction")

    if submitted:
        result = predict_tabular({
            "age": age,
            "sex": sex,
            "cholesterol": cholesterol
        })

        st.session_state.tabular_result = result

        st.success("Prediction complete")
        st.metric("Risk", result["risk_label"])
        st.metric("Probability", format_probability(result["probability"]))

# =========================
# ECG
# =========================
elif page == "ECG Analysis":
    st.markdown("## ECG Analysis")

    file = st.file_uploader("Upload ECG", type=["png","jpg","jpeg"])

    if file:
        st.image(file)

        if st.button("Analyze ECG"):
            result = predict_ecg(file)
            st.session_state.ecg_result = result

            if not result["success"]:
                st.warning("ECG module unavailable")
                st.stop()

            st.success("Done")
            st.metric("Class", result["class_name"])
            st.metric("Confidence", format_probability(result["confidence"]))

# =========================
# COMBINED
# =========================
elif page == "Combined Result":
    st.markdown("## Combined Result")

    tab = st.session_state.tabular_result
    ecg = st.session_state.ecg_result

    if tab or ecg:
        combined = combine_predictions(tab or {"probability":0}, ecg)
        st.metric("Overall Risk", combined["overall_risk"])
        st.metric("Score", format_probability(combined["combined_score"]))
    else:
        st.warning("Run predictions first")

# =========================
# ABOUT
# =========================
elif page == "About":
    st.markdown("## About")
    st.write("CardioShield AI is a multimodal cardiovascular screening system.")
