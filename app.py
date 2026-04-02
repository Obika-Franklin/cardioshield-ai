import streamlit as st
from utils.predictors import predict_tabular, predict_ecg, combine_predictions

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
# SESSION STATE
# =========================
if "tabular_result" not in st.session_state:
    st.session_state.tabular_result = None

if "ecg_result" not in st.session_state:
    st.session_state.ecg_result = None


# =========================
# STYLING
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f6f8fc;
}

/* Hero */
.hero-card {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    padding: 2.5rem;
    border-radius: 24px;
    color: white;
    margin-bottom: 1.5rem;
}

/* Cards */
.section-box, .info-card, .disclaimer-box {
    background: white;
    border-radius: 18px;
    padding: 1.2rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}

.disclaimer-box {
    border-left: 5px solid #f59e0b;
}

.info-card {
    border-left: 5px solid #2563eb;
}

/* Metrics */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 14px;
    padding: 1rem;
    border: 1px solid rgba(0,0,0,0.06);
}

/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    background: #2563eb;
    color: white;
    border-radius: 12px;
    font-weight: 600;
}

/* Inputs */
input, .stSelectbox div {
    border-radius: 12px !important;
}

/* Hide default */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
def render_header():
    st.markdown("""
    <div class="hero-card">
        <h1>CardioShield AI</h1>
        <p>Multimodal cardiovascular screening powered by machine learning and ECG intelligence.</p>
    </div>
    """, unsafe_allow_html=True)


render_header()


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## CardioShield AI")
    st.caption("Navigation")

    page = st.radio(
        "Go to",
        ["Home", "Clinical Risk Prediction", "ECG Analysis", "Combined Result", "About"]
    )


# =========================
# HOME
# =========================
if page == "Home":
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("## Early heart disease screening, redesigned")

        st.write(
            "CardioShield AI combines structured patient risk factors with ECG intelligence "
            "to enable earlier cardiovascular detection."
        )

        st.markdown("### Why this matters")
        st.write(
            "Heart disease is often detected late. This MVP demonstrates faster triage and scalable screening."
        )

        st.markdown("### MVP capabilities")
        st.write("- Clinical risk prediction")
        st.write("- ECG image analysis")
        st.write("- Combined screening insights")

    with col2:
        st.markdown("""
        <div class="section-box">
            <h3>Demo Highlights</h3>

            <div style="display:flex; flex-direction:column; gap:10px;">

                <div class="metric-card">
                    <p>Models</p>
                    <h2>2</h2>
                </div>

                <div class="metric-card">
                    <p>Modalities</p>
                    <h2>Tabular + ECG</h2>
                </div>

                <div class="metric-card">
                    <p>Deployment</p>
                    <h2>Streamlit Cloud</h2>
                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="disclaimer-box">', unsafe_allow_html=True)
        st.write("This system is for screening only.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### How to Use")
    st.write("1. Run Clinical Prediction")
    st.write("2. Upload ECG")
    st.write("3. View Combined Result")
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# CLINICAL PAGE
# =========================
elif page == "Clinical Risk Prediction":

    st.markdown("## Clinical Risk Prediction")

    with st.form("form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.number_input("Age (years)", 1, 120, 45)

            sex = st.selectbox(
                "Sex",
                [0,1],
                format_func=lambda x: "Female" if x == 0 else "Male"
            )

            chest_pain_type = st.selectbox(
                "Chest Pain Type",
                [1,2,3,4],
                format_func=lambda x: [
                    "Typical angina",
                    "Atypical angina",
                    "Non-anginal pain",
                    "Asymptomatic"
                ][x-1]
            )

            resting_bp_s = st.number_input("Resting Blood Pressure (mm Hg)", 50, 250, 120)

        with col2:
            cholesterol = st.number_input("Serum Cholesterol (mg/dL)", 50, 700, 200)

            fasting_blood_sugar = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dL",
                [0,1],
                format_func=lambda x: "No" if x == 0 else "Yes"
            )

            resting_ecg = st.selectbox(
                "Resting ECG",
                [0,1,2],
                format_func=lambda x: ["Normal","ST abnormality","LV hypertrophy"][x]
            )

            max_heart_rate = st.number_input("Maximum Heart Rate", 50, 250, 150)

        with col3:
            exercise_angina = st.selectbox(
                "Exercise Angina",
                [0,1],
                format_func=lambda x: "No" if x == 0 else "Yes"
            )

            oldpeak = st.number_input("ST Depression (Oldpeak)", 0.0, 10.0, 1.0)

            st_slope = st.selectbox(
                "ST Slope",
                [1,2,3],
                format_func=lambda x: ["Upsloping","Flat","Downsloping"][x-1]
            )

        submit = st.form_submit_button("Run Screening")

    if submit:
        data = {
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

        result = predict_tabular(data)

        st.metric("Risk", result["risk_label"])
        st.metric("Probability", f"{result['probability']:.2%}")


# =========================
# ECG PAGE
# =========================
elif page == "ECG Analysis":
    st.markdown("## ECG Analysis")

    file = st.file_uploader("Upload ECG", ["png","jpg","jpeg"])

    if file:
        st.image(file)

        if st.button("Analyze"):
            res = predict_ecg(file)
            st.metric("Class", res["class_name"])
            st.metric("Confidence", f"{res['confidence']:.2%}")


# =========================
# COMBINED
# =========================
elif page == "Combined Result":
    st.markdown("## Combined Result")

    combined = combine_predictions(
        st.session_state.tabular_result or {"probability":0},
        st.session_state.ecg_result
    )

    st.metric("Overall Risk", combined["overall_risk"])
    st.metric("Score", f"{combined['combined_score']:.2%}")


# =========================
# ABOUT
# =========================
elif page == "About":
    st.markdown("## About")

    st.write("CardioShield AI is a cardiovascular screening MVP.")
