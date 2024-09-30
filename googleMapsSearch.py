import requests
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os

# Step 1: Load API key from .env file
load_dotenv(find_dotenv())  # Finds and loads the .env file
API_KEY = os.getenv('API_KEY')  # Retrieves the API key from the .env file

# Verify that the API key is loaded correctly
if not API_KEY:
    raise ValueError("API Key not found. Please set GOOGLE_PLACES_API_KEY in your .env file.")

# Step 2: Search for place using Google Places API
def get_place_details(address, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': address,
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': api_key
    }
    response = requests.get(url, params=params)
    result = response.json()
    
    if result['status'] == 'OK':
        place_id = result['candidates'][0]['place_id']
        return place_id
    else:
        return None

# Step 3: Get website from place details
def get_website_from_place_id(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'website',
        'key': api_key
    }
    response = requests.get(url, params=params)
    result = response.json()
    
    if result['status'] == 'OK' and 'website' in result['result']:
        return result['result']['website']
    else:
        return None

# Step 4: Read CSV, update with URLs, and save it back to the same file
def update_csv_with_urls(filename, max_iterations=None):
    # Read the CSV file
    # df = pd.read_csv(filename)
    df = pd.read_csv(filename, on_bad_lines='skip')
    print(df.info())

    # Ensure there is an 'Address' column in the CSV
    if 'Address' not in df.columns:
        raise ValueError("The CSV file does not have an 'Address' column.")
    
    # Create a new 'URL' column if it doesn't exist
    if 'URL' not in df.columns:
        df['URL'] = None
    
    # Cap the number of rows to process based on `max_iterations`
    total_rows = len(df)
    rows_to_process = min(max_iterations, total_rows) if max_iterations else total_rows
    
    # Iterate through the addresses and update URLs
    for idx in range(rows_to_process):
        address = df.loc[idx, 'Address']
        place_id = get_place_details(address, API_KEY)
        
        if place_id:
            website = get_website_from_place_id(place_id, API_KEY)
            if website:
                df.at[idx, 'URL'] = website
                print(f"Website found for {address}: {website}")
            else:
                print(f"No website found for {address}")
        else:
            print(f"Place not found for the address: {address}")
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)
    print(f"Updated CSV saved successfully as {filename}")

# Example usage
# You can set `max_iterations` to any number, such as 100, to process up to 100 rows.
update_csv_with_urls('churches_list_updated.csv', max_iterations=100)