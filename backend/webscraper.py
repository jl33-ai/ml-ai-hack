"""
Webscraping articles
Created by Harrison

Note difference for yearly, daily and active calls
Todo:
Scrape ptv websites

"""


import time
import requests
from bs4 import BeautifulSoup as Bs
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


# PTV websites
# Main ptv website: https://www.ptv.vic.gov.au
# https://www.ptv.vic.gov.au/disruptions/disruptions-information/
# Distruptions:
    # https://twitter.com/ptv_official?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor
    # https://www.ptv.vic.gov.au/disruptions/disruptions-information/#

# Fares: https://www.ptv.vic.gov.au/tickets/fares/
    # Metro fares: https://www.ptv.vic.gov.au/tickets/fares/metropolitan-fares/
# Fares:
    # https://www.ptv.vic.gov.au/tickets/fares/zones/


# Boilerplate
headers = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/75.0.3770.142 Safari/537.36'
    }

"""
Function to make all generic request calls
"""
def soup_maker(url):
    request_data = requests.get(url, headers=headers).content
    soup = Bs(request_data, features="html.parser")
    return soup


"""
function to call information for distruptions
Call depending on live update or current daily updates
"""
def ptv_disruptions(news=False):

    disruption_url = "https://www.ptv.vic.gov.au/disruptions/disruptions-information/#"

    # Set the path to the OperaDriver
    opera_driver_path = 'C:/WebDrivers/operadriver.exe'

    # Set the location of the Opera Browser
    # options = webdriver.ChromeOptions()
    # options.binary_location = 'path/to/your/opera.exe'  # Example: 'C:/Program Files/Opera/launcher.exe'

    # Initialize the WebDriver with the specified options
    driver = webdriver.Chrome()


    driver.get(disruption_url)

    try:
        accordion_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "accordion__button"))
        )
        accordion_button.click()
        print("Click successful")
        html_content = driver.page_source
        raw_html = Bs(html_content, 'html.parser')
        
        # text processing
        # print(raw_html)
        if raw_html:
            live_updates = raw_html.find("div", class_={"accordion LiveTravelUpdates__accordion"})
            # print(live_updates)
            for update in live_updates.findAll("li"):
                print(update.text)
                print("-------------------------------")
        else:
            print("Error")
        

    finally:
        # Close the WebDriver
        driver.quit()


    # raw_html = soup_maker(disruption_url)
    # if raw_html:
    #     print("Data scraped")
    #     distruption_list = raw_html.find(id={"accordion-2"})
    #     print(distruption_list)
        # for disruption in distruption_list.find_all("li"):
            
        #     print(disruption.content)

    return "Error occured in data extraction"


ptv_disruptions()