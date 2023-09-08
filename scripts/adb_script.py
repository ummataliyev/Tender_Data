import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a WebDriver instance (you might need to specify the path to your chromedriver executable)
driver = webdriver.Chrome()

# Define the base URL
base_url = 'https://www.adb.org/projects/tenders/sector/information-and-communication-technology-1066/status/active-1576'

# Initialize lists to store the extracted data
all_data = []

# Function to extract data from a page
def extract_data():
    # Check if the "No projects found..." message is present
    empty_message = driver.find_elements(By.CSS_SELECTOR, 'div.view-empty h4')
    if empty_message:
        print("No projects found. Stopping the scraping process.")
        return False

    # Find all 'div' elements with class 'item-title'
    item_elements = driver.find_elements(By.CSS_SELECTOR, 'div.item')
    print(item_elements)

    for item_element in item_elements:
        # Extract title and href
        item_title_element = item_element.find_element(By.CSS_SELECTOR, 'div.item-title')
        title_text = item_title_element.text.strip()
        a_element = item_title_element.find_element(By.TAG_NAME, 'a')
        href = a_element.get_attribute('href')

        # Extract status
        item_meta_element = item_element.find_element(By.CSS_SELECTOR, 'div.item-meta')
        status_element = item_meta_element.find_element(By.XPATH, './div/span[1]/following-sibling::span')
        status_text = status_element.text.strip()

        # Only append data if the status is "Active"
        if status_text == "Active":
            all_data.append({'Title': title_text, 'Link': href, 'Status': status_text})

    return True

# Start from page 0
page = 0

try:
    while True:
        # Construct the URL for the current page
        url = f'{base_url}?page={page}'

        driver.get(url)

        # Extract data from the current page
        if not extract_data():
            break  # Exit the loop if "No projects found" message is present

        # Find the "Next" button and wait for it to be clickable
        next_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "?page=")]'))
        )

        # Check if the "Next" button is enabled (clickable)
        if not next_button.is_enabled():
            break  # Exit the loop if there is no "Next" button

        # Increment the page number to go to the next page
        page += 1

except Exception as e:
    print("Error occurred:" + str(e))
finally:
    # Close the WebDriver
    driver.quit()

# Create a DataFrame from the extracted data
df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
df.to_excel('adb.xlsx', index=False)
