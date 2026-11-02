import os, joblib, pandas as pd, streamlit as st

st.set_page_config(page_title="Engine Predictive Maintenance System", layout="wide")
st.title("Engine Predictive Maintenance System")
st.markdown("This app uses ML trained on sensor telemetry to identify engine failures.")

@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "models", "best_model.pkl")
    if not os.path.exists(model_path):
        st.error(f"Model artifact not found at {model_path}.")
        return None
    return joblib.load(model_path)

model = load_model()
st.sidebar.header("Sensor Telemetry Input")
engine_rpm       = st.sidebar.slider("Engine Speed (RPM)", 50, 2500, 750, 10)
lub_oil_pressure = st.sidebar.slider("Lubricating Oil Pressure (bar)", 0.0, 8.0, 3.2, 0.05)
fuel_pressure    = st.sidebar.slider("Fuel Pressure (bar)", 0.0, 25.0, 6.5, 0.1)
coolant_pressure = st.sidebar.slider("Coolant Pressure (bar)", 0.0, 8.0, 2.4, 0.05)
lub_oil_temp     = st.sidebar.slider("Lubricating Oil Temperature (C)", 50.0, 120.0, 78.0, 0.5)
coolant_temp     = st.sidebar.slider("Coolant Temperature (C)", 50.0, 200.0, 80.0, 0.5)

input_df = pd.DataFrame([{"Engine rpm": engine_rpm, "Lub oil pressure": lub_oil_pressure,
    "Fuel pressure": fuel_pressure, "Coolant pressure": coolant_pressure,
    "lub oil temp": lub_oil_temp, "Coolant temp": coolant_temp}])

col1, col2 = st.columns(2)
with col1:
    st.subheader("Current Sensor Readings")
    st.dataframe(input_df.T.rename(columns={0: "Reading Value"}))
    st.markdown("**Normal RPM:** 600-1100 | **Healthy Oil:** 2.5-5.5 bar | **Safe Coolant:** 70-95 C")
with col2:
    st.subheader("Diagnostic Assessment")
    if model is not None:
        if st.button("Run Health Diagnostic", type="primary", use_container_width=True):
            pred = model.predict(input_df)[0]
            prob = model.predict_proba(input_df)[0] if hasattr(model, "predict_proba") else [0,0]
            st.divider()
            if pred == 1:
                st.error("ALERT: Engine Fault / Maintenance Required!")
                st.metric("Failure Risk Probability", f"{prob[1]*100:.1f}%")
                st.warning("1. Inspect lubrication circuit.\n2. Check coolant.\n3. Run diagnostic scan.")
            else:
                st.success("STATUS: Engine Operating Normally")
                st.metric("Normal Operating Confidence", f"{prob[0]*100:.1f}%")
                st.info("All sensor values within optimal bounds.")
    else:
        st.warning("Model not available.")

st.caption("Predictive Maintenance ML Pipeline | Built with Streamlit & Scikit-Learn")
