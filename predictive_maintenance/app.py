"""
Streamlit Web Application for Real-Time Predictive Maintenance
Enables end users / fleet managers to input engine sensor parameters and predict health status.
"""

import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(
    page_title='Engine Predictive Maintenance System',
    page_icon='gear',
    layout='wide'
)

st.title('Engine Predictive Maintenance System')
st.markdown("""
This intelligent monitoring application utilizes machine learning trained on sensor telemetry
to assess engine operating conditions and identify potential failures before they occur.
""")

@st.cache_resource
def load_model():
    model_path = 'models/best_model.pkl'
    if not os.path.exists(model_path):
        st.error(f'Model artifact not found at {model_path}. Please train the model first.')
        return None
    return joblib.load(model_path)

model = load_model()

st.sidebar.header('Sensor Telemetry Input')

engine_rpm = st.sidebar.slider(
    'Engine Speed (RPM)',
    min_value=50,
    max_value=2500,
    value=750,
    step=10,
    help='Engine revolutions per minute.'
)

lub_oil_pressure = st.sidebar.slider(
    'Lubricating Oil Pressure (bar)',
    min_value=0.0,
    max_value=8.0,
    value=3.2,
    step=0.05,
    help='Pressure of lubrication oil.'
)

fuel_pressure = st.sidebar.slider(
    'Fuel Pressure (bar)',
    min_value=0.0,
    max_value=25.0,
    value=6.5,
    step=0.1,
    help='Pressure of fuel delivery.'
)

coolant_pressure = st.sidebar.slider(
    'Coolant Pressure (bar)',
    min_value=0.0,
    max_value=8.0,
    value=2.4,
    step=0.05,
    help='Pressure in cooling system.'
)

lub_oil_temp = st.sidebar.slider(
    'Lubricating Oil Temperature (°C)',
    min_value=50.0,
    max_value=120.0,
    value=78.0,
    step=0.5,
    help='Oil operating temperature.'
)

coolant_temp = st.sidebar.slider(
    'Coolant Temperature (°C)',
    min_value=50.0,
    max_value=200.0,
    value=80.0,
    step=0.5,
    help='Cooling system temperature.'
)

input_dict = {
    'Engine rpm': [engine_rpm],
    'Lub oil pressure': [lub_oil_pressure],
    'Fuel pressure': [fuel_pressure],
    'Coolant pressure': [coolant_pressure],
    'lub oil temp': [lub_oil_temp],
    'Coolant temp': [coolant_temp]
}
input_df = pd.DataFrame(input_dict)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader('Current Sensor Readings')
    st.dataframe(input_df.T.rename(columns={0: 'Reading Value'}))
    st.markdown('### Operational Benchmarks')
    st.markdown("""
    - **Normal RPM:** 600 - 1100 RPM
    - **Healthy Oil Pressure:** 2.5 - 5.5 bar
    - **Safe Coolant Temp:** 70 - 95 °C
    """)

with col2:
    st.subheader('Diagnostic Assessment')
    if model is not None:
        if st.button('Run Health Diagnostic', use_container_width=True, type='primary'):
            prediction = model.predict(input_df)[0]
            if hasattr(model, 'predict_proba'):
                prob = model.predict_proba(input_df)[0]
                fault_prob = prob[1]
                normal_prob = prob[0]
            else:
                fault_prob = 1.0 if prediction == 1 else 0.0
                normal_prob = 1.0 - fault_prob
            st.divider()
            if prediction == 1:
                st.error('ALERT: Engine Fault / Maintenance Required!')
                st.metric(label='Failure Risk Probability', value=f'{fault_prob * 100:.1f}%')
                st.warning("""
                **Recommended Maintenance Actions:**
                1. Inspect lubrication circuit for pressure drops or abnormal viscosity.
                2. Check coolant circulation to prevent thermal runaway.
                3. Perform immediate diagnostic scan before next operational shift.
                """)
            else:
                st.success('STATUS: Engine Operating Normally')
                st.metric(label='Normal Operating Confidence', value=f'{normal_prob * 100:.1f}%')
                st.info('All sensor telemetry values are within optimal operating bounds.')
    else:
        st.warning('Please ensure model artifact models/best_model.pkl is available.')

st.divider()
st.caption('Predictive Maintenance ML Pipeline | Built with Streamlit & Scikit-Learn')