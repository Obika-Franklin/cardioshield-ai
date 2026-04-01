# CardioShield AI — Production-Ready Streamlit Starter Pack

This starter pack turns your trained CardioShield models into a clean MVP that is suitable for:
- Streamlit Cloud deployment
- investor demos
- capstone/project showcases
- pilot conversations with hospitals or clinicians

## What is included

- `app.py` — main Streamlit app
- `utils/config.py` — app configuration, class labels, categorical mappings
- `utils/predictors.py` — model loading and inference logic
- `utils/ui.py` — polished UI components and custom CSS
- `.streamlit/config.toml` — premium dark theme
- `requirements.txt` — Python packages
- `packages.txt` — system package for image rendering support

## Models you must add

Place these files inside the `models/` folder:

```bash
models/
├── rf_model.pkl
├── preprocessor.pkl
└── vgg16_ecg_model.keras
```

## Important verification step

Before demo or deployment, verify the ECG class order in `utils/config.py`.

Your notebook should print something like:

```python
print(valid_gen.class_indices)
```

Whatever order appears there must match `ECG_CLASS_NAMES` in the app.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud deployment

1. Create a GitHub repo and upload this project.
2. Add your model files inside `models/`.
3. Go to Streamlit Cloud.
4. Click **New app**.
5. Connect your repo.
6. Set `app.py` as the entry point.
7. Deploy.

## How to present it to investors

Frame it this way:

> CardioShield AI is a multimodal cardiovascular screening platform that combines structured clinical variables and ECG image analysis into a low-cost decision-support workflow.

Use these talking points:
- early detection instead of late-stage intervention
- lean deployment model
- scalable in resource-limited settings
- modular enough for hospital dashboards, APIs, and future EHR integrations

## Notes

- This is a **screening MVP**, not a diagnostic device.
- The fusion layer is intentionally lightweight for demo readiness.
- You can later replace the simple fusion logic with a properly validated multimodal model.
