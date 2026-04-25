import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression



# 🏠 dataset
data = {
    "size_sqft": [650, 800, 850, 900, 1000, 1200, 1500, 1800],
    "price": [150000, 180000, 190000, 200000, 230000, 280000, 340000, 400000]
}

df = pd.DataFrame(data)

# features and target
X = df[["size_sqft"]]
y = df["price"]

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# model
model = LinearRegression()
model.fit(X_train, y_train)

# prediction (IMPORTANT FIX — no warnings)
input_data = pd.DataFrame({"size_sqft": [1100]})
prediction = model.predict(input_data)

print("🏠 Predicted price for 1100 sqft:", prediction[0])

joblib.dump(model, "house_price_model.pkl")
print("✅ Model saved successfully!")