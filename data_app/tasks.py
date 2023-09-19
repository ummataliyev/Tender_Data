import re
import time
import datetime
import pandas as pd

from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from celery import shared_task

from data_app.models import Job

from data_app.utils import send_telegram


@shared_task
def adb_script():
    print("Task number one")

    # Create a WebDriver instance (you might need to specify the path to your chromedriver executable)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Use the correct path
    chrome_options.add_argument("--headless")  # Optional, for running in headless mode
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options)  # Path to ChromeDriver on your server

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

        if all_data:
            for data_item in all_data:
                Job.objects.create(
                    company_name=data_item['Title'],
                    link=data_item['Link'],
                    is_active=data_item['Status'] == "Active"
                )

            # Send a Telegram message using your send_telegram function
            send_telegram("New Updates On Tenders")
        else:
            print("No data to save. Stopping the scraping process.")

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


# @shared_task
# def xt_script():
#     print("Task number two")
#     driver = webdriver.Chrome()

#     base_url = 'https://xt-xarid.uz/procedure/tender?status=close'
#     driver.get(base_url)

#     data_list = []
#     time.sleep(3)

#     ui_list_content = driver.find_element(By.CLASS_NAME, 'items')
#     data_view_items = ui_list_content.find_elements(By.CLASS_NAME, 'data-view-item')

#     for item in data_view_items:
#         tender_number = item.find_element(By.XPATH, './/div/span[contains(text(), "№")]').text.strip()
#         lot_link = item.find_element(By.XPATH, './/div[@class="title"]/label/a').get_attribute('href')
#         tender_name = item.find_element(By.XPATH, './/div[@class="title"]/label/a').text.strip()
#         deadline = item.find_element(By.XPATH, './/div[contains(label, "Якунланиш муддати:")]/div/time').text.strip()

#         pattern = r'\d+\s+[А-Яа-я]+\s+\d+'

#         match = re.search(pattern, deadline)

#         if match:
#             extracted_date = match.group()
#             russian_month_names = [
#                 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
#                 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
#             ]

#             try:
#                 # Parse the extracted date using the dateutil parser
#                 extracted_datetime = date_parser.parse(extracted_date, dayfirst=True, monthparser=russian_month_names)
#                 # Get the current date and time
#                 current_datetime = datetime.datetime.now()

#                 # Compare the extracted date with the current date
#                 status = extracted_datetime > current_datetime
#             except (ValueError, OverflowError):
#                 # Handle the case where the date couldn't be parsed
#                 extracted_date = deadline
#                 status = False
#         else:
#             extracted_date = deadline
#             status = False

#         # Save the data to the database

#         Job.objects.create(
#             company_name=tender_name['Tender Number'],
#             link=lot_link['Lot Link'],
#             is_acvtive=status['Deadline']
#         )

#         tender_info = {
#             "Tender Number": tender_number,
#             "Lot Link": lot_link,
#             "Tender Name": tender_name,
#             "Deadline": extracted_date,
#         }

#         data_list.append(tender_info)

#     driver.quit()

#     df = pd.DataFrame(data_list)

#     excel_file = 'harid.xlsx'
#     df.to_excel(excel_file, index=False)
