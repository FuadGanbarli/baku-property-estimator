import streamlit as st
import joblib
import numpy as np
import folium
from streamlit_folium import st_folium
import joblib
from geopy.distance import geodesic
import math
import pandas as pd

model = joblib.load("REE_model.pkl")
columns = joblib.load("columns.pkl")
location_names = [col.replace("Location_", "") for col in columns if col.startswith("Location_")]

st.title("🏠 Baku Property Price Estimator")
input_data = {col: 0 for col in columns}

area = st.number_input("Area (m²)", min_value=10, max_value=1000)
rooms = st.number_input("Rooms", min_value=1, max_value=10)
is_apartment = st.checkbox("Is it an apartment?")
repaired = st.checkbox("Repaired?")
location = st.selectbox("Location", sorted(location_names))
if is_apartment:
    floor = st.number_input("Floor", min_value=1, max_value=50)
    floors = st.number_input("Total Floors", min_value=1, max_value=50)
else:
    floor = None
    floors = None
    st.info("Floor information not applicable for this property type")
st.write("📍 Click on the map to select property location")

m = folium.Map(location=[40.30, 49.985], zoom_start=12)

metros = [
    {"name": "İçərişəhər",       "lat": 40.3659, "lng": 49.8308},
    {"name": "Sahil",             "lat": 40.3716, "lng": 49.8439},
    {"name": "28 May",            "lat": 40.3798, "lng": 49.8483},
    {"name": "Xətai",              "lat": 40.3833, "lng": 49.8725},
    {"name": "Nəsimi",              "lat": 40.4251, "lng": 49.8269},
    {"name": "Azadlıq Prospekti",    "lat": 40.4262, "lng": 49.8420},
    {"name": "Dərnəgül",             "lat": 40.4253, "lng": 49.8612},
    {"name": "Gənclik",          "lat": 40.4004, "lng": 49.8514},
    {"name": "Nəriman Nərimanov","lat": 40.4027, "lng": 49.8718},
    {"name": "Bakmil",            "lat": 40.4142, "lng": 49.8779},
    {"name": "Ulduz",             "lat": 40.4148, "lng": 49.8915},
    {"name": "Koroğlu",          "lat": 40.4207, "lng": 49.918},
    {"name": "Qara Qarayev",     "lat": 40.4188, "lng": 49.9368},
    {"name": "Neftçilər",        "lat": 40.4108, "lng": 49.9435},
    {"name": "Xalqlar Dostluğu", "lat": 40.3988, "lng": 49.9533},
    {"name": "Əhmədli",          "lat": 40.3886, "lng": 49.9618},
    {"name": "Hazi Aslanov",     "lat": 40.3737, "lng": 49.9540},
    {"name": "8 Noyabr",         "lat": 40.4046, "lng": 49.8301},
    {"name": "Avtovağzal",       "lat": 40.4225, "lng": 49.7971},
    {"name": "Memar Əcəmi",      "lat": 40.4105, "lng": 49.8155},
    {"name": "Nizami",           "lat": 40.3794, "lng": 49.8305},
    {"name": "Elmlər Akademiyası","lat": 40.3751, "lng": 49.8156},
    {"name": "İnşaatçılar",      "lat": 40.3903, "lng":49.8026},
    {"name": "20 Yanvar",        "lat": 40.4043, "lng": 49.8099},
    {"name": "Xocasən",          "lat": 40.4212, "lng": 49.7791}
]

for metro in metros:
    folium.Marker(location=[metro["lat"], metro["lng"]],
                  popup=metro["name"],
                  tooltip=metro["name"],
                  icon=folium.Icon(color="green", icon="subway", prefix="fa")).add_to(m)
    
map_data = st_folium(m, height=450, width=700)

if map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]
    st.success(f"📍 Selected location: {lat:.6f}, {lng:.6f}")


    folium.Marker(
        location=[lat, lng],
        popup="Selected Property",
        icon=folium.Icon(color="red", icon="home", prefix="fa")
    ).add_to(m)

def metro_proximity(lat, lng, metros):
    if lat is None or  lng is None:
        return None, None
    if math.isnan(float(lat)) or math.isnan(float(lng)):
        return None, None
    isNear = False
    min_distance = float("inf")
    for metro in metros:
        distance = geodesic((lat, lng), (metro["lat"], metro["lng"]) ).km
        if distance < min_distance:
            min_distance = distance
            if min_distance <= 1.6:
                isNear = True
    return isNear

if st.button("Predict Price"):
    if lat is None or lng is None:
        st.error("Please click on the map to select a location!")
    else:
        PROXIMITY = metro_proximity(lat, lng, metros)
        input_data["Area"] = area
        input_data["Rooms"] = rooms
        input_data["Floor"] = floor if floor is not None else np.nan
        input_data["Floors"] = floors if floors is not None else np.nan
        input_data["Repaired"] = int(repaired)
        input_data["Latitude"] = lat
        input_data["Longtitude"] = lng
        input_data["Metro Proximity"] = int(PROXIMITY)
        input_data[f"Location_{location}"] = 1
        features = pd.DataFrame([input_data])
        log_price = model.predict(features)[0]
        price = np.expm1(log_price)
        st.success(f"💰 Estimated Price: {price:,.0f} AZN")