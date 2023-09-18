import re
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

base_url = 'https://xt-xarid.uz/procedure/tender?status=close'
driver.get(base_url)

data_list = []
time.sleep(3)

ui_list_content = driver.find_element(By.CLASS_NAME, 'items')
data_view_items = ui_list_content.find_elements(By.CLASS_NAME, 'data-view-item')

for item in data_view_items:
    tender_number = item.find_element(By.XPATH, './/div/span[contains(text(), "№")]').text.strip()
    lot_link = item.find_element(By.XPATH, './/div[@class="title"]/label/a').get_attribute('href')
    tender_name = item.find_element(By.XPATH, './/div[@class="title"]/label/a').text.strip()
    deadline = item.find_element(By.XPATH, './/div[contains(label, "Якунланиш муддати:")]/div/time').text.strip()

    pattern = r'\d+\s+[А-Яа-я]+\s+\d+'

    match = re.search(pattern, deadline)

    if match:
        extracted_date = match.group()
    else:
        extracted_date = deadline

    tender_info = {
        "Tender Number": tender_number,
        "Lot Link": lot_link,
        "Tender Name": tender_name,
        "Deadline": extracted_date,
    }

    data_list.append(tender_info)

driver.quit()

df = pd.DataFrame(data_list)

excel_file = 'harid.xlsx'
df.to_excel(excel_file, index=False)
