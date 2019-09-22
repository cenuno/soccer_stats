"""
Using the epoch dates from 2011 matches, dump the weather data
into a the 'weather' MongoDB
"""

# load necessary modules
import pandas as pd
from sqlalchemy import create_engine
from weathergetter import WeatherGetter

# connect to psql db
engine = create_engine("postgresql:///soccer")

# load unique 2011 dates
df = pd.read_sql_query(sql="SELECT * FROM unique_2011_dates", 
                       con=engine)

# convert epoch_date to string
df["epoch_date"] = df["epoch_date"].astype(int).astype(str)

# instantiate WeatherGetter object
berlin_weather = WeatherGetter()

print("""
----Starting API calls----

Exporting data into the 'weather' collection in the 'soccer' MongoDB.

""")

# for each date, get the weather data from the DarkSky API
# and dump each record into the 'weather' MongoDB
for date in df["epoch_date"]:
    berlin_weather.get_weather(date=date, verbose=True)

print("""
----Finished API calls----

Data exported into the 'weather' collection in the 'soccer' MongoDB.

""")