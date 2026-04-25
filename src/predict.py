import joblib
import pandas as pd

# Load saved model
model = joblib.load("house_price_model.pkl")

# Input for prediction
input_data = pd.DataFrame({"size_sqft": [1100]})

# Predict using saved model
prediction = model.predict(input_data)

print("🏠 Predicted price (from saved model):", prediction[0])