from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run headless
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

df = pd.read_csv('churches_cleaned.csv')
df['URL'] = ''

for index, row in df.iterrows():
    address = row['Address']
    driver.get("https://www.google.com/")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(address)
    search_box.submit()

    try:
        # Optional delay for dynamic content to load
        time.sleep(2)

        # Wait for search results to load and be visible
        first_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[@class='yuRUbf']/a)[1]"))
        ).get_attribute("href")
        df.at[index, 'URL'] = first_link
    except Exception as e:
        print(f"Error on address {address}: {e}")
        df.at[index, 'URL'] = "N/A"

    # Optional: limit the number of searches for testing
    if index == 3:
        break

df.to_csv('churches_cleaned.csv', index=False)

driver.quit()