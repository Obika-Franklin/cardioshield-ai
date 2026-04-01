import streamlit as st
from utils.ui import inject_custom_css, hero_section, feature_cards, result_badge, probability_bar, disclaimer_box, metric_strip
from utils.predictors import (
    get_tabular_bundle,
    get_ecg_model,
    predict_tabular,
    predict_ecg,
    combine_results,
)
from utils.config import TABULAR_NUMERIC_FIELDS, TABULAR_CATEGORICAL_OPTIONS, ECG_CLASS_NAMES, APP_NAME

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

if "tabular_result" not in st.session_state:
    st.session_state.tabular_result = None
if "ecg_result" not in st.session_state:
    st.session_state.ecg_result = None

with st.sidebar:
    st.markdown("## CardioShield AI")
    st.caption("Investor-grade MVP for cardiovascular risk screening")
    page = st.radio(
        "Navigate",
        ["Home", "Clinical Risk", "ECG Analysis", "Combined Insight", "Investor View", "About"],
    )
    st.markdown("---")
    st.markdown("### Deployment checklist")
    st.markdown(
        """
        - Upload `rf_model.pkl` to `models/`
        - Upload `preprocessor.pkl` to `models/`
        - Upload `vgg16_ecg_model.keras` to `models/`
        - Confirm ECG class order in `utils/config.py`
        """
    )

if page == "Home":
    hero_section()
    feature_cards()
    st.markdown("### What this MVP does")
    st.markdown(
        """
        CardioShield AI screens cardiovascular risk in two ways:

        1. **Clinical Risk Engine** – predicts risk from structured patient variables.
        2. **ECG Vision Engine** – classifies uploaded ECG images.
        3. **Combined Insight Layer** – merges both outputs into a single investor-friendly screening workflow.
        """
    )
    disclaimer_box()

elif page == "Clinical Risk":
    st.markdown("## Clinical Risk Prediction")
    st.caption("Structured patient-data inference using the trained Random Forest pipeline")

    left, right = st.columns([1.2, 1])

    with left:
        with st.form("clinical_form"):
            st.markdown("### Patient profile")
            age = st.number_input("Age", min_value=1, max_value=120, value=45)
            sex = st.selectbox("Sex", options=list(TABULAR_CATEGORICAL_OPTIONS["sex"].keys()), format_func=lambda x: TABULAR_CATEGORICAL_OPTIONS["sex"][x])

            st.markdown("### Clinical measurements")
            resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120)
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=50, max_value=700, value=200)
            max_hr = st.number_input("Max Heart Rate", min_value=50, max_value=250, value=150)
            oldpeak = st.number_input("Oldpeak (ST depression)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

            st.markdown("### Diagnostic indicators")
            chest_pain = st.selectbox("Chest Pain Type", options=list(TABULAR_CATEGORICAL_OPTIONS["chest pain type"].keys()), format_func=lambda x: TABULAR_CATEGORICAL_OPTIONS["chest pain type"][x])
            fasting_bs = st.selectbox("Fasting Blood Sugar", options=list(TABULAR_CATEGORICAL_OPTIONS["fasting blood sugar"].keys()), format_func=lambda x: TABULAR_CATEGORICAL_OPTIONS["fasting blood sugar"][x])
            resting_ecg = st.selectbox("Resting ECG", options=list(TABULAR_CATEGORICAL_OPTIONS["resting ecg"].keys()), format_func=lambda x: TABULAR_CATEGORICAL_OPTIONS["resting ecg"][x])
            exercise_angina = st.selectbox("Exercise Angina", options=list(TABULAR_CATEGORICAL_OPTIONS["exercise angina"].keys()), format_func=lambda x: TABULAR_CATEGORICAL_OPTIONS["exercise angina"][x])
            st_slope = st.selectbox("ST Slope", options=list(TABULAR_CATEGORICAL_OPTIONS["ST slope"].keys()), format_func=lambda x: TABULAR_CATEGORICAL_OPTIONS["ST slope"][x])

            submitted = st.form_submit_button("Run clinical screening", use_container_width=True)

        if submitted:
            bundle = get_tabular_bundle()
            if bundle is None:
                st.error("Tabular model files not found. Add `rf_model.pkl` and `preprocessor.pkl` to the `models/` folder.")
            else:
                input_payload = {
                    "age": age,
                    "resting bp s": resting_bp,
                    "cholesterol": cholesterol,
                    "max heart rate": max_hr,
                    "oldpeak": oldpeak,
                    "sex": sex,
                    "chest pain type": chest_pain,
                    "fasting blood sugar": fasting_bs,
                    "resting ecg": resting_ecg,
                    "exercise angina": exercise_angina,
                    "ST slope": st_slope,
                }
                st.session_state.tabular_result = predict_tabular(bundle, input_payload)

    with right:
        st.markdown("### Latest output")
        if st.session_state.tabular_result:
            result = st.session_state.tabular_result
            result_badge(result["risk_label"])
            metric_strip(
                [
                    ("Positive-class probability", f"{result['probability']:.1%}"),
                    ("Predicted class", str(result["prediction"])),
                    ("Confidence band", result["confidence_band"]),
                ]
            )
            probability_bar(result["probability"])
            st.markdown(result["clinical_message"])
        else:
            st.info("Run a clinical screening to see the output here.")
        disclaimer_box()

elif page == "ECG Analysis":
    st.markdown("## ECG Image Analysis")
    st.caption("Vision-model inference using the trained VGG16 ECG classifier")
    upload = st.file_uploader("Upload an ECG image", type=["png", "jpg", "jpeg", "webp"])

    col1, col2 = st.columns([1, 1])
    with col1:
        if upload is not None:
            st.image(upload, caption="Uploaded ECG image", use_container_width=True)

    with col2:
        if st.button("Analyze ECG", use_container_width=True, disabled=upload is None):
            model = get_ecg_model()
            if model is None:
                st.error("ECG model file not found. Add `vgg16_ecg_model.keras` to the `models/` folder.")
            else:
                st.session_state.ecg_result = predict_ecg(model, upload, ECG_CLASS_NAMES)

        if st.session_state.ecg_result:
            result = st.session_state.ecg_result
            result_badge(result["display_label"])
            metric_strip(
                [
                    ("Predicted ECG class", result["class_name"]),
                    ("Model confidence", f"{result['confidence']:.1%}"),
                    ("Risk translation", result["risk_label"]),
                ]
            )
            probability_bar(result["confidence"])
            st.markdown(result["clinical_message"])
        else:
            st.info("Upload an ECG image and click Analyze ECG.")
        disclaimer_box()

elif page == "Combined Insight":
    st.markdown("## Combined Insight")
    st.caption("Simple multimodal fusion for the MVP demo")

    if st.session_state.tabular_result and st.session_state.ecg_result:
        fusion = combine_results(st.session_state.tabular_result, st.session_state.ecg_result)
        result_badge(fusion["overall_risk"])
        metric_strip(
            [
                ("Combined score", f"{fusion['combined_score']:.1%}"),
                ("Clinical engine", st.session_state.tabular_result["risk_label"]),
                ("ECG engine", st.session_state.ecg_result["risk_label"]),
            ]
        )
        probability_bar(fusion["combined_score"])
        st.markdown(fusion["summary"])
        st.success("This fused output is suitable for MVP storytelling, screening triage, and investor demos. It should not be framed as a final diagnosis.")
    else:
        st.warning("Run both the Clinical Risk and ECG Analysis modules first to unlock the combined view.")
    disclaimer_box()

elif page == "Investor View":
    st.markdown("## Investor View")
    st.caption("Narrative framing for Google, Microsoft, incubators, and healthcare innovation panels")

    metric_strip(
        [
            ("Positioning", "AI screening infrastructure"),
            ("Primary wedge", "Low-cost early cardiovascular triage"),
            ("MVP mode", "Decision-support"),
        ]
    )

    st.markdown(
        """
        ### Investor narrative
        **CardioShield AI** shifts heart screening from late-stage, specialist-heavy workflows to an earlier, software-driven decision-support layer.

        **Why it matters:**
        - Cardiovascular care becomes more expensive and less effective when detection happens late.
        - Many settings still lack scalable screening capacity.
        - A multimodal approach is stronger than a single-input workflow because it blends structured risk factors with ECG image intelligence.

        **What makes the MVP presentation-ready:**
        - Clear patient and clinician workflows
        - Premium interface rather than a classroom demo look
        - Explainable risk bands and confidence outputs
        - Modular architecture that can later evolve into APIs, hospital dashboards, and cloud-native inference services
        """
    )

    st.markdown("### Suggested CTA buttons for demo day")
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("Investor Brief", "https://example.com")
    with c2:
        st.link_button("Join Waitlist", "https://example.com")

    st.info("Replace the placeholder links above with your actual deck, Notion page, Google Form, or landing page.")

elif page == "About":
    st.markdown("## About CardioShield AI")
    st.markdown(
        """
        CardioShield AI is a dual-model cardiovascular screening MVP.

        - **Model 1:** Random Forest for structured patient variables
        - **Model 2:** CNN/VGG16 for ECG image analysis
        - **Fusion:** lightweight combined scoring for MVP-level multimodal output

        This app is intentionally packaged as a lean deployment starter pack for Streamlit Cloud.
        """
    )
    st.markdown("### Files you must place in `/models`")
    st.code(
        """
models/
├── rf_model.pkl
├── preprocessor.pkl
└── vgg16_ecg_model.keras
        """.strip()
    )
    st.markdown("### Verify before demo")
    st.markdown(
        f"""
        - Tabular numeric fields: {', '.join(TABULAR_NUMERIC_FIELDS)}
        - ECG class count in app: {len(ECG_CLASS_NAMES)}
        - ECG classes currently set in config: {', '.join(ECG_CLASS_NAMES)}
        """
    )
    disclaimer_box()
