from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time


PATH_TO_DRIVER = "C:/Chrome Driver/chromedriver.exe"    # path to where your 'chromedriver.exe' is installed
WEBSITE_URL = "https://soundcloud.com/"

driver = webdriver.Chrome(PATH_TO_DRIVER)

# fetching the soundcloud website using the driver
driver.get(WEBSITE_URL)

try:
    # waiting to find tbe button for accepting all cookies
    accept_cookies = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
except TimeoutException:
    print("The request timed out trying to find the element.")
else:
    # accept all cookies
    accept_cookies.click()

    # finding the button for exploring playlists
    explore_playlists = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[3]/a")

    # scrolling to the 'explore_playlists' button and moving the mouse on-top it
    actions = ActionChains(driver)
    actions.move_to_element(explore_playlists).perform()

    # see all the playlists
    explore_playlists.click()

    try:
        # waiting to find the button for seeing the top 50 playlist
        top_50_playlist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div/ul/li[1]/div/div[3]/div/a")))
    except TimeoutException:
        print("The request timed out trying to find the element")
    else:
        # see the top-50 playlist
        top_50_playlist.click()

        try:
            # getting the driver to wait until the first song has loaded
            first_song = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div[2]/ul/li[1]/div/div[3]")))
        except TimeoutException:
            print("The request timed out trying to find the element.")
        else:
            # scrolling down to the end of the page to load all the songs
            not_yet_at_page_end = True
            previous_heights = []

            while not_yet_at_page_end:
                # wait for 2 seconds
                time.sleep(2)

                # scrolling down to the end of the page to load the songs and returning the current page height
                page_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);return document.body.scrollHeight")

                # appending the current page height to the 'previous_heights' array
                previous_heights.append(page_height)

                # start checking if we have reached the end when the page has been scrolled more than once
                if len(previous_heights) > 1:
                    # if the last 2 heights are the same, then we have reached the end of the page
                    if previous_heights[-1] == previous_heights[-2]:
                        not_yet_at_page_end = False

            current_page_html = driver.page_source

            # making soup with the current page
            soup = BeautifulSoup(current_page_html, "html.parser")

            # finding all the songs and the number of times each was played
            songs = soup.select("div.trackItem__content.sc-truncate")
            count_info = soup.select("div.trackItem__additional")

            top_50_songs = []   # list of the top-50 songs

            # looping through the songs and the number of times each song was played
            for song, count in zip(songs, count_info):
                song_name = song.select_one("a.trackItem__trackTitle.sc-link-dark.sc-link-primary.sc-font-light")
                no_of_times_played = count.select_one("span.trackItem__playCount.sc-ministats.sc-ministats-medium.sc-ministats-plays")

                # checking if the number of times played is not available for a specific song
                if no_of_times_played is None:
                    times_played = 0
                else:
                    times_played = no_of_times_played.getText().replace("\n", "").replace(" ", "")   # remove newlines and spaces

                # appending a dictionary with a key and the value to the 'top_50_songs' list
                top_50_songs.append({
                    "song": song_name.getText(),
                    "times_played": times_played
                })

            # creating a dataframe from the 'top_50_songs' list
            data = pd.DataFrame(top_50_songs, columns=["song", "times_played"])

            # writing the dataframe created to a csv file
            data.to_csv("top-5-songs.csv")

# closing down the driver
driver.close()
