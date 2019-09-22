import requests
import json
from pymongo import MongoClient

# load secret key ----
with open("/Users/cnuno/.secret/dark_sky_api.json", "r") as f:
    key = json.load(f)["key"]

# store exclusions ----
exclusions = "?exclude=currently,minutely,hourly,alerts,flags"

# instantiate MongoDB client ----
client = MongoClient()
db = client["soccer"]
weather = db["weather"]

# Powered by Dark Sky <https://darksky.net/poweredby/>
class WeatherGetter():
    """This class gets the weather for Berlin, using Dark Sky's API"""
    def __init__(self):
        self.lat = "52.520008"
        self.long = "13.404954"
        self.base_url = "https://api.darksky.net/forecast/"
    
    def get_weather(self, date, verbose=True):
        """Gets the daily weather for Berlin for a particular date."""
        # store request url
        url = f"{self.base_url}{key}/{self.lat},{self.long},{date}{exclusions}"
        
        # call the api ----
        response = requests.get(url)

        # check to make sure call is valid ----
        if response.status_code == 200:
            if verbose:
                print(response.status_code)
        else: 
            raise ValueError(f"Error getting data from DarkSky API: Response Code {response.status_code}")
        
        # store API results as dictionary object
        # note: to guarantee we retain the supplied date information,
        #       it is being inserted as a key-value pair 
        output = response.json()
        output["date"] = date
        
        # insert data into weather table inside the soccer mongodb
        weather.insert_one(output)

        return None
        
