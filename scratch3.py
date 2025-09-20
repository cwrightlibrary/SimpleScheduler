from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

import time

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-extensions")
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

url = r"https://richlandlibrary.sharepoint.com/sites/StAndrews/Lists/St%20Andrews%20Calendar/calendar.aspx"

driver.get(url)

username = open("data/office_login.txt", "r", encoding="utf-8").readlines()[0].strip()
password = open("data/office_login.txt", "r", encoding="utf-8").readlines()[1].strip()

email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
email_input.send_keys(username)

next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
next_button.click()

password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
password_input.send_keys(password)

time.sleep(3)

sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
sign_in_button.click()

time.sleep(3)

driver.get(url)

time.sleep(3)

content = driver.page_source

soup = BeautifulSoup(content, "html.parser")

dayrows = soup.find_all("tr", class_="ms-acal-summary-dayrow")

date_query = "9/24/2025"

date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//tr[@date="{date_query}"]')))

date_element.click()

