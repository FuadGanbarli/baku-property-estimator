from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
df = pd.read_csv("raw_data.csv", encoding="utf-8")
if 'address' not in df.columns:
    df['address'] = None
df['address'] = df['address'].astype('object')

headers = {
  'User-Agent': os.getenv('YOUR_AGENT'),
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Referer': 'https://bina.az/alqi-satqi',
  'content-type': 'application/json',
  'x-platform': 'desktop',
  'DNT': '1',
  'Sec-GPC': '1',
  'Connection': 'keep-alive',
  'Cookie': os.getenv('YOUR_COOKIE_HERE'),
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Priority': 'u=4',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'TE': 'trailers'
}

BATCH_SIZE = 2000
missing = df[df['address'].isna()]
count = 0

for idx, row in missing.iterrows():
    response = requests.get(url=row['Path'], headers= headers)
    soup = BeautifulSoup(response.text, "lxml" )
    adress_div= soup.find("div", class_= "product-map__left__address")
    if adress_div:
        adress_div = adress_div.text
        df.at[idx, 'address'] = adress_div.strip()
        count +=1
        print(f"{count}/{BATCH_SIZE} — {df.at[idx, 'address']}")
        time.sleep(1)
    else:
        df.at[idx, 'address'] = None
    if count> 0  and count % 100 == 0:
        df.to_csv("raw_data.csv", index=False, encoding="utf-8-sig")
        print("Progress saved!")
    if count >= BATCH_SIZE:
        print(f"Batch done! Run script again for next batch.")
        break
   



df.to_csv("data_with_address.csv", index=False, encoding="utf-8-sig")


