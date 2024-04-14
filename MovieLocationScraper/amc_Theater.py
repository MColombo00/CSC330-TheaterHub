import requests
from bs4 import BeautifulSoup

URL = "https://www.amctheatres.com/movie-theatres#"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

colInfo = soup.find_all("div")

# print(set([tag.name for tag in soup.find_all()]))
print(colInfo)