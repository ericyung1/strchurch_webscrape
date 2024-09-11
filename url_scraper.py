from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
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

    time.sleep(1)

    try:
        first_link = driver.find_element(By.XPATH, "//div[@class='g']//a").get_attribute("href")
        df.at[index, 'URL'] = first_link
    except Exception as e:
        print(f"Error on address {address}: {e}")
        df.at[index, 'URL'] = "N/A"

df.to_csv('churches_cleaned.csv', index=False)