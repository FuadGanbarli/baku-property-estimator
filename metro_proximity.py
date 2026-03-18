import pandas as pd
from geopy.distance import geodesic
import math

df = pd.read_csv('data_with_address.csv', encoding= 'utf-8-sig' )
if "Metro Proximity" not in df.columns:
    df['Metro Proximity'] =  None
df["Metro Proximity"] = pd.Series(dtype="object")

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
    {"name": "Həzi Aslanov 2",   "lat": 40.3722, "lng": 49.9535},
    {"name": "8 Noyabr",         "lat": 40.4046, "lng": 49.8301},
    {"name": "Avtovağzal",       "lat": 40.4225, "lng": 49.7971},
    {"name": "Memar Əcəmi",      "lat": 40.4105, "lng": 49.8155},
    {"name": "Nizami",           "lat": 40.3794, "lng": 49.8305},
    {"name": "Elmlər Akademiyası","lat": 40.3751, "lng": 49.8156},
    {"name": "İnşaatçılar",      "lat": 40.3903, "lng":49.8026},
    {"name": "20 Yanvar",        "lat": 40.4043, "lng": 49.8099},
    {"name": "Memar Əcəmi 2",    "lat": 40.4106, "lng": 49.8137},
    {"name": "Xocasən",          "lat": 40.4212, "lng": 49.7791}
]

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

for idx, row in df.iterrows():
    isMetroNear = metro_proximity(row["Latitude"], row["Longtitude"], metros)
    df.at[idx, "Metro Proximity"] = isMetroNear
    print(f"{idx}/{len(df)}, {row['address']} -> {df.at[idx, 'Metro Proximity']}")

df.to_csv("data_with_address.csv", index= False, encoding="utf-8-sig")
print("Saved")