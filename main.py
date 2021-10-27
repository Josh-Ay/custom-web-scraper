from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

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

        # making soup with the current page source
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # finding all the songs and the number of times each was played
        song_names = soup.select("span.systemPlaylistBannerItem__trackTitle.sc-font")
        times_played_list = soup.select("span.systemPlaylistBannerItem__playCount.sc-ministats.sc-ministats-inverted.sc-ministats-small.sc-ministats-plays")

        top_50_songs = []   # list of the top-50 songs

        # looping through the songs and the number of times each song was played
        for song, times_played in zip(song_names, times_played_list):
            # appending a dictionary with a key and the value to the 'top_50_songs' list
            top_50_songs.append({
                "song": song.getText(),
                "times_played": times_played.getText().replace("\n", "").replace(" ", "")   # remove newlines and spaces
            })

        print(top_50_songs)

# closing down the driver
driver.close()
