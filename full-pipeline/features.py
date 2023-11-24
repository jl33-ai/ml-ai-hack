import requests, streamlit as st, json
# googlemaps

# how model uses APIs
DETAILS = [
    {
        "name": "getCurrentWeather",
        "description": '''Get current and future apparent temperature at current location,
                          max UV index for the day, 
                          and hourly precipitation probability
                          (Probability of precipitation with more than 0.1 mm of the preceding hour)''',
        "parameters": {
            "type": "object",
            "properties": {}
            # "properties": {
            #     "latitude": {
            #         "type": "string",
            #     },
            #     "longitude": {
            #         "type": "string",
            #     }
            # },
            # "required": ["latitude", "longitude"]
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
        "name": "getEvents",
        "description": '''returns a json containing the latest events, the syntax for each event json is: 
                          name of event: {'summary': brief information about the event, 
                                          'event_date': relative date of event (the year is always 2023), 
                                          'event_type': type of event}''',
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "getTrainDistruptions",
        "description": "returns a json containing the latest distruptions for a given train line or train station, described as: 'station/line': 'distruption details'.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    # {
    #     "name": "directions",
    #     "description": '''get step by step directions via public transport from a starting point to an ending point, leaving at a certain time. here is an example of what this might return: [
    #                     {
    #                         "legs": [
    #                         {
    #                             "steps": [
    #                             {
    #                                 "html_instructions": "Head northwest on Main St",
    #                                 "distance": {"text": "0.1 mi", "value": 160},
    #                                 "duration": {"text": "1 min", "value": 60},
    #                                 // Additional information about the step
    #                             },
    #                             // Additional steps...
    #                             ],
    #                             "duration": {"text": "5 mins", "value": 300},
    #                             "distance": {"text": "0.3 mi", "value": 500},
    #                             // Additional information about the leg
    #                         }
    #                         ],
    #                         "overview_polyline": {"points": "a~l~Fjk~uOnzh..."},
    #                         "summary": "Main St",
    #                         "warnings": ["Walking directions are in beta. Use caution – This route may be missing sidewalks or pedestrian paths."],
    #                         "waypoint_order": []
    #                     }
    #                 ]''',
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             'start': {
    #                 'type': 'string'
    #             },
    #             'end': {
    #                 'type': 'string'
    #             },
    #             'leave_time': {
    #                 'type': 'string'
    #             }
    #         }
    #     }
    # }
]

# return lat, long pair
def getStartingLocation():
    response = json.loads(requests.get("https://ipapi.co/json/"))
    
    return response['latitude'], response['longitude']

def getCurrentWeather():
    latitude, longitude = getStartingLocation()
    return requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={float(latitude)}&longitude={float(longitude)}&current=apparent_temperature&hourly=apparent_temperature&hourly=precipitation_probabiliy&daily=uv_index_max").json()

def getEvents():
    # hard coded, in prod we should request these deets at the start of the day
    return {'Christmas Treasure Hunt': {'summary': 'Go on a Christmas adventure in Carlton Gardens.', 'event_date': '10 Dec', 'event_type': '\nFree\nFamily and kids\n'}, "New Year's Eve Twilight Dinner Package": {'summary': "Enjoy a dining and drinks package in Melbourne's 160-year-old historic cellar.", 'event_date': '31 Dec', 'event_type': '\nEvents\nFood and wine\n'}, 'Docklands Christmas Maze': {'summary': 'Find your holiday cheer at the giant Christmas maze, with amazing prizes to be won.', 'event_date': '29 Nov', 'event_type': '\nFree\nFamily and kids\n'}, 'Titanic: The Artefact Exhibition': {'summary': 'Explore human stories of the Titanic told through 200+ artefacts recovered from the legendary ship.', 'event_date': '16 Dec', 'event_type': '\nExhibition\nHistory\n'}, 'Eric Prydz: Holo': {'summary': 'Swedish producer Prydz brings his jaw-dropping Holo live show to Melbourne.', 'event_date': '8', 'event_type': '\nMusic\nEntertainment\n'}, 'NGV Architecture Commission: (This is) Air': {'summary': 'The NGV 2023 Architecture Commission is a large-scale installation that makes the invisible visible.', 'event_date': '23 Nov', 'event_type': '\nFree\nArt\n'}, 'Christmas Square': {'summary': 'Discover a Christmas wonderland featuring the city’s giant tree.', 'event_date': '24 Nov', 'event_type': '\nFree\nFamily and kids\n'}, 'Cirque du Soleil: Luzia': {'summary': 'Go on a vibrant journey through worlds filled with wonders and artistry with Cirque du Soleil.', 'event_date': '24 Mar', 'event_type': '\nTheatre\nDance\n'}}
    # return webscraper.melb_events()

#def directions(start, end, leave_time):
    #return
    # return googlemaps.Client(key=st.secrets['gmaps_key']).directions(start, end, mode='transit', departure_time=leave_time)

def getTrainDistruptions():
    # default is train trips
    return {'contained in details': ['Trains are resuming between Parliament and Heidelberg with delays up to 30 minutes after an earlier power fault', 'Trains are resuming between Parliament and Heidelberg with delays up to 30 minutes after an earlier power fault', 'One escalator on Platform 6/7 at Flinders Street Station will be closed from 11pm Sunday 12 November to 12pm Wednesday 29 November 2023, due to station works. To access Platform 6/7, please use the adjacent stairs or lift located opposite Platform 2/3. For your safety, please observe any signage and instructions in place during this time.'], 'Parkdale Station': ' Station closure from 11.30pm Saturday 21 October 2023 to mid-2024', 'Sunbury Line': ' Buses replace trains from 11.30pm Thursday 23 November to last service Sunday 26 November 2023', 'Cranbourne and Pakenham lines': ' Buses replacing trains from first service Friday 24 November to last service Sunday 26 November 2023', 'Pakenham Line': ' Buses replace trains between Dandenong and Pakenham from 9.30pm Friday 24 November to 9.30pm Sunday 26 November 2023', 'Belgrave and Lilydale lines': ' Buses replace trains on select sections from late January 2024', 'Frankston Line stations': ' Temporary car park closures, platform closures, and changes to pedestrian access until mid-2024', 'Cranbourne and Pakenham line stations': ' Temporary car park closures and changes to pedestrian access until 2024', 'Hurstbridge Line stations': ' Temporary car park closures and pedestrian access changes from January 2021 until further notice', 'Belgrave Station': ' Temporary car park closures from 4am Wednesday 23 March 2022 to Sunday 31 December 2023', 'Flinders Street Station': ' Temporary pedestrian access changes from Saturday 30 April 2022 to 2024', 'Albion and Sunshine stations': ' Temporary car park closures at select times from January 15 2023 to early February 2025', 'Croydon Station': ' Temporary pedestrian access changes from Thursday 9 November to late November 2023', 'Ringwood East Station': ' Permanent pedestrian access changes from Wednesday 18 October 2023', 'Keon Park Station': ' Temporary car park closures from Monday 5 June 2023 to 2025', 'Sunbury Station': ' Temporary car park closures from 20 June 2023 until late 2024', 'Bayswater Station': ' Temporary pedestrian access changes from Tuesday 24 October to March 2024', 'Craigieburn Station': ' Temporary car space closures from mid-August 2023 until further notice', 'Parliament Station': ' Temporary pedestrian access changes from June 2022 to late 2023', 'Merinda Park Station': ' Temporary car park closures from late-September 2023 to mid-January 2024', 'Boronia Station': ' Temporary car space closures from Monday 13 November to Friday 24 November 2023', 'Pakenham Station': ' Station closure from 10pm Friday 24 November to 3am Monday 11 December 2023', 'Merlynston Station': ' Car Park opening from Friday 17 November 2023', 'Union Station': ' Car park and bus stop openings from late 2023'}    
    # return webscraper.ptv_disruptions(trip_type)

# placeholder feature
# def getServiceInfo():
#     return "The Public Transport Victoria (PTV) system is a comprehensive network of train, tram, and bus services operating in Victoria, Australia, especially in Melbourne. Trains, the backbone of Melbourne's public transport, connect suburbs to the city center. The city's iconic trams provide convenient inner-city travel, while buses cover areas less accessible by rail. Ticketing is managed via the myki card, a rechargeable smart card used across all modes of transport. Fares depend on travel zones and times, with options for daily caps and concessions. The system is accessible, featuring low-floor trams, tactile indicators, and equipped stations and stops. Operational hours for trains and trams extend to around midnight, with all-night services on weekends under the Night Network. Buses run on various schedules, often with reduced weekend services. PTV offers real-time information through displays, a journey planner, and a mobile app, aiding in travel planning and service updates. Safety is ensured through patrols, rules like myki validation, and CCTV surveillance. PTV emphasizes environmental sustainability by reducing emissions and promoting public transport to lessen road congestion. Continuous improvements and expansions are made to accommodate Melbourne's growing population, including infrastructure upgrades and new services. As a crucial part of Melbourne's urban dynamics, PTV is essential for commuters, students, tourists, and the public, known for its efficiency and coverage."

OPTIONS = {'getStartingLocation': getStartingLocation, 
           'getCurrentWeather': getCurrentWeather, 
           'getTrainDistruptions': getTrainDistruptions,
           'getEvents': getEvents}
           #'directions': directions} 
