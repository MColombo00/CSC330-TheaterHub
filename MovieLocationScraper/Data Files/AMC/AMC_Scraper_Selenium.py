import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://www.amctheatres.com/movie-theatres/morristown/amc-headquarters-plaza-10/showtimes/all/2024-04-24/amc-headquarters-plaza-10/all"

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
driver.get(url)

time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

data = soup.find_all(['h2','a'])

print(soup.find('h2', class_ = "").get_text())
# div_ob = []

# for div in data:
#     mov = div.find('h2', class_ = "").get_text()
#     showing = div.find('a', class_ = "Btn Btn--default")




#     div_data = {
#         'movie' : ,
#         'time' : div.find('a', class_ = "Btn Btn--default")
#     }
#     div_ob.append(div_data)

# with open('MovieLocationScraper\Data Files\AMC\divs_output.json', 'w') as file:
#    json.dump(div_ob, file, indent = 4)

driver.close()