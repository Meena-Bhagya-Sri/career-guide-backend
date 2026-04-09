import joblib
import os

BASE_DIR = os.path.dirname(__file__)

rf_model = joblib.load(
    os.path.join(BASE_DIR, "models", "career_rf_model.pkl")
)

label_encoder = joblib.load(
    os.path.join(BASE_DIR, "models", "label_encoder.pkl")
)

def predict_career(X):
    prediction = rf_model.predict(X)[0]
    return label_encoder.inverse_transform([prediction])[0]
