import os
import joblib
import pandas as pd
import streamlit as st

# Configure Streamlit page layout matching IBM Carbon core structure
st.set_page_config(
    page_title="Engine Predictive Maintenance | IBM Carbon Design",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carbon Custom CSS Styling
st.markdown("""
<style>
    /* IBM Carbon-like Global Styles */
    html, body, [class*="css"] {
        font-family: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .carbon-header {
        background-color: #161616;
        color: #ffffff;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #393939;
    }
    .carbon-card {
        background-color: #f4f4f4;
        border: 1px solid #e0e0e0;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-radius: 0px; /* Carbon uses sharp edges */
    }
    .carbon-metric-title {
        font-size: 0.875rem;
        color: #525252;
        margin-bottom: 0.25rem;
    }
    .carbon-metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #161616;
    }
    .status-normal {
        border-left: 4px solid #24a148; /* Carbon green */
    }
    .status-alert {
        border-left: 4px solid #da1e28; /* Carbon red */
    }
</style>
""", unsafe_allow_html=True)

# Carbon Top Header Banner
st.markdown("""
<div class="carbon-header">
    <p style="font-size: 0.875rem; color: #a8a8a8; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Asset Performance Management</p>
    <h1 style="font-size: 2rem; font-weight: 300; margin: 0; color: #ffffff;">Engine Predictive Maintenance System</h1>
    <p style="font-size: 1rem; color: #e0e0e0; margin-top: 0.5rem; max-width: 800px;">
        Continuous condition-based monitoring and early anomaly classification utilizing edge telemetry sensors.
    </p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "models", "best_model.pkl")
    if not os.path.exists(model_path):
        st.error(f"Mandatory machine learning model artifact not found at: {model_path}")
        return None
    return joblib.load(model_path)

model = load_model()

# Sidebar - Control & Sensor Panel with clear Carbon Grouping
st.sidebar.markdown("### Telemetry Input Panel")
st.sidebar.markdown("Adjust the slider controls below to simulate real-time engine telemetry and diagnostics.")

engine_rpm = st.sidebar.slider("Engine Speed (RPM)", 50, 2500, 750, 10, help="Engine operational rotations per minute.")
lub_oil_pressure = st.sidebar.slider("Lubricating Oil Pressure (bar)", 0.0, 8.0, 3.2, 0.05, help="Pressure of lubricating fluid circuit.")
fuel_pressure = st.sidebar.slider("Fuel Delivery Pressure (bar)", 0.0, 25.0, 6.5, 0.1, help="Pressure level of the fuel injection pump.")
coolant_pressure = st.sidebar.slider("Cooling Loop Pressure (bar)", 0.0, 8.0, 2.4, 0.05, help="Static coolant circulation loop pressure.")
lub_oil_temp = st.sidebar.slider("Oil Sump Temperature (°C)", 50.0, 120.0, 78.0, 0.5, help="Thermal status of lubricating oil sump.")
coolant_temp = st.sidebar.slider("Engine Coolant Temperature (°C)", 50.0, 200.0, 80.0, 0.5, help="Operational liquid temperature of engine blocks.")

# Construct Input Schema matching training sets
input_df = pd.DataFrame([{
    "Engine rpm": engine_rpm,
    "Lub oil pressure": lub_oil_pressure,
    "Fuel pressure": fuel_pressure,
    "Coolant pressure": coolant_pressure,
    "lub oil temp": lub_oil_temp,
    "Coolant temp": coolant_temp
}])

# Main Carbon Work Grid
col1, col2 = st.columns([5, 7])

with col1:
    st.markdown("### Active Sensor Readings")
    
    # Display inputs transposed in a structured clean data table
    display_df = input_df.T.rename(columns={0: "Telemetry Value"})
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("""
    <div class="carbon-card">
        <h4 style="margin-top:0; font-size:1rem; font-weight:600; color:#161616;">Operational Threshold Rules</h4>
        <ul style="font-size:0.875rem; color:#525252; padding-left:1.2rem; line-height:1.5;">
            <li><b>Normal Speed Range:</b> 600 - 1100 RPM</li>
            <li><b>Critical Lubrication:</b> > 2.5 bar</li>
            <li><b>Optimal Cooling Temp:</b> 70 - 95 °C</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Diagnostic Assessment Dashboard")
    
    if model is not None:
        if st.button("Execute Asset Diagnostics", type="primary", use_container_width=True):
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0] if hasattr(model, "predict_proba") else [0.0, 0.0]
            
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            
            if prediction == 1:
                # Alert State Layout
                st.markdown(f"""
                <div class="carbon-card status-alert">
                    <h4 style="color:#da1e28; margin:0; font-weight:600;">🚨 HIGH FAILURE RISK DETECTED</h4>
                    <p style="font-size:0.875rem; color:#161616; margin-top:0.5rem;">
                        Asset status requires immediate condition-based preventative maintenance work order dispatch.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Custom IBM Metric Cards
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.markdown(f"""
                    <div class="carbon-card">
                        <div class="carbon-metric-title">ANOMALY CONFIDENCE</div>
                        <div class="carbon-metric-value" style="color:#da1e28;">{probabilities[1]*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f"""
                    <div class="carbon-card">
                        <div class="carbon-metric-title">HEALTH INDEX</div>
                        <div class="carbon-metric-value">{(1.0 - probabilities[1])*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.warning("**Recommended Action Items:**\n" 
                           "1. **Viscosity Verification**: Check lubrication pressure levels for micro-leakage.\n" 
                           "2. **Cooling Inspection**: Evaluate water pump duty cycle and coolant blockages.\n" 
                           "3. **Schedule Off-Shift PM**: Dispatch technicians to prevent structural thermodynamic warping.")
            else:
                # Healthy State Layout
                st.markdown(f"""
                <div class="carbon-card status-normal">
                    <h4 style="color:#198038; margin:0; font-weight:600;">✅ SYSTEM STABLE</h4>
                    <p style="font-size:0.875rem; color:#161616; margin-top:0.5rem;">
                        The engine asset is operating inside expected standard baseline telemetry ranges.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.markdown(f"""
                    <div class="carbon-card">
                        <div class="carbon-metric-title">STABILITY INDEX</div>
                        <div class="carbon-metric-value" style="color:#198038;">{probabilities[0]*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f"""
                    <div class="carbon-card">
                        <div class="carbon-metric-title">FAILURE PROBABILITY</div>
                        <div class="carbon-metric-value">{probabilities[1]*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.info("No preventative anomalies identified. Recommended action: Standard operational run scheduled.")
    else:
        st.warning("Model loading failure. Verify 'models/best_model.pkl' is correctly packaged and placed.")

st.markdown("<br><hr style='border: 0; border-top: 1px solid #e0e0e0;'/>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8d8d8d; font-size: 0.75rem;'>Asset Performance Management (APM) Framework | IBM Carbon Compliant Interface Layout</p>", unsafe_allow_html=True)
