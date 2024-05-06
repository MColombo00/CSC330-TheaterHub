import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from random import randint
import time
import schedule 


def job():
    f1 = open("MovieLocationScraper/Data Files/AMC/AMC-Theaters-List.txt", "r")

    #Creates a headless webdriver to mimic a human using Selenium
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    movie_list = []

    #filtering through the 557 links for each theater from "AMC-Theaters-List.txt"
    for x in range(557):
        ourl = f1.readline().strip()

        # Adding /showtimes to display all movies playing at this location. otherwise it would pull the main menu for that theater.
        # then the webdriver gets the url of the theater and parses the HTML of each web page using BeautifulSoup. 
        #program sleeps for 3 seconds to avoid being IP blocked.
        url = ourl + "/showtimes"   
        driver.get(url)     
        print("Headless Firefox Initialized for URL: " + url) 
        time.sleep(3)
        location = url.strip('/').split('/')[-2]
        theater = url.strip('/').split('/')[-3]
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        all_data = soup.find_all(['div'], class_='ShowtimesByTheatre-film')

        #filtering through each h2 element and getting the text.
        #then it finds all buttons with the class name below.
        #finally it appends the data from the button and adds it to the showtimes list
        for x in all_data:

            showtimes = []
            title = ""

            find_h2 = x.find("h2")
            for n in find_h2:
                title = n.get_text()

            st_unit = x.find_all("a", class_="Btn Btn--default")
            for st in st_unit:
                showtimes.append(st.get_text())
            
            #this creates a movie with its respective details and adds it to the movie_list
            for t in showtimes:
                mov_dat = {
                    'movie': title,
                    'time': t,
                    'location': location,
                    'theater': theater
                }
                movie_list.append(mov_dat)

    #opens our amc-movies-json file so we can write to it
    with open('MovieLocationScraper\Data Files\AMC\\amc-movies.json', 'w') as file:
        json.dump(movie_list, file, indent=4) #dumps our movie list into the json file

    print("Done!")
    driver.quit() #stops the web driver to remove any unnecessary resources

job()

#schedule to run the scraper every day at midnight

# schedule.every().day.at("00:00").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)