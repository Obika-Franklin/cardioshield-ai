import os
import io
import joblib
import requests
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# =========================
# PATHS
# =========================
RF_MODEL_PATH = "models/rf_model.pkl"
PREPROCESSOR_PATH = "models/preprocessor.pkl"

CNN_MODEL_PATH = "models/vgg16_ecg_model.keras"
CNN_MODEL_URL = "https://github.com/Obika-Franklin/cardioshield-ai/releases/download/v1.0.0/vgg16_ecg_model.keras"

# =========================
# CONFIG
# =========================
# Replace these labels with the EXACT class order used in training
ECG_CLASS_NAMES = [
    "Normal",
    "Abnormal Heartbeat",
    "Myocardial Infarction",
    "History of Myocardial Infarction"
]

IMG_SIZE = (100, 100)


# =========================
# DOWNLOAD HELPER
# =========================
def download_file(url: str, save_path: str):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    response = requests.get(url, stream=True, timeout=300)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0

    progress_bar = st.progress(0, text="Preparing ECG AI model...")
    status_text = st.empty()

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)

                if total_size > 0:
                    progress = min(downloaded / total_size, 1.0)
                    progress_bar.progress(progress, text="Preparing ECG AI model...")
                    status_text.caption(
                        f"Downloaded {downloaded / (1024 * 1024):.1f} MB of {total_size / (1024 * 1024):.1f} MB"
                    )

    progress_bar.empty()
    status_text.empty()


# =========================
# MODEL LOADERS
# =========================
@st.cache_resource
def load_rf_model():
    return joblib.load(RF_MODEL_PATH)


@st.cache_resource
def load_preprocessor():
    return joblib.load(PREPROCESSOR_PATH)


@st.cache_resource
def load_cnn_model():
    try:
        if not os.path.exists(CNN_MODEL_PATH):
            download_file(CNN_MODEL_URL, CNN_MODEL_PATH)

        model = load_model(CNN_MODEL_PATH)
        return model

    except Exception as e:
        st.error(f"ECG module unavailable in this demo environment. Error: {e}")
        return None


# =========================
# TABULAR PREDICTION
# =========================
def map_risk(probability: float) -> str:
    if probability < 0.33:
        return "Low Risk"
    elif probability < 0.66:
        return "Medium Risk"
    return "High Risk"


def predict_tabular(input_data: dict) -> dict:
    rf_model = load_rf_model()
    preprocessor = load_preprocessor()

    df = pd.DataFrame([input_data])
    X_processed = preprocessor.transform(df)

    prediction = int(rf_model.predict(X_processed)[0])

    if hasattr(rf_model, "predict_proba"):
        probability = float(rf_model.predict_proba(X_processed)[0][1])
    else:
        probability = float(prediction)

    risk_label = map_risk(probability)

    return {
        "prediction": prediction,
        "probability": probability,
        "risk_label": risk_label
    }


# =========================
# ECG IMAGE PREPROCESSING
# =========================
def preprocess_ecg_image(uploaded_file):
    if uploaded_file is None:
        raise ValueError("No image file uploaded.")

    file_bytes = uploaded_file.read()
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)

    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = arr / 255.0

    return arr, img


# =========================
# ECG PREDICTION
# =========================
def predict_ecg(uploaded_file) -> dict:
    cnn_model = load_cnn_model()

    if cnn_model is None:
        return {
            "success": False,
            "message": "ECG model could not be loaded."
        }

    arr, display_img = preprocess_ecg_image(uploaded_file)

    probs = cnn_model.predict(arr, verbose=0)[0]
    class_idx = int(np.argmax(probs))
    confidence = float(np.max(probs))
    predicted_label = ECG_CLASS_NAMES[class_idx]

    return {
        "success": True,
        "class_idx": class_idx,
        "class_name": predicted_label,
        "confidence": confidence,
        "all_probabilities": probs.tolist(),
        "display_image": display_img
    }


# =========================
# SIMPLE MVP FUSION
# =========================
def combine_predictions(tabular_result: dict, ecg_result: dict) -> dict:
    tab_prob = float(tabular_result.get("probability", 0.0))

    if not ecg_result or not ecg_result.get("success"):
        combined_score = tab_prob
    else:
        ecg_conf = float(ecg_result.get("confidence", 0.0))
        combined_score = (0.6 * tab_prob) + (0.4 * ecg_conf)

    if combined_score < 0.33:
        overall_risk = "Low Risk"
    elif combined_score < 0.66:
        overall_risk = "Medium Risk"
    else:
        overall_risk = "High Risk"

    return {
        "combined_score": combined_score,
        "overall_risk": overall_risk
    }
