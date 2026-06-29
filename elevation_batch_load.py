import requests
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Retrieve the key from the environment
API_KEY = os.getenv("open_topography_api_key")

OUTPUT_DIR = "south_america_dem"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# South America bounding box (approximate)
lat_range = range(-55, 15, 5) # South to North
lon_range = range(-80, -35, 5) # West to East

def download_tile(min_lon, min_lat, max_lon, max_lat):
    filename = f"dem_{min_lon}_{min_lat}.tif"
    if os.path.exists(os.path.join(OUTPUT_DIR, filename)):
        return

    url = "https://portal.opentopography.org/API/globaldem"
    params = {
        "demtype": "SRTMGL1",
        "south": min_lat,
        "north": max_lat,
        "west": min_lon,
        "east": max_lon,
        "outputFormat": "GTiff",
        "API_Key": API_KEY  # Pass the key here
    }
    
    print(f"Downloading: {filename}...")
    response = requests.get(url, params=params, stream=True)
    if response.status_code == 200:
        with open(os.path.join(OUTPUT_DIR, filename), 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download tile {filename}: {response.status_code}")

for lat in lat_range:
    for lon in lon_range:
        download_tile(lon, lat, lon + 5, lat + 5)

print("Batch download complete. Files are in the 'south_america_dem' folder.")