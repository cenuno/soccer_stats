# load necessary modules ----
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

# create the WeatherGetter class ----
class WeatherGetter():
    """Retrieve daily weather for Berlin, Germany 
    
    Note: Stores the data from the Dark Sky API in a collection called weather
          within the soccer MongoDB

    Attributes:
        lat (str): latitudinal coordinate of Berlin, Germany
        long (str): longitudinal coordinate of Berlin, Germany
        base_url (str): url to the historical weather data API

    Methods:
        get_weather(): retrieves Berlin's historical weather data 
                       for one particular date and stores the data
                       within the weather collection in the soccer MongoDB
    """
    def __init__(self):
        self.lat = "52.520008"
        self.long = "13.404954"
        self.base_url = "https://api.darksky.net/forecast/"
    
    def get_weather(self, date: str, verbose: bool = True) -> None:
        """Retrieve the daily weather for Berlin for one particular date
        
        Args:
            date (str): 10-digit epoch date
            verbose (bool): True/False to print out the integer code of
                            responded HTTP Status

        Returns:
            None (but the data is stored within the weather collection in
                  the soccer MongoDB)
        """
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
        
        # insert data into weather collection inside the soccer MongoDB
        weather.insert_one(output)

        return None
        
