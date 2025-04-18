# save_model.py
import pickle
import pandas as pd
from xgboost import XGBRegressor

# Load data
house = pd.read_csv("Housing.csv")

# Convert categorical features to numerical
house["mainroad"] = house["mainroad"].map({"yes": 1, "no": 0})
house["guestroom"] = house["guestroom"].map({"yes": 1, "no": 0})
house["basement"] = house["basement"].map({"yes": 1, "no": 0})
house["hotwaterheating"] = house["hotwaterheating"].map({"yes": 1, "no": 0})
house["airconditioning"] = house["airconditioning"].map({"yes": 1, "no": 0})
house["prefarea"] = house["prefarea"].map({"yes": 1, "no": 0})
house["furnishingstatus"] = house["furnishingstatus"].map({"furnished": 1, "semi-furnished": 2, "unfurnished": 3})

# Define features and target
X = house[[
    "area", "bedrooms", "bathrooms", "stories",
    "mainroad", "guestroom", "basement", "hotwaterheating",
    "airconditioning", "parking", "prefarea", "furnishingstatus"
]]
y = house["price"]

# Train the model using XGBoost
model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    objective='reg:squarederror',
    random_state=42
)
model.fit(X, y)

# Save the model
with open("app/house_price_model.pkl", "wb") as f:
    pickle.dump(model, f)
