from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from check import extract_features
import os

app = Flask(__name__)
CORS(app)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# -----------------------------
# Train fallback model if missing
# -----------------------------
def train_and_load_model():
    from train_model import main as train_main

    print("⚠️ model.pkl missing or corrupted. Training new model...")
    train_main()

    with open(MODEL_PATH, "rb") as model_file:
        return pickle.load(model_file)

# -----------------------------
# Load model safely
# -----------------------------
if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) == 0:
    model = train_and_load_model()
else:
    try:
        with open(MODEL_PATH, "rb") as model_file:
            model = pickle.load(model_file)

        print("✅ Model loaded successfully")

    except (EOFError, pickle.UnpicklingError):
        model = train_and_load_model()

# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return "🚀 Phishing URL Detection Backend Running"

# -----------------------------
# Predict Route
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json(force=True, silent=True) or {}

        url = data.get("url", "")

        # -----------------------------
        # Validate URL
        # -----------------------------
        if not isinstance(url, str) or not url.strip():
            return jsonify({
                "error": "Invalid URL"
            }), 400

        url = url.strip()

        # -----------------------------
        # Extract Features
        # -----------------------------
        features = extract_features(url)

        features_np = np.array(
            features,
            dtype=float
        ).reshape(1, -1)

        # -----------------------------
        # Prediction
        # -----------------------------
        prediction = model.predict(features_np)[0]

        probability = 0.0

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(features_np)[0]

            positive_index = (
                list(model.classes_).index(1)
                if 1 in model.classes_
                else -1
            )

            probability = (
                float(probabilities[positive_index])
                if positive_index >= 0
                else float(probabilities.max())
            )

        else:
            probability = float(prediction)

        # -----------------------------
        # Feature Data for Frontend
        # -----------------------------
        feature_data = {
            "URL Length": features[0],
            "Number of Dots": features[1],
            "HTTPS": "Yes" if features[2] else "No",
            "Contains @": "Yes" if features[3] else "No",
            "Contains -": "Yes" if features[4] else "No",
            "Domain Length": features[5],
            "Number of Digits": features[6],
            "Special Characters": features[7],
            "IP Address": "Yes" if features[8] else "No",
            "Subdomains": max(features[1] - 1, 0),
            "Suspicious Keywords": sum(
                word in url.lower()
                for word in [
                    "login",
                    "verify",
                    "secure",
                    "update",
                    "bank",
                    "paypal",
                    "account"
                ]
            )
        }

        # -----------------------------
        # Reasons / Analysis
        # -----------------------------
        reasons = []

        if features[2] == 0:
            reasons.append("No HTTPS encryption")

        if features[8] == 1:
            reasons.append("Uses IP address instead of domain")

        if features[3] == 1:
            reasons.append("Contains @ symbol")

        if features[4] == 1:
            reasons.append("Contains hyphen (-)")

        if features[0] > 75:
            reasons.append("URL is unusually long")

        if feature_data["Suspicious Keywords"] > 0:
            reasons.append("Contains suspicious keywords")

        # Safe indicators
        if features[2] == 1:
            reasons.append("Uses HTTPS encryption")

        if features[0] < 75:
            reasons.append("Normal URL length")

        if features[8] == 0:
            reasons.append("Uses proper domain")

        # -----------------------------
        # Final Response
        # -----------------------------
        return jsonify({
            "isPhishing": bool(prediction),
            "confidence": round(probability * 100, 2),
            "riskScore": round(probability * 100),
            "features": feature_data,
            "reasons": reasons
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )