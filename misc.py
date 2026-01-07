import requests

from datetime import date, datetime
from zoneinfo import ZoneInfo  # Python 3.9+

import os


# EST-aware timestamp for filenames
timestamp = datetime.now(ZoneInfo("America/New_York")).strftime("%Y%m%d_%H%M%S")
today = date.today().isoformat()  # 'YYYY-MM-DD'
# Ensure output directory exists
output_dir = f"data/{today}"
os.makedirs(output_dir, exist_ok=True)

def get_json_for_api(api_endpoint: str):
    response = requests.get(api_endpoint)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    else: 
        return response.json()
