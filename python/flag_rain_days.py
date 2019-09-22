"""
Access the 'weather' collection from the 'soccer' Mongodb
and identify the rainy days during the 2011 matches
"""

# load necessary modules ----
from pymongo import MongoClient
import pandas as pd
from sqlalchemy import create_engine

# connect to mongodb ----
client = MongoClient()
db = client["soccer"]
weather = db["weather"]

# convert collection into data frame ----
df = pd.DataFrame(list(weather.find()))

# create an empty list
weather_info = []

for record in range(len(df)):
    # extract pieces of information from each record
    epoch_date = df["date"][record]
    weather = df["daily"][record]["data"][0]["icon"]
    # add them to the list
    weather_info.append({"epoch_date": epoch_date, "weather": weather})

# convert the list to a data frame
weather_df = pd.DataFrame(weather_info)

# print(weather_df["weather"].value_counts())

# after identifying there are only 3 types of 'weather' values
# let's create a rain flag
weather_df["rain"] = weather_df["weather"] == "rain"

# export weather_df as a psql table ----
engine = create_engine("postgresql:///soccer")
weather_df.to_sql(name="unique_2011_weather", con=engine, index=False)
