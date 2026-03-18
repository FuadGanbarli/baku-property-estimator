import requests
import time
import pandas as pd
import math
import os
from dotenv import load_dotenv
load_dotenv()
df = pd.read_csv("data_with_address.csv", encoding="utf-8")
if 'Latitude' not in df.columns:
    df['Latitude']  = None
if 'Longtitude' not in df.columns:
    df['Longtitude']  = None
BATCH_SIZE = 2000 
count =  0
missing = df[df["Latitude"].isna()]

def get_coordinates(location, address):
    url = 'https://nominatim.openstreetmap.org/search'
    headers = {"User-Agent" :os.getenv('YOUR_AGENT')}
    if not address or (isinstance(address, float)and math.isnan(address)):
        return None, None
    if not location or (isinstance(location, float)):
        return None, None
        
        
    params = {"q": location + address, "format": "json"}
    response = requests.get(url=url, params=params, headers=headers)
    data = response.json()
        
    if data:
        
        return float(data[0]["lat"]), float(data[0]["lon"])
        
    time.sleep(1)

    return None, None


last_idx = df[df["Latitude"].notna()].index.max()
for idx, row in df.iloc[last_idx:].iterrows():
     address = row['address']
     location = row['Location']
     lat, lng = get_coordinates( location, address)
     df.at[idx, 'Latitude' ]  = lat
     df.at[idx, "Longtitude"] = lng
     count +=1
     print(f"{count}/{BATCH_SIZE} — {df.at[idx, 'address']} -> {lat}, {lng}")
     time.sleep(1)
     if count> 0  and count % 100 == 0:
        df.to_csv("data_with_address.csv", index=False, encoding="utf-8-sig")
        print("Progress saved!")
     if count == BATCH_SIZE:
      print(f"Batch done! Run script again for next batch.")
      break
    

df.to_csv("data_with_address.csv", index=False, encoding="utf-8-sig")


    