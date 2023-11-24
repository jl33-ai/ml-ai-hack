"""
Webscraping articles
Created by Harrison

Note difference for yearly, daily and active calls
Todo:
Scrape ptv websites
Add weather data
"""

# remove these for now to ensure no errors in deployment
#import time
#import requests
#from bs4 import BeautifulSoup as Bs
#import re
#import pandas as pd

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
    return select_transport_option(transport_option)


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
        return

    try:
        button = driver.find_element(By.ID, button_id)
        button.click()
    except:
        pass

    try:
        accordion_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "accordion__button"))
        )
        accordion_button.click()
        html_content = driver.page_source
        raw_html = Bs(html_content, 'html.parser')
        
        # text processing
        if raw_html:
            live_updates = raw_html.find("div", class_={"accordion LiveTravelUpdates__accordion"})
            # print(live_updates)
            updates_list = live_updates.find_all("li")
        
            return [update.text for update in updates_list]
        

    finally:
        # Close the WebDriver
        driver.quit()

    return 

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

"""
Scrapes whats on melb
"""
def melb_events():
    url = "https://whatson.melbourne.vic.gov.au/search/things-to-do"
    base_url = "https://whatson.melbourne.vic.gov.au/"
    soup = soup_maker(url)
    event_list = soup.find("div", class_="list-module-contents list-results")
    event_list = event_list.find_all("div", class_="page-preview fill-height preview-type-list-square")
    
    out = {}
    
    for event in event_list:
        try:
            event_html = event.find("a", class_="main-link")
            title = event_html.find("h2", class_="title").text
            summary = event.find("p", class_="summary").text
            event_link = event.find("a")
            event_link = f"{base_url}{event_link.get('href')}"
            event_date = event_html.find("time").text
            event_type = event.find("ul", class_="tag-list").text

            out[event_link] = {
                                "title": title,
                                "summary": summary,
                                "event_date": event_date,
                                "event_type": event_type,
                            }

        except:
            pass

    
    return out
        

# Replace 'your_api_key' with your actual OpenWeatherMap API key
api_key = '54eb710c29de0ff841c5889195af540d'

print(ptv_disruptions())
print("\n")
print(melb_events())
