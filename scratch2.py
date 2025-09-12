from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Setup Selenium options
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-extensions")
options.add_argument("--headless")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Define the RSS URL
rss_url = r"https://richlandlibrary.sharepoint.com/sites/StAndrews/_layouts/15/listfeed.aspx?List=%7B12B7C455%2DEF3E%2D4D72%2D9E7B%2D7A480BF14DC0%7D&Source=https%3A%2F%2Frichlandlibrary%2Esharepoint%2Ecom%2Fsites%2FStAndrews%2FLists%2FSt%2520Andrews%2520Calendar%2Fcalendar%2Easpx"

# Open the webpage
driver.get(rss_url)

# Read credentials from the file
username = open("data/office_login.txt", "r", encoding="utf-8").readlines()[0].strip()
password = open("data/office_login.txt", "r", encoding="utf-8").readlines()[1].strip()

# Log in process (email input)
email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
email_input.send_keys(username)

# Click Next
next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
next_button.click()

# Wait for password input and enter it
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
password_input.send_keys(password)

# Sleep to allow sign-in process to complete
time.sleep(3)

# Click sign-in button
sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
sign_in_button.click()

# Allow for full sign-in and page load
time.sleep(3)

# Reload the RSS page
driver.get(rss_url)

# Wait for the page to fully load
time.sleep(3)

# Get the page source (raw HTML)
rss_content = driver.page_source

# Save the raw HTML to a file (optional)
with open("data/rss_feed.txt", "w", encoding="utf-8") as f:
    f.write(rss_content)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(rss_content, "html.parser")

# Pretty-print the HTML to see the structure
pretty_html = soup.prettify()

# Optionally print the cleaned up, readable HTML
print(pretty_html)

# Now you can start selecting data using BeautifulSoup
# For example, find all <item> tags if this is an RSS feed structure:
items = soup.find_all("item")
for item in items:
    title = item.find("title").text if item.find("title") else "No title"
    link = item.find("link").text if item.find("link") else "No link"
    description = item.find("description").text if item.find("description") else "No description"
    
    print(f"Title: {title}")
    print(f"Link: {link}")
    print(f"Description: {description}\n")

# Close the browser
driver.quit()
