import streamlit as st
import joblib
import pandas as pd

# Background
def set_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1503376780353-7e6692767b70");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: -1;
        }
        h1, h2, h3, h4, h5, h6, p, div {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# Load model
model = joblib.load("accident_prediction_model.pkl")

st.title("🚧 Pothole Accident Risk Predictor")
st.write("Enter road conditions below:")

# ✅ UPDATED INPUTS (MORE CONTROL)
depth = st.slider("Pothole Depth (cm)", 1, 50, 10)
count = st.slider("Pothole Count in 10m", 0, 10, 2)
vehicle_speed = st.slider("Vehicle Speed (km/h)", 20, 120, 50)
visibility = st.slider("Visibility (meters)", 10, 500, 150)

traffic_density = st.selectbox("Traffic Density", ["Low", "Medium", "High"])
weather = st.selectbox("Weather Condition", ["Sunny", "Cloudy", "Rainy", "Foggy"])

if st.button("Predict Accident Risk"):

    speed_limit = 60
    lane_count = 2

    traffic_map = {"Low": 0, "Medium": 1, "High": 2}
    weather_map = {"Sunny": 0, "Cloudy": 1, "Rainy": 2, "Foggy": 3}

    # ✅ DYNAMIC FEATURES
    user_data = {
        "pothole_depth_cm": depth,
        "pothole_width_cm": 40,
        "pothole_area_cm2": depth * 40,
        "pothole_severity": 2,
        "pothole_count_in_10m": count,
        "road_type": 1,
        "road_condition": 2,
        "lane_count": lane_count,
        "speed_limit": speed_limit,
        "traffic_density": traffic_map[traffic_density],
        "vehicle_speed": vehicle_speed,
        "brake_applied": 0,
        "sudden_steering_change": 0,
        "vehicle_type": 1,
        "tyre_condition": 1,
        "weather": weather_map[weather],
        "visibility_m": visibility,
        "light_condition": 0,
        "latitude": 18.5,
        "longitude": 73.8,
        "maintain_speed_two_wheeler": 40,
        "maintain_speed_four_wheeler": 55,
        "pothole_area_speed_ratio": (depth * 40) / (vehicle_speed + 1),
        "combined_danger_score": (depth * 0.6 + count * 2 + vehicle_speed * 0.2),
        "speed_over_limit": int(vehicle_speed > speed_limit)
    }

    input_df = pd.DataFrame([user_data])

    # ✅ PREDICTION
    accident_prob = model.predict_proba(input_df)[0][1]
    accident_percentage = accident_prob * 100

    # ✅ IMPROVED THRESHOLDS
    if accident_percentage > 60:
        safe_speed = speed_limit * 0.5
        risk_level = "HIGH RISK 🚨"
    elif accident_percentage > 40:
        safe_speed = speed_limit * 0.7
        risk_level = "MODERATE RISK ⚠️"
    else:
        safe_speed = speed_limit * 0.9
        risk_level = "LOW RISK ✅"

    # ✅ OUTPUT UI
    st.subheader("🚦 Results")

    st.success(f"Accident Risk: {round(accident_percentage,2)} %")

    if "HIGH" in risk_level:
        st.error(risk_level)
    elif "MODERATE" in risk_level:
        st.warning(risk_level)
    else:
        st.info(risk_level)

    st.markdown(f"### 🚗 Recommended Safe Speed: {round(safe_speed,2)} km/h")
