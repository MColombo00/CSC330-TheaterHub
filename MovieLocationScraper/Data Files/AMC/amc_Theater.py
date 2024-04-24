import requests
from bs4 import BeautifulSoup
import datetime

f1 = open("MovieLocationScraper/Data Files/AMC/AMC-Theaters-List.txt", "r")
f2 = open("C:/Users/mikec/Desktop/Github/CSC330-TheaterHub/MovieLocationScraper/Data Files/AMC/AMC-Theaters-HTML.txt", "w")
date = datetime.datetime.now()


# print(date)
i = 5

location = str(f1.readline()).strip().split("/")


# soup = BeautifulSoup(f1.readline(), "html.parser")

for x in range(1):
    OURL = f1.readline().strip()
    NURL = OURL + "/showtimes/all/" + str(date.year) + "-" + str(date.month) + "-" + str(date.day)

    print(NURL)

    page = requests.get(NURL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    f2.write( str(NURL) + "\n\n" + str(soup) + "\n\n\n")


