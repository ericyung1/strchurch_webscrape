import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.stlouischurches.org"

# Create a list to store church data
church_data = []

# Function to collect church details from a zip code page
def collect_church_details_from_zip(zip_url):
    print(f"Processing zip code page: {zip_url}")
    response = requests.get(zip_url)
    zip_soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the div with id 'listings'
    listings_div = zip_soup.find('div', id='listings')
    
    if listings_div:
        # Find all church entries within the listings div
        church_entries = listings_div.find_all('div', class_='listing-summary')
        
        for entry in church_entries:
            church_name = entry.find('h3').text.strip() if entry.find('h3') else 'N/A'
            phone_number = entry.find('div', id='field_9').find('span', class_='output').text.strip() if entry.find('div', id='field_9') else 'N/A'
            zip_code = entry.find('p', class_='address').find_all('a')[-1].text.strip() if entry.find('p', class_='address') else 'N/A'
            address = entry.find('p', class_='address').text.strip() if entry.find('p', class_='address') else 'N/A'
            denomination = entry.find('div', id='field_36').find('span', class_='output').text.strip() if entry.find('div', id='field_36') else 'N/A'
            
            # Combine church details
            full_details = [church_name, phone_number, zip_code, address, denomination, 'MO']  # Add state abbreviation
            church_data.append(full_details)
    else:
        print(f"No listings found on page: {zip_url}")

# Function to collect church details from a category page
def collect_church_details_from_category(category_url):
    print(f"Processing category page: {category_url}")
    response = requests.get(category_url)
    category_soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all row-fluid divs
    rows = category_soup.find_all('div', class_='row-fluid')
    
    for row in rows:
        # Find all span6 divs within each row
        entries = row.find_all('div', class_='span6')
        for entry in entries:
            # Extract and print the text of each a tag
            links = entry.find_all('a')
            for link in links:
                zip_name = link.text.strip()
                if zip_name not in ["Read More", "Hide map", "Other"]:  # Skip unwanted entries
                    zip_url = base_url + link['href']  # Complete URL
                    print(f"Found zip code: {zip_name}")
                    
                    # Collect church details from this zip code page
                    collect_church_details_from_zip(zip_url)

# Send a GET request to the main page
url = "https://www.stlouischurches.org"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the categories
categories = soup.find_all('div', class_='category')

# Iterate through each category to extract and visit its hyperlink
for category in categories:
    category_tag = category.find('h2').find('a')
    category_name = category_tag.text.strip()
    category_url = base_url + category_tag['href']  # Complete URL
    
    # Collect church details from this category
    print(f"Processing category: {category_name}")
    collect_church_details_from_category(category_url)

# Print the collected data to debug
print(church_data)

# Convert the collected data to a DataFrame
df = pd.DataFrame(church_data, columns=['Church Name', 'Phone Number', 'Zip Code', 'Address', 'Denomination', 'State'])

# Write the DataFrame to an Excel file
df.to_excel('churches_cleaned.xlsx', index=False)

print("Data has been written to 'churches_cleaned.xlsx'")
