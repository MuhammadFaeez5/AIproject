import streamlit as st
import numpy as np
import joblib
from strategy_rules import rule_based_signal_timing
import pandas as pd

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(layout="centered")
st.title("🚦 Real-Time Traffic Congestion Predictor")

st.markdown("Enter traffic and weather conditions to get congestion prediction and signal control suggestion.")

# Inputs
temp = st.number_input("Temperature (K)", min_value=250.0, max_value=330.0, value=295.0)
rain = st.number_input("Rain in 1 hour (mm)", min_value=0.0, max_value=100.0, value=0.0)
snow = st.number_input("Snow in 1 hour (mm)", min_value=0.0, max_value=100.0, value=0.0)
clouds = st.slider("Cloud coverage (%)", min_value=0, max_value=100, value=50)
hour = st.slider("Hour of the day", min_value=0, max_value=23, value=8)
weekday = st.selectbox("Day of the week", options=[
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
])
vehicles = st.number_input("Vehicle Count", min_value=0, max_value=200, value=50)

# Convert weekday to number and weekend flag
weekday_number = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(weekday)
is_weekend = weekday_number >= 5

# Prepare input for model
input_data = pd.DataFrame([{
    'temp': temp,
    'rain_1h': rain,
    'snow_1h': snow,
    'clouds_all': clouds,
    'hour': hour,
    'weekday': weekday_number,
    'Vehicles': vehicles,
    'is_weekend': is_weekend,
    'traffic_volume': vehicles * 80  # approximate traffic volume
}])

# Scale the features used in training
features = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'hour', 'weekday', 'Vehicles']
scaled_input = scaler.transform(input_data[features])

# Make prediction
congestion = model.predict(scaled_input)[0]
congestion_text = "Yes" if congestion == 1 else "No"

# Signal strategy
signal_strategy = rule_based_signal_timing(input_data.iloc[0])

# Output
st.subheader("🔍 Prediction Result")
st.markdown(f"**Recommended Signal Strategy:** {signal_strategy}")

