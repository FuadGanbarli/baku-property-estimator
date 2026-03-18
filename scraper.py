import requests
import time
import json
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
url = "https://bina.az/graphql?operationName=SearchItems&variables=%7B%22first%22%3A16%2C%22filter%22%3A%7B%22leased%22%3Afalse%7D%2C%22sort%22%3A%22BUMPED_AT_DESC%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22a2b7bef96bc42110dd00da3fdc558d26a60fdb9b91e3802dd124c3091ce43f0b%22%7D%7D"
payload = {}
headers = {
  'User-Agent':os.getenv('YOUR_AGENT'),
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Referer': 'https://bina.az/alqi-satqi',
  'content-type': 'application/json',
  'x-platform': 'desktop',
  'DNT': '1',
  'Sec-GPC': '1',
  'Connection': 'keep-alive',
  'Cookie': os.getenv('YOUR_COOKIE_HERE') ,
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Priority': 'u=4',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'TE': 'trailers'
}

all_items = []
cursor = None
while len(all_items) < 15000:
    variables = {
        "first": 16,
        "filter": {"leased": False},
        "sort": "BUMPED_AT_DESC"
    }
    
    
    if cursor:
        variables["cursor"] = cursor

    params = {
        "operationName": "SearchItems",
        "variables": json.dumps(variables),
        "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"a2b7bef96bc42110dd00da3fdc558d26a60fdb9b91e3802dd124c3091ce43f0b"}}'
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    
    edges = data["data"]["itemsConnection"]["edges"]
    for edge in edges:
     node = edge["node"]
     all_items.append({
        'ID': node["id"],
        'Path': "https://bina.az" + node['path'],
        'Area': node["area"]['value'], 
        'Location': node["location"]["fullName"] if node["location"] else None,
        'Rooms' : node["rooms"] if node["rooms"] else None,
        'Floor': node["floor"] if node["floor"] else None,
        'Floors': node["floors"] if node["floors"] else None,
        "Repaired": node["hasRepair"] if node["hasRepair"] else None,
        'Price': node["price"]["total"],
        'Currency':node["price"]["currency"]
    })

     print(f"Collected: {len(all_items)} items")

    
    page_info = data["data"]["itemsConnection"]["pageInfo"]
    if not page_info["hasNextPage"]:
        break  
    
    cursor = page_info["endCursor"]
    time.sleep(1) 

print(f"Done! Total: {len(all_items)} items")

df = pd.DataFrame(data= all_items)
df.to_csv("raw_data.csv", index= False)