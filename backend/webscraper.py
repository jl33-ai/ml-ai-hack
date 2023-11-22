"""
Webscraping articles
Created by Harrison

Note difference for yearly, daily and active calls
Todo:
Scrape ptv websites
Add weather data
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
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


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

# run when using selenium
driver = webdriver.Chrome()

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
def ptv_disruptions(news=False, transport_option="train"):

    disruption_url = "https://www.ptv.vic.gov.au/disruptions/disruptions-information/#"

    # Depending on the transport type affects distruption
    select_transport_option(transport_option)

    return "Error occured in data extraction"


def select_transport_option(option):
    print(f"Getting distruption data for {option}")
    driver.get('https://www.ptv.vic.gov.au/disruptions/disruptions-information/')
    option_ids = {
        "train": "tabtitle-0",
        "tram": "tabtitle-1",
        "bus": "tabtitle-2",
        "vline": "tabtitle-3"
    }
    # Waiting for page to load
    time.sleep(2)

    button_id = option_ids.get(option.lower())
    if not button_id:
        print("Invalid option")
        return

    try:
        button = driver.find_element(By.ID, button_id)
        button.click()
    except NoSuchElementException:
        print("Button not found")

    try:
        accordion_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "accordion__button"))
        )
        accordion_button.click()
        print("Click successful")
        html_content = driver.page_source
        raw_html = Bs(html_content, 'html.parser')
        
        # text processing
        if raw_html:
            live_updates = raw_html.find("div", class_={"accordion LiveTravelUpdates__accordion"})
            # print(live_updates)
            updates_list = live_updates.findAll("li")
            for update in updates_list  :
                print(update.text)
                print("-------------------------------")
            return updates_list
        else:
            print("Error")
        

    finally:
        # Close the WebDriver
        driver.quit()

# Weather data
# Melbourne lat and long 37.8136, 144.9631
def get_weather(api_key, city="Melbourne", country="AU", forcast=False, current_weather=True):
    # base_url = "http://api.openweathermap.org/data/2.5/weather"
    geo_loc = f"http://api.openweathermap.org/geo/1.0/direct?q={city},Victoria,AU&limit=5&appid={api_key}"
    geo_loc_request = requests.get(geo_loc)
    if geo_loc_request.status_code == 200:
        geo_data = geo_loc_request.json()
        lat = geo_data[-1]["lat"]
        lon = geo_data[-1]["lon"]
    else:
        print("Error fetching location")

    weather_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}"
    # Note for forcast, require pro version
    forcast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    if current_weather:
        response = requests.get(weather_url)

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperature = main['temp']
            humidity = main['humidity']
            weather_description = data['weather'][0]['description']

            print(f"Weather in {city}: {weather_description}")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
        else:
            print("Error fetching weather data")
    
    if forcast:
        
        response_forcast = requests.get(forcast_url)

        if response_forcast.status_code == 200:
            # Get weather forcast every 3 hours for next 12 hours
            data = response_forcast.json()
            main = data["list"][:4]
            # Wondering if I should just chuck the raw json into the LLM and let it figure out the data
            # for forcast_point in main:
            #     temperature = forcast_point["main"]['temp']
            #     humidity = main['humidity']
            #     weather_description = data['weather'][0]['description']

            #     print(f"Weather in {city}: {weather_description}")
            #     print(f"Temperature: {temperature}°C")
            #     print(f"Humidity: {humidity}%")
        else:
            print("Error fetching forcast data")

# Site to scrape the train station data, only need to run once
def train_station_data():
    station_url = "https://en.wikipedia.org/wiki/List_of_Metro_Trains_Melbourne_railway_stations"
    soup = soup_maker(station_url)
    # webscraping doesn't seem to work, trying to pen the site
    driver.get(station_url)
    time.sleep(1)
    html_content = driver.page_source
    raw_html = Bs(html_content, 'html.parser')

    # print(raw_html)
    table_data = raw_html.find("table", class_="wikitable sortable mw-collapsible sticky-header jquery-tablesorter mw-made-collapsible")
    # table_data = soup.findAll("table")
    rows = table_data.find_all("tr")
    print(table_data.find("tbody"))
    # rows[0] is the header column, typically ignore, just need the titles

    # Headers for data
    """
    Name

    Image

    Transport
    connections


    Service(s)

    Distance from Southern Cross[4]

    Zone(s)

    Date opened[5]

    Suburb

    Notes
    [5]
    """

    # if rows:
    #     print(rows)
            

# Replace 'your_api_key' with your actual OpenWeatherMap API key
api_key = '54eb710c29de0ff841c5889195af540d'

# get_weather(api_key, current_weather=False, forcast=True)
# ptv_disruptions()
# ptv_disruptions(transport_option="bus")
train_station_data()
