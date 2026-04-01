APP_NAME = "CardioShield AI"

TABULAR_NUMERIC_FIELDS = [
    "age",
    "resting bp s",
    "cholesterol",
    "max heart rate",
    "oldpeak",
]

TABULAR_CATEGORICAL_OPTIONS = {
    "sex": {
        0: "Female",
        1: "Male",
    },
    "chest pain type": {
        1: "Typical Angina",
        2: "Atypical Angina",
        3: "Non-Anginal Pain",
        4: "Asymptomatic",
    },
    "fasting blood sugar": {
        0: "< 120 mg/dL",
        1: "> 120 mg/dL",
    },
    "resting ecg": {
        0: "Normal",
        1: "ST-T Wave Abnormality",
        2: "Left Ventricular Hypertrophy",
    },
    "exercise angina": {
        0: "No",
        1: "Yes",
    },
    "ST slope": {
        1: "Upsloping",
        2: "Flat",
        3: "Downsloping",
    },
}

# Verify this order against your training generator:
# print(valid_gen.class_indices)
ECG_CLASS_NAMES = [
    "ECG Images of Myocardial Infarction Patients (240x12=2880)",
    "ECG Images of Patient that have History of MI (172x12=2064)",
    "ECG Images of Patient that have abnormal heartbeat (233x12=2796)",
    "Normal Person ECG Images (284x12=3408)",
]
