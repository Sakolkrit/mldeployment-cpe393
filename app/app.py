from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the first model for /predict endpoint
MODEL_PATH = os.path.join("model.pkl")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Load the house price prediction model for /predict_house endpoint
HOUSE_MODEL_PATH = os.path.join("house_price_model.pkl")
with open(HOUSE_MODEL_PATH, "rb") as f:
    house_model = pickle.load(f)

# Function to preprocess the incoming house input
def preprocess_house_input(data):
    if "features" not in data:
        raise ValueError("Missing 'features' key in input")
        
    features = data["features"]
    if len(features) != 12:
        raise ValueError(f"Expected 12 features, got {len(features)}")
    
    processed_features = features.copy()
    
    # Convert categorical features
    categorical_mappings = {
        4: {"yes": 1, "no": 0},  # mainroad
        5: {"yes": 1, "no": 0},  # guestroom
        6: {"yes": 1, "no": 0},  # basement
        7: {"yes": 1, "no": 0},  # hotwaterheating
        8: {"yes": 1, "no": 0},  # airconditioning
        10: {"yes": 1, "no": 0},  # prefarea
        11: {"furnished": 1, "semi-furnished": 2, "unfurnished": 3}  # furnishingstatus
    }
    
    for idx, mapping in categorical_mappings.items():
        if features[idx] not in mapping:
            raise ValueError(f"Invalid value for feature index {idx}: {features[idx]}")
        processed_features[idx] = mapping[features[idx]]
    
    # Convert all to float
    processed_features = [float(x) for x in processed_features]
    
    feature_names = [
        "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom",
        "basement", "hotwaterheating", "airconditioning", "parking", "prefarea",
        "furnishingstatus"
    ]
    
    return pd.DataFrame([processed_features], columns=feature_names)

@app.route("/")
def home():
    return "House Price Prediction API with XGBoost is running"

@app.route("/health")
def health():
    return jsonify({"status": "OK!"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if "features" not in data or not isinstance(data["features"], list):
        return jsonify({"error": "Invalid Input: Features must be a list"}), 400
    
    features = data["features"]
    if not isinstance(features[0], list):
        features = [features]  
    
    expected_features = 4
    for feature in features:
        if len(feature) != expected_features:
            return jsonify({"error": "Invalid Input: Each feature must have 4 values"}), 400
    
    result = []

    for i, feature in enumerate(features):
        input_features = np.array(feature).reshape(1, -1)
        prediction = model.predict_proba(input_features)
    
        predicted_class = int(np.argmax(prediction[0]))
        probability = float(prediction[0][predicted_class])
        result.append({
            "prediction": predicted_class,
            "confidence": probability
        })
    
    return jsonify({"predictions": result})

@app.route("/predict_house", methods=["POST"])
def predict_house():
    try:
        data = request.get_json()
        processed_features = preprocess_house_input(data)
        prediction = house_model.predict(processed_features)
        return jsonify({
            "predicted_price": float(prediction[0])
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
