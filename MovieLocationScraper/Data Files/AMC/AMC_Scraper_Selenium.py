import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from random import randint
import time
import schedule 


def job():
    f1 = open("MovieLocationScraper/Data Files/AMC/AMC-Theaters-List.txt", "r")

    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    movie_list = []

    for x in range(5):
    # for x in f1:
        ourl = f1.readline().strip()
        url = ourl + "/showtimes"
        # print(url)
        driver.get(url)
        print("Headless Firefox Initialized for URL: " + url)
        time.sleep(5)
        location = url.strip('/').split('/')[-2]
        theater = url.strip('/').split('/')[-3]
        # print(location)
        # print(theater)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        all_data = soup.find_all(['div'], class_='ShowtimesByTheatre-film')

        
        for x in all_data:
            # print(x)
            # location = url.strip().split("/")
            # print(location[4])
            showtimes = []
            title = ""

            find_h2 = x.find("h2")
            for n in find_h2:
                title = n.get_text()

            st_unit = x.find_all("a", class_="Btn Btn--default")
            for st in st_unit:
                showtimes.append(st.get_text())

            for t in showtimes:
                mov_dat = {
                    'movie': title,
                    'time': t,
                    'location': location,
                    'theater': theater
                }
                movie_list.append(mov_dat)

    # print(movie_list)

    with open('MovieLocationScraper\Data Files\AMC\\amc-movies.json', 'w') as file:
        json.dump(movie_list, file, indent=4)

    driver.quit()

job()

# schedule.every().day.at("00:00").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)