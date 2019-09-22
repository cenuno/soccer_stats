"""
Methods used to calculate the win rate attribute in the Team() class
"""

import pandas as pd
from typing import Dict, List

def _long_games(self) -> pd.DataFrame:
    """Returns the reshaped games data frame from wide to long"""
    # transform from wide to long (i.e. one row per team (either home or away))
    games_long = pd.melt(self.games,
                         id_vars=["Date", "FTR", "rainy"],
                         value_vars=["HomeTeam", "AwayTeam"])
    
    # rename columns
    games_long.rename(columns={"variable": "home_away",
                                  "value": "team"},
                             inplace=True)
    
    # create new column that makes home_away a boolean
    games_long["home"] = games_long["home_away"] == "HomeTeam"
    
    # sort values by Date
    games_long.sort_values(by=["Date"], inplace=True)
    
    # reset index
    games_long.reset_index(drop=True, inplace=True)
    
    return games_long


def _subset_games(long_df: pd.DataFrame, 
                  team_name: str, 
                  rainy: bool,
                  interest: str) -> List[int]:
    """Returns the indices of a long data frame where the conditions are true
    
    Params:
    
    + long_df: a long DF
    + team_name: the name of a particular team
    + rainy: a True/False value that subsets the data based on games played in the rain
    + interest: the user may select the games where the team "wins", "losses", "draws", or "all"
    """
    
    # store conditions
    team_condition = long_df["team"] == team_name
    rain_condition = long_df["rainy"]
    
    # if someone is interested in dry games, switch the bool
    # i.e. True if no rain (originally, False is no rain)
    if rainy == False:
        rain_condition = ~rain_condition
    
    home = {
        "wins": (long_df["FTR"] == "H") & (long_df["home"]),
        "losses": (long_df["FTR"] == "A") & (long_df["home"]),
        "draws": (long_df["FTR"] == "D") & (long_df["home"])
    }
    
    away = {
        "wins": (long_df["FTR"] == "A") & (long_df["home"] == False),
        "losses": (long_df["FTR"] == "H") & (long_df["home"] == False),
        "draws": (long_df["FTR"] == "D") & (long_df["home"] == False)
    }
    
    # create empty list
    subset_ind = []
    
    # based on interest, subset the data frame
    if interest == "wins":
        indices = long_df.loc[(rain_condition) &
                              (team_condition) &
                              ((home["wins"]) | (away["wins"]))].index
    elif interest == "losses":
        indices = long_df.loc[(rain_condition) &
                              (team_condition) &
                              ((home["losses"]) | (away["losses"]))].index
    elif interest == "draws":
        indices = long_df.loc[(rain_condition) &
                              (team_condition) &
                              ((home["draws"]) | (away["conditions"]))].index
    else:
        indices = long_df.loc[(rain_condition) &
                              (team_condition)].index
        
    # unpack each index value in indices and append it to the empty list
    for index in indices:
        subset_ind.append(index)
    
    # return a filtered version
    return subset_ind #long_df.filter(items=subset_ind, axis=0).reset_index(drop=True)


def _win_rate(self) -> float:
    """Calculates the team's win percentage based on their games by rain and dry games"""
    
    # store number of rain games ----
    n_rain_games = len(self._subset_games(long_df=self._long_games(self.games),
                                     team_name=self.name,
                                     rainy=True,
                                     interest="all"))
    
    # store number of wins in the rain ----
    n_rain_wins = len(self._subset_games(long_df=self._long_games(self.games),
                                    team_name=self.name,
                                    rainy=True,
                                    interest="wins"))
    
    # store number of dry (non-rain) games ----
    n_dry_games = len(self.games) - n_rain
    
    # store number of wins in dry (non-rain) games ----
    n_dry_wins = len(_subset_games(long_df=_long_games(self.games),
                                   team_name=self.name,
                                   rainy=False,
                                   interest="wins"))
    
    # store win percentages by weather 
    win_rate = {
        "dry": round(n_dry_wins / n_dry_games, 3),
        "rain": round(n_rain_wins / n_rain_games, 3)
    }
    
    return win_rate
    
