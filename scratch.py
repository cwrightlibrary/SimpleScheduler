from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import time

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-extensions")
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

rss_url = r"https://richlandlibrary.sharepoint.com/sites/StAndrews/_layouts/15/listfeed.aspx?List=%7B12B7C455%2DEF3E%2D4D72%2D9E7B%2D7A480BF14DC0%7D&Source=https%3A%2F%2Frichlandlibrary%2Esharepoint%2Ecom%2Fsites%2FStAndrews%2FLists%2FSt%2520Andrews%2520Calendar%2Fcalendar%2Easpx"

driver.get(rss_url)

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

driver.get(rss_url)

time.sleep(3)

rss_content = driver.page_source

soup = BeautifulSoup(rss_content, "html.parser")
pretty_html = soup.prettify()

divs = soup.find_all("div", class_="ms-inputuserfield padfive seventyp")

changes_list = []

for div in divs:
  name = div.find("h4").find("a").text.strip()
  start_time = div.find("div").find_all("div")[0].text.strip().replace("Start Time:", "").strip()
  end_time = div.find("div").find_all("div")[1].text.strip().replace("End Time:", "").strip()
  # formatted_str = f"{name}\nStart Time: {start_time}\nEnd Time: {end_time}"
  # changes_list.append(formatted_str)
  change = [name, start_time, end_time]
  changes_list.append(change)

# for item in changes_list:
#   print(item)
#   print("\n---\n")

driver.quit()