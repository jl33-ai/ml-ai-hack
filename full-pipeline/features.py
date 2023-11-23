import requests

# how model uses APIs
DETAILS = [
    {
        "name": "getCurrentWeather",
        "description": "Get the current weather in a given location given in latitude and longitude",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "decimal",
                },
                "longitude": {
                    "type": "decimal",
                }
            },
            "required": ["latitude", "longitude"]
        }
    },
    {
        "name": "getStartingLocation",
        "description": "Get the user's location based on their IP address",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }, 
    {
        "name": "getServiceInfo",
        "description": "Get specific information about the PTV system",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

# return lat, long pair
def getStartingLocation():
    response = requests.get("https://ipapi.co/json/").json()
    return response['latitude'], response['longitude']

def getCurrentWeather(latitude, longitude):
    return requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=apparent_temperature&hourly=apparent_temperature").json()

def getServiceInfo():
    return "The Public Transport Victoria (PTV) system is a comprehensive network of train, tram, and bus services operating in Victoria, Australia, especially in Melbourne. Trains, the backbone of Melbourne's public transport, connect suburbs to the city center. The city's iconic trams provide convenient inner-city travel, while buses cover areas less accessible by rail. Ticketing is managed via the myki card, a rechargeable smart card used across all modes of transport. Fares depend on travel zones and times, with options for daily caps and concessions. The system is accessible, featuring low-floor trams, tactile indicators, and equipped stations and stops. Operational hours for trains and trams extend to around midnight, with all-night services on weekends under the Night Network. Buses run on various schedules, often with reduced weekend services. PTV offers real-time information through displays, a journey planner, and a mobile app, aiding in travel planning and service updates. Safety is ensured through patrols, rules like myki validation, and CCTV surveillance. PTV emphasizes environmental sustainability by reducing emissions and promoting public transport to lessen road congestion. Continuous improvements and expansions are made to accommodate Melbourne's growing population, including infrastructure upgrades and new services. As a crucial part of Melbourne's urban dynamics, PTV is essential for commuters, students, tourists, and the public, known for its efficiency and coverage."

OPTIONS = {'getStartingLocation': getStartingLocation, 'getCurrentWeather': getCurrentWeather, 'getServiceInfo': getServiceInfo}

# test
print(getStartingLocation(), getCurrentWeather(*getStartingLocation()))