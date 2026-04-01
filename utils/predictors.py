from pathlib import Path
from typing import Dict, Any, List

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.image import img_to_array
except Exception:
    load_model = None
    img_to_array = None

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"


@st.cache_resource(show_spinner=False)
def get_tabular_bundle():
    rf_path = MODELS_DIR / "rf_model.pkl"
    pre_path = MODELS_DIR / "preprocessor.pkl"
    if not (rf_path.exists() and pre_path.exists()):
        return None
    return {
        "model": joblib.load(rf_path),
        "preprocessor": joblib.load(pre_path),
    }


@st.cache_resource(show_spinner=False)
def get_ecg_model():
    model_path = MODELS_DIR / "vgg16_ecg_model.keras"
    if not model_path.exists() or load_model is None:
        return None
    return load_model(model_path)


def _risk_band(probability: float) -> str:
    if probability < 0.33:
        return "Low Risk"
    if probability < 0.66:
        return "Medium Risk"
    return "High Risk"


def _confidence_band(probability: float) -> str:
    distance = abs(probability - 0.5)
    if distance >= 0.35:
        return "High"
    if distance >= 0.15:
        return "Moderate"
    return "Low"


def predict_tabular(bundle: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    df = pd.DataFrame([payload])
    transformed = bundle["preprocessor"].transform(df)
    pred = int(bundle["model"].predict(transformed)[0])

    if hasattr(bundle["model"], "predict_proba"):
        prob = float(bundle["model"].predict_proba(transformed)[0][1])
    else:
        prob = float(pred)

    risk_label = _risk_band(prob)

    if risk_label == "Low Risk":
        message = "### Clinical interpretation\nThe structured clinical indicators suggest a lower immediate cardiovascular risk signal. In the MVP, this supports routine follow-up rather than urgent escalation."
    elif risk_label == "Medium Risk":
        message = "### Clinical interpretation\nThe patient profile shows a moderate risk signal. In a real workflow, this level is useful for prioritizing further review, repeat tests, or clinician follow-up."
    else:
        message = "### Clinical interpretation\nThe model is detecting a stronger adverse pattern across the patient variables. In the MVP story, this is the kind of case that justifies earlier referral and faster triage."

    return {
        "prediction": pred,
        "probability": prob,
        "risk_label": risk_label,
        "confidence_band": _confidence_band(prob),
        "clinical_message": message,
    }


def _prepare_image(uploaded_file, image_size=(100, 100)):
    image = Image.open(uploaded_file).convert("RGB")
    image = image.resize(image_size)
    arr = img_to_array(image).astype("float32") / 255.0
    return np.expand_dims(arr, axis=0)


def _ecg_risk_translation(class_name: str) -> str:
    name = class_name.lower()
    if "normal" in name:
        return "Low Risk"
    if "history of mi" in name or "abnormal heartbeat" in name:
        return "Medium Risk"
    if "myocardial infarction" in name:
        return "High Risk"
    return "Medium Risk"


def predict_ecg(model, uploaded_file, class_names: List[str]) -> Dict[str, Any]:
    arr = _prepare_image(uploaded_file)
    probs = model.predict(arr, verbose=0)[0]
    idx = int(np.argmax(probs))
    confidence = float(np.max(probs))
    class_name = class_names[idx]
    risk_label = _ecg_risk_translation(class_name)

    if risk_label == "Low Risk":
        message = "### ECG interpretation\nThe uploaded ECG image maps to the low-risk class currently configured in the app. This is the kind of output that supports reassuring but still clinically supervised screening."
    elif risk_label == "Medium Risk":
        message = "### ECG interpretation\nThe ECG model is detecting a non-normal pattern that deserves additional review. In the MVP, this supports triage and follow-up rather than final diagnosis."
    else:
        message = "### ECG interpretation\nThe ECG model is mapping the image to the highest-risk class configured in the current label set. This should be framed as a strong screening alert, not as a standalone diagnosis."

    return {
        "class_index": idx,
        "class_name": class_name,
        "confidence": confidence,
        "risk_label": risk_label,
        "display_label": f"{risk_label} · ECG",
        "clinical_message": message,
        "probabilities": {class_names[i]: float(probs[i]) for i in range(len(class_names))},
    }


def combine_results(tabular_result: Dict[str, Any], ecg_result: Dict[str, Any]) -> Dict[str, Any]:
    score = (0.6 * tabular_result["probability"]) + (0.4 * ecg_result["confidence"])
    overall = _risk_band(score)

    summary = f"""
### Multimodal summary
- The **clinical engine** returned **{tabular_result['risk_label']}**.
- The **ECG engine** returned **{ecg_result['risk_label']}** with **{ecg_result['confidence']:.1%}** confidence.
- The weighted MVP fusion score is **{score:.1%}**, which maps to **{overall}**.

For investor demos, present this as a **screening orchestration layer** that combines structured and visual health signals into a single workflow. For clinical honesty, state clearly that final diagnosis remains with a qualified medical professional.
"""

    return {
        "combined_score": score,
        "overall_risk": overall,
        "summary": summary,
    }
