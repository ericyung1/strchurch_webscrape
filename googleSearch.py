import pandas as pd
import requests
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from .env file using find_dotenv()
load_dotenv(find_dotenv())

# API Key and Search Engine ID from .env file
API_KEY = os.getenv('API_KEY')
CX = os.getenv('CX')

# Function to search using Google API
def google_search(query):
    print(f"Searching for: {query}")  # Print the current search query
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}"
    response = requests.get(url).json()
    # Extract the first search result URL
    if "items" in response:
        return response["items"][0]["link"]
    else:
        return "No result found"

# Read CSV file (adjust 'churches_cleaned.csv' to your actual file name)
df = pd.read_csv('test - Sheet1.csv')

# Limit to 500 rows for search
max_rows = 500
df['URL'] = df['Address'].head(max_rows).apply(google_search)

# Save the updated CSV file
df.to_csv('updated_churches.csv', index=False)

print("URLs added successfully.")