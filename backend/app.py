from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from check import extract_features
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")


def train_and_load_model():
    from train_model import main as train_main

    print("Model file missing or invalid. Training fallback model...")
    train_main()

    with open(MODEL_PATH, "rb") as model_file:
        return pickle.load(model_file)


if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) == 0:
    model = train_and_load_model()
else:
    try:
        with open(MODEL_PATH, "rb") as model_file:
            model = pickle.load(model_file)
    except (EOFError, pickle.UnpicklingError):
        model = train_and_load_model()

@app.route("/")
def home():
    return "Backend Running 🚀"

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json(force=True, silent=True) or {}
    url = data.get("url", "")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "Invalid URL"}), 400

    url = url.strip()
    features = extract_features(url)
    features_np = np.array(features, dtype=float).reshape(1, -1)

    prediction = model.predict(features_np)[0]
    probability = 0.0

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features_np)[0]
        positive_index = list(model.classes_).index(1) if 1 in model.classes_ else -1
        probability = float(probabilities[positive_index]) if positive_index >= 0 else float(probabilities.max())
    else:
        probability = float(prediction)

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
            for word in ["login", "verify", "secure", "update"]
        )
    }

    reasons = []

    if features[2] == 0:
        reasons.append("No HTTPS encryption")

    if features[8] == 1:
        reasons.append("Uses IP address")

    if features[0] < 50:
        reasons.append("URL appears legitimate")

    if features[2] == 1:
        reasons.append("Uses HTTPS encryption")

    if features[0] < 75:
        reasons.append("Normal URL length")

    return jsonify({
        "isPhishing": bool(prediction),
        "confidence": round(probability * 100, 2),
        "riskScore": round(probability * 100),
        "features": feature_data,
        "reasons": reasons
    })

if __name__ == "__main__":
    app.run(debug=True)