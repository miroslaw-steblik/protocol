import requests
from bs4 import BeautifulSoup 
import pandas as pd

webpage = 'https://investment-solutions.mercer.com/europe/uk/en/our-funds.html'

response = requests.get(webpage)
soup = BeautifulSoup(response.content, 'html.parser')

#print(soup.prettify())
table = soup.find('table')





"""
- Initialize BeautifulSoup with the provided HTML content.
- Find all rows by searching for <tr> tags.
- For each row:
  - Extract the fund name from <p class="first-col-text">.
  - Extract the type, ISIN, fund company, and fund code by navigating through subsequent <td> tags.
  - Find all document links within the row by searching for <a> tags with href attributes.
  - For each document link, extract the URL and the document description.
- Store each fund's information in a dictionary with keys for each data point (name, type, ISIN, etc.).
- Append each fund's dictionary to a list for all funds.
- Print or return the list of dictionaries for further processing.
"""

# rows = table.find_all('tr')[1:]  # Skip the header row
# funds_data = []

# for row in rows:
#     cols = row.find_all('td')
#     print(f"Found {len(cols)} columns in this row.")  # Debugging line
#     if len(cols) >= 5:  # Adjusted condition for debugging
#         fund = {
#             'name': cols[0].find('p', class_='first-col-text').text.strip() if cols[0].find('p', class_='first-col-text') else 'N/A',
#             'type': cols[1].text.strip(),
#             'ISIN': cols[2].text.strip(),
#             'fund_company': cols[3].text.strip(),
#             'fund_code': cols[4].text.strip(),
#         }
#         funds_data.append(fund)
#     else:
#         print(f"Skipping a row due to insufficient columns: {row}")  # Debugging line

# df = pd.DataFrame(funds_data)
# print(df)

# ###############################################################################
# # Search for all <td> tags that might contain the ISIN
# td_tags = soup.find_all('td')
# print(f"Found {len(td_tags)} <td> tags.")

# # Placeholder for fund information
# fund_info = None

# for td in td_tags:
#     if "IE00B9JNN477" in td.text:
#         # Navigate to the parent <tr> tag
#         tr = td.find_parent('tr')
#         if tr:
#             cols = tr.find_all('td')
#             # Extract required information
#             fund_info = {
#                 'name': cols[0].find('p', class_='first-col-text').text.strip() if cols[0].find('p', class_='first-col-text') else 'N/A',
#                 'type': cols[1].text.strip(),
#                 'ISIN': cols[2].text.strip(),
#                 'fund_company': cols[3].text.strip(),
#                 'fund_code': cols[4].text.strip(),
#                 # Add more fields as necessary
#             }
#             break  # Stop searching once the ISIN is found

# if fund_info:
#     print("Fund Information:", fund_info)
# else:
#     print("ISIN not found.")


# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
# from bs4 import BeautifulSoup
# import time

# # Set up WebDriver for Firefox
# gecho_driver_path = '/home/miros/DataOps/software/geckodriver'
# service = FirefoxService(executable_path=gecho_driver_path)
# driver = webdriver.Firefox(service=service)

# # Navigate to the page
# driver.get(webpage)

# # Wait for the dynamic content to load
# time.sleep(5)  # Adjust the sleep time as necessary

# # Get the HTML content after JavaScript has loaded
# html_content = driver.page_source

# # Close the browser
# driver.quit()

# # Parse the HTML with BeautifulSoup
# soup = BeautifulSoup(html_content, 'html.parser')

# # Search for <td> tags
# td_tags = soup.find_all('td')

# print(f"Found {len(td_tags)} <td> tags.")

import time

from selenium import webdriver


driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.

driver.get('http://www.google.com/');

time.sleep(5) # Let the user actually see something!

search_box = driver.find_element_by_name('q')

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(5) # Let the user actually see something!

driver.quit()