import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load dataset (fixed encoding issue)
df = pd.read_csv("ieee118_clean_measurements.csv", encoding='latin1')

# Clean column names (important)
df.columns = df.columns.str.strip()

# Load model and scaler
model = joblib.load("cyber_attack_model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("Smart Grid Cyber Attack Detection")

st.write("Enter Smart Grid Measurements")

# Example: number of buses (change if needed)
num_buses = 5
bus_inputs = []

# Create input fields dynamically
for i in range(num_buses):
    val = st.number_input(f"Bus {i+1} Measurement", value=0.0)
    bus_inputs.append(val)

if st.button("Predict"):

    # Convert input to numpy array
    input_data = np.array([bus_inputs])

    # Scale input
    scaled_data = scaler.transform(input_data)

    # Predict
    prediction = model.predict(scaled_data)

    attacked_buses = []

    # If model returns multi-output like [0,1,0,1,...]
    try:
        for i, val in enumerate(prediction[0]):
            if val == 1:
                attacked_buses.append(f"Bus {i+1}")
    except:
        # If model returns single value (fallback)
        if prediction[0] == 1:
            attacked_buses.append("Unknown Bus (model not trained for bus-level detection)")

    # Display result
    if attacked_buses:
        st.error(f"⚠️ Attack detected on: {', '.join(attacked_buses)}")
    else:
        st.success("✅ Normal Grid Operation")