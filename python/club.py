# load necessary modules -----
import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import create_engine

# create sql connection -----
engine = create_engine("postgresql:///soccer")

# create sql queries -----
all_rain_win_pct_query = "SELECT * FROM club_rain_win_pct_2011"
all_stats_query = "SELECT * FROM club_stats_2011"

# create Club class -----
class Club(object):
    """Shows club statistics in 2011"""

    def __init__(self, name: str):
        # each Club object must have a name to reference a club
        self.name = name
        self.rain_win_pct_df = self._filter(name=self.name, rain=True)
        self.stats_df = self._filter(name=self.name, rain=False)

    # load necessary data ----
    all_rain_win_pct_df = pd.read_sql_query(all_rain_win_pct_query,
                                              engine)
    
    all_stats_df = pd.read_sql_query(all_stats_query, engine)

    def _filter(self, name: str, rain: bool = False) -> pd.DataFrame:
        # create club specific queries ----
        _club_rain_query = f"{all_rain_win_pct_query} WHERE club = '{name}'"
        _club_stats = f"{all_stats_query} WHERE club = 'Aachen'"

        # load club specific data ----
        club_stats_df = pd.read_sql_query(_club_stats, engine)
        club_rain_win_pct_df = pd.read_sql_query(_club_rain_query, engine)

        if rain:
            return club_rain_win_pct_df
        else:
            return club_stats_df

