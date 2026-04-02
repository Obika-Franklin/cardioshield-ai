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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f8fbff 0%, #f3f6fb 100%);
    color: #0f172a;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid rgba(15, 23, 42, 0.08);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.4rem;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #0f172a !important;
}

/* Hero */
.hero-card {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 58%, #0f172a 100%);
    padding: 2.3rem;
    border-radius: 26px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 45px rgba(37, 99, 235, 0.18);
    border: 1px solid rgba(255,255,255,0.16);
    position: relative;
    overflow: hidden;
}

.hero-card::before {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -80px;
    top: -80px;
    background: rgba(255,255,255,0.10);
    border-radius: 50%;
}

.hero-card::after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    right: 120px;
    bottom: -100px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}

/* General cards */
.metric-card,
.section-box,
.disclaimer-box,
.info-card {
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(15, 23, 42, 0.08);
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

.metric-card {
    padding: 1.1rem;
}

.section-box,
.info-card {
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.disclaimer-box {
    padding: 1rem 1.1rem;
    margin-top: 1rem;
    border-left: 5px solid #f59e0b;
}

.info-card {
    border-left: 5px solid #2563eb;
}

/* Streamlit metrics */
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid rgba(15, 23, 42, 0.08);
    padding: 1rem 1rem;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

div[data-testid="metric-container"] label {
    color: #475569 !important;
    font-weight: 600;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #0f172a;
    font-weight: 800;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.72rem 1.2rem;
    font-weight: 700;
    box-shadow: 0 10px 20px rgba(37, 99, 235, 0.18);
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 26px rgba(37, 99, 235, 0.22);
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput input,
.stSelectbox > div > div,
.stTextArea textarea {
    border-radius: 14px !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    background: #ffffff !important;
}

/* Form container */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(15, 23, 42, 0.07);
    border-radius: 22px;
    padding: 1.2rem 1.1rem 0.8rem 1.1rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}

/* Radio */
div[role="radiogroup"] > label {
    background: #ffffff;
    border: 1px solid rgba(15, 23, 42, 0.08);
    padding: 0.55rem 0.8rem;
    border-radius: 12px;
    margin-bottom: 0.35rem;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.92);
    border: 1px dashed rgba(37, 99, 235, 0.35);
    border-radius: 18px;
    padding: 0.75rem;
}

/* Alerts */
[data-testid="stSuccess"] {
    background: rgba(16, 185, 129, 0.10);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 14px;
}

[data-testid="stWarning"] {
    background: rgba(245, 158, 11, 0.10);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 14px;
}

[data-testid="stInfo"] {
    background: rgba(37, 99, 235, 0.08);
    border: 1px solid rgba(37, 99, 235, 0.18);
    border-radius: 14px;
}

/* Headings */
h1, h2, h3, h4 {
    letter-spacing: -0.02em;
    font-weight: 800;
    color: #0f172a;
}

.hero-card h1,
.hero-card h2,
.hero-card h3,
.hero-card h4,
.hero-card p,
.hero-card span {
    color: white !important;
    position: relative;
    z-index: 2;
}

/* Paragraphs */
p, li {
    color: #334155;
    line-height: 1.7;
}

/* Horizontal rule */
hr {
    border: none;
    height: 1px;
    background: rgba(15, 23, 42, 0.08);
    margin: 1.5rem 0;
}

/* Hide streamlit default menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =========================
# HELPERS
# =========================
def render_header():
    st.markdown("""
    <div class="hero-card">
        <p style="margin:0; font-size:0.92rem; font-weight:700; opacity:0.92; text-transform:uppercase; letter-spacing:0.08em;">
            AI-Powered Cardiovascular Screening
        </p>
        <h1 style="margin-top:0.55rem; margin-bottom:0.65rem;">CardioShield AI</h1>
        <p style="font-size:1.08rem; margin-bottom:0.45rem; max-width:760px;">
            Multimodal cardiovascular risk screening powered by machine learning and ECG image intelligence.
        </p>
        <p style="opacity:0.94; margin-bottom:0; max-width:760px;">
            Built as an early-screening decision-support MVP for scalable, affordable, and clinically guided heart risk assessment.
        </p>
    </div>
    """, unsafe_allow_html=True)


def risk_recommendation(risk_label: str) -> str:
    if risk_label == "Low Risk":
        return "Current screening result suggests lower immediate risk. Maintain healthy habits and continue routine monitoring."
    elif risk_label == "Medium Risk":
        return "This screening indicates moderate risk. A clinician review and additional cardiovascular evaluation are advisable."
    return "This screening indicates elevated cardiovascular risk. Prompt medical follow-up is strongly recommended."


def format_probability(prob: float) -> str:
    return f"{prob:.2%}"


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## CardioShield AI")
    st.caption("Navigation")

    page = st.radio(
        "Go to",
        [
            "Home",
            "Clinical Risk Prediction",
            "ECG Analysis",
            "Combined Result",
            "About"
        ]
    )

    st.markdown("---")
    st.caption("CardioShield AI MVP")
    st.caption("Investor Demo Build")


# =========================
# HEADER
# =========================
render_header()


# =========================
# HOME PAGE
# =========================
if page == "Home":
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("## Early heart disease screening, redesigned")
        st.write(
            "CardioShield AI combines structured patient risk factors with ECG image intelligence "
            "to support earlier cardiovascular risk detection in a scalable and affordable workflow."
        )

        st.markdown("### Why this matters")
        st.write(
            "Heart disease is often detected late, when treatment is more expensive and outcomes are worse. "
            "This MVP demonstrates a practical AI-assisted screening workflow that can support faster triage "
            "and more accessible preventive care."
        )

        st.markdown("### MVP capabilities")
        st.write("- Clinical risk prediction from structured patient inputs")
        st.write("- ECG image analysis using a deep learning model")
        st.write("- Combined screening summary for a multimodal workflow")
        st.write("- Decision-support framing for patient and clinician use")

    with col2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("### Demo Highlights")
        st.metric("Models", "2")
        st.metric("Modalities", "Tabular + ECG")
        st.metric("Deployment", "Streamlit Cloud")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="disclaimer-box">', unsafe_allow_html=True)
        st.markdown("**Clinical disclaimer**")
        st.write(
            "This system is intended for screening and decision support only. "
            "It does not replace professional medical diagnosis."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### Recommended demo flow")
    st.write("1. Run the Clinical Risk Prediction module")
    st.write("2. Run the ECG Analysis module")
    st.write("3. Open Combined Result to present the integrated summary")
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# CLINICAL RISK PAGE
# =========================
elif page == "Clinical Risk Prediction":
    st.markdown("## Clinical Risk Prediction")
    st.write("Enter patient risk factors to generate a structured cardiovascular screening result.")

    with st.form("clinical_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=45)

            sex = st.selectbox(
                "Sex",
                [0, 1],
                format_func=lambda x: {
                    0: "Female",
                    1: "Male"
                }[x]
            )

            chest_pain_type = st.selectbox(
                "Chest Pain Type",
                [1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Typical angina",
                    2: "Atypical angina",
                    3: "Non-anginal pain",
                    4: "Asymptomatic"
                }[x]
            )

            resting_bp_s = st.number_input(
                "Resting Blood Pressure (mm Hg)",
                min_value=50,
                max_value=250,
                value=120
            )

        with col2:
            cholesterol = st.number_input(
                "Serum Cholesterol (mg/dL)",
                min_value=50,
                max_value=700,
                value=200
            )

            fasting_blood_sugar = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dL",
                [0, 1],
                format_func=lambda x: {
                    0: "No",
                    1: "Yes"
                }[x]
            )

            resting_ecg = st.selectbox(
                "Resting Electrocardiogram Result",
                [0, 1, 2],
                format_func=lambda x: {
                    0: "Normal",
                    1: "ST-T wave abnormality",
                    2: "Left ventricular hypertrophy"
                }[x]
            )

            max_heart_rate = st.number_input(
                "Maximum Heart Rate Achieved",
                min_value=50,
                max_value=250,
                value=150
            )

        with col3:
            exercise_angina = st.selectbox(
                "Exercise-Induced Angina",
                [0, 1],
                format_func=lambda x: {
                    0: "No",
                    1: "Yes"
                }[x]
            )

            oldpeak = st.number_input(
                "ST Depression (Oldpeak)",
                min_value=0.0,
                max_value=10.0,
                value=1.0,
                step=0.1
            )

            st_slope = st.selectbox(
                "Slope of Peak Exercise ST Segment",
                [1, 2, 3],
                format_func=lambda x: {
                    1: "Upsloping",
                    2: "Flat",
                    3: "Downsloping"
                }[x]
            )

        submitted = st.form_submit_button("Run Clinical Screening")

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

        st.success("Clinical screening completed.")

        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Class", result["prediction"])
        m2.metric("Risk Category", result["risk_label"])
        m3.metric("Risk Probability", format_probability(result["probability"]))

        st.markdown("### Clinical Interpretation")
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.write(risk_recommendation(result["risk_label"]))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="disclaimer-box">', unsafe_allow_html=True)
        st.markdown("**Important**")
        st.write(
            "This output is intended for screening support only and should be reviewed in the context "
            "of clinical judgment, patient history, and further diagnostic testing."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.tabular_result is not None:
        result = st.session_state.tabular_result
        st.info("Showing most recent clinical screening result.")
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Class", result["prediction"])
        m2.metric("Risk Category", result["risk_label"])
        m3.metric("Risk Probability", format_probability(result["probability"]))


# =========================
# ECG PAGE
# =========================
elif page == "ECG Analysis":
    st.markdown("## ECG Image Analysis")
    st.write("Upload an ECG image for AI-assisted screening.")

    uploaded_file = st.file_uploader(
        "Upload ECG image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded ECG", use_container_width=True)

        if st.button("Analyze ECG"):
            result = predict_ecg(uploaded_file)
            st.session_state.ecg_result = result

            if not result["success"]:
                st.warning("ECG analysis is currently unavailable. Clinical risk screening remains active.")
                st.stop()

            st.success("ECG analysis completed successfully.")

            c1, c2 = st.columns(2)
            c1.metric("Predicted ECG Class", result["class_name"])
            c2.metric("Confidence", format_probability(result["confidence"]))

            st.markdown("### ECG Interpretation")
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.write(
                "The uploaded ECG image has been processed by the CNN screening model. "
                "This result should be interpreted as a decision-support signal rather than a final diagnosis."
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="disclaimer-box">', unsafe_allow_html=True)
            st.markdown("**Clinical disclaimer**")
            st.write(
                "ECG predictions are not a substitute for cardiologist review, formal ECG interpretation, "
                "or full patient assessment."
            )
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.ecg_result is not None and st.session_state.ecg_result.get("success"):
        result = st.session_state.ecg_result
        st.info("Showing most recent ECG result.")
        c1, c2 = st.columns(2)
        c1.metric("Predicted ECG Class", result["class_name"])
        c2.metric("Confidence", format_probability(result["confidence"]))


# =========================
# COMBINED RESULT PAGE
# =========================
elif page == "Combined Result":
    st.markdown("## Combined Screening Result")
    st.write("This page presents the integrated MVP summary across available prediction modules.")

    tabular_result = st.session_state.tabular_result
    ecg_result = st.session_state.ecg_result

    if tabular_result is None and ecg_result is None:
        st.warning("No screening results available yet. Run the Clinical Risk Prediction and/or ECG Analysis module first.")
        st.stop()

    combined = combine_predictions(tabular_result if tabular_result else {"probability": 0.0}, ecg_result)

    top1, top2, top3 = st.columns(3)
    top1.metric("Overall Risk", combined["overall_risk"])
    top2.metric("Combined Score", format_probability(combined["combined_score"]))
    top3.metric(
        "Available Modalities",
        f"{int(tabular_result is not None) + int(ecg_result is not None)} / 2"
    )

    st.markdown("### Module Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("#### Clinical Risk Module")
        if tabular_result is not None:
            st.write(f"**Risk Category:** {tabular_result['risk_label']}")
            st.write(f"**Probability:** {format_probability(tabular_result['probability'])}")
        else:
            st.write("No tabular screening result available.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("#### ECG Analysis Module")
        if ecg_result is not None and ecg_result.get("success"):
            st.write(f"**ECG Class:** {ecg_result['class_name']}")
            st.write(f"**Confidence:** {format_probability(ecg_result['confidence'])}")
        else:
            st.write("No ECG screening result available.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Combined Interpretation")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    if combined["overall_risk"] == "Low Risk":
        st.write(
            "The available screening signals currently indicate a relatively lower immediate cardiovascular risk profile. "
            "Routine monitoring and healthy lifestyle maintenance remain advisable."
        )
    elif combined["overall_risk"] == "Medium Risk":
        st.write(
            "The screening outputs suggest a moderate level of concern. "
            "Follow-up clinical review and further assessment are recommended."
        )
    else:
        st.write(
            "The combined screening signals suggest elevated cardiovascular risk. "
            "Timely clinical follow-up and a more comprehensive diagnostic workup are strongly recommended."
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="disclaimer-box">', unsafe_allow_html=True)
    st.markdown("**MVP note**")
    st.write(
        "This combined result is generated through an MVP integration layer for demonstration purposes. "
        "It should not be interpreted as a clinically validated multimodal diagnostic score."
    )
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# ABOUT PAGE
# =========================
elif page == "About":
    st.markdown("## About CardioShield AI")

    st.write(
        "CardioShield AI is a multimodal cardiovascular screening MVP designed to support earlier, "
        "more scalable detection of heart disease risk."
    )

    st.markdown("### Core architecture")
    st.write("- Random Forest model for structured clinical risk factors")
    st.write("- CNN model for ECG image analysis")
    st.write("- Lightweight integration layer for combined decision support")

    st.markdown("### Why this is compelling")
    st.write(
        "The platform is designed around practical screening workflows rather than heavyweight hospital infrastructure. "
        "That makes it suitable for future deployment in clinics, telehealth systems, and resource-constrained settings."
        )

    st.markdown("### Positioning")
    st.write(
        "CardioShield AI is positioned as a decision-support and screening system, not a replacement for clinicians. "
        "This lowers complexity for MVP deployment while keeping the long-term vision scalable."
    )

    st.markdown('<div class="disclaimer-box">', unsafe_allow_html=True)
    st.markdown("**Medical disclaimer**")
    st.write(
        "This application is for educational, research, and MVP demonstration purposes only. "
        "It is not a medical device and should not be used as a sole basis for diagnosis or treatment decisions."
    )
    st.markdown("</div>", unsafe_allow_html=True)
