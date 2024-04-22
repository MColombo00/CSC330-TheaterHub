import requests
from bs4 import BeautifulSoup
import datetime

f1 = open("MovieLocationScraper/Data Files/AMC/AMC-Theaters-List.txt", "r")
f2 = open("C:/Users/mikec/Desktop/Github/CSC330-TheaterHub/MovieLocationScraper/Data Files/AMC/AMC-Theaters-HTML.txt", "w")
date = datetime.datetime.now()
i = 5

test = [str(f1.readline()).strip().split("/")]

print(test)


# soup = BeautifulSoup(f1.readline(), "html.parser")

# print(f1.readline() + "/showtimes/all/" + str(date.year) + "-" + str(date.month) + "-" + str(date.day))

# for x in range(5):
#     URL = f1.readline() + "/showtimes/all/" + str(date.year) + "-" + str(date.month) + "-" + str(date.day) + 
#     print(URL)

#     page = requests.get(URL)

#     soup = BeautifulSoup(page.content, "html.parser")
#     f2.write(str(soup))
#     colInfo = soup.find_all("div")

#     #f2.write("\n\n\n\n" + URL)


# # print(set([tag.name for tag in soup.find_all()]))
