import streamlit as st
import numpy as np
import pickle

# Page configuration
st.set_page_config(
    page_title="Smart Grid Cyber Attack Detection",
    page_icon="🔐",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1 {
    color: #00FFFF;
    text-align: center;
}
.stButton>button {
    background-color: #00C9A7;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Load model
model = pickle.load(open("cyber_attack_model.pkl", "rb"))

# Sidebar
st.sidebar.title("⚡ Smart Grid Security")
st.sidebar.info(
"""
This system predicts cyber attacks in smart grid networks using Machine Learning.

Enter system feature values to detect anomalies.
"""
)

# Main title
st.title("🔐 Cyber Attack Detection System")

st.write("### Enter Grid Feature Value")

# Input
f1 = st.number_input("Feature f1", value=0.0, step=0.1)

# Predict button
if st.button("🚀 Predict Attack Risk"):

    features = np.array([[f1]])

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])

    st.write("---")
    st.subheader("📊 Prediction Result")

    if prediction == 1:
        st.error("⚠ Cyber Attack Detected")
    else:
        st.success("✅ Normal Grid Operation")

    st.subheader("📈 Attack Probability")

    st.progress(probability / 100)
    st.metric(label="Attack Risk", value=f"{probability:.2f}%")

    if probability > 70:
        st.warning("⚠ High Risk of Cyber Attack!")
    elif probability > 40:
        st.info("Moderate risk detected.")
    else:
        st.success("System operating normally.")

# Footer
st.write("---")
st.caption("Smart Grid Security Monitoring System | ML Project")