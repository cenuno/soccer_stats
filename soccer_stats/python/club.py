# load necessary modules -----
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sqlalchemy import create_engine

# create sql connection
# note: if the sql connection contained personal information
#       it would be stored as a .json file in the ~/.secrets/ dir
engine = create_engine("postgresql:///soccer")

# create sql queries 
all_rain_win_pct_query = "SELECT * FROM club_rain_win_pct_2011"
all_stats_query = "SELECT * FROM club_stats_2011"

# create Club class -----
class Club(object):
    """Statistics for the 2011 season for one soccer club

    Note: only contains data on teams in the English Premier League
          and D1 and D2 for the Bundesliga
    
    Attributes:
        name (str): the name of the club
        rain_win_pct_df (DataFrame): club specific season stats of rain games
        all_rain_win_pct_df (DataFrame): all clubs season stats of rain games
        stats_df (DataFrame): club specific season stats (regardless of rain)
        all_stats_df (DataFrame): all clubs season stats (regardless of rain)

    Methods:
        plot_rain_stats(): visualize season statiistics of rain games
        plot_stats(): visualize season statistics (regardless of rain)
    """


    def __init__(self, name: str):
        self.name = name
        self.rain_win_pct_df = self._filter(rain=True)
        self.stats_df = self._filter(rain=False)


    # load necessary data ----
    all_rain_win_pct_df = pd.read_sql_query(all_rain_win_pct_query,
                                            engine)
    
    all_stats_df = pd.read_sql_query(all_stats_query, engine)

    def _filter(self, rain: bool = False) -> pd.DataFrame:
        """Create club specific data frames
        
        Crafts unique queries based on the self.name value to ensure
        that data returned is specific to one club.

        Args:
            rain: True/False whether or not to query statistics where 
                  games were played in the rain.

        Returns:
            A data frame with one record containing 2011 season statistics
        """
        # create club specific queries ----
        club_rain_query = f"{all_rain_win_pct_query} WHERE club = '{self.name}'"
        club_stats_query = f"{all_stats_query} WHERE club = '{self.name}'"

        # load club specific data ----
        club_stats_df = pd.read_sql_query(club_stats_query, engine)
        club_rain_win_pct_df = pd.read_sql_query(club_rain_query, engine)

        if rain:
            return club_rain_win_pct_df
        else:
            return club_stats_df

    def plot_stats(self, export: bool = False) -> None:
        """Visualizes club wins, draws, and losses for the 2011 season
        
        Args:
            export: True/False whether to export the visual as .png file

        Returns:
            None (but a barplot is shown)
        """
        # store axis labels ----
        num_cols = ["wins", "ties", "losses"]

        # store total # of games played ----
        total_games = self.stats_df["total_games"].values[0]

        # store the number of wins, ties, and losses ----
        stats = np.zeros(len(num_cols))

        for index, value in enumerate(num_cols):
            stats[index] = self.stats_df[value].values[0]

        # create barplot to visualize the season statistics ----
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(x=[col.title() for col in num_cols], 
                    height=stats,
                    color=["green", "gray", "red"])
        # place stat values above each bar 
        for index, stat in enumerate(stats):
            ax.text(x=index, 
                    y=stat + 0.15, 
                    s=str(int(stat)), 
                    color="black", 
                    fontweight='bold')
        ax.set_ylabel("Number of games")
        ax.set_title(f"{self.name} 2011 Wins, Ties, and Losses ({total_games} total games)")
        fig.tight_layout()

        if export:
            fig.savefig(f"visuals/{str(self.name).replace(' ', '_')}_2011_season_stats.png",
                        dpi=175,
                        bbox_inches="tight")
            print(f"{self.name} season statistics bar chart exported to visuals/ dir")

        return plt.show()


    def plot_rain_win_pct(self, color: str = None, export: bool = False, ) -> None:
        """Visualizes rain win % against all other teams in their league for the 2011 season
        
        Args:
            color (str): the color used to highlight the club's rain win %
            export (bool): True/False whether to export the visual as .png file

        Returns:
            None (but a histogram is shown)
        """
        # set default color ----
        if color is None:
            color = "orange"

        # store club rain win % ----
        club_rain_win_pct = self.rain_win_pct_df["rain_win_pct"][0]

        # store club league ----
        club_league = self.rain_win_pct_df["div"].values[0]

        # store league labels ----
        league_label = {"D1": "Bundesliga", 
                       "D2": "Bundesliga 2", 
                       "E0": "English Premier League"}

        club_league_label = league_label[club_league]

        # filter data to clubs in the same league as those in Club
        condition = self.all_rain_win_pct_df["div"].isin(self.rain_win_pct_df["div"])
        league_rain_win_pct = self.all_rain_win_pct_df.loc[condition, "rain_win_pct"]

        # create histogram to visualize rain win % comparison ----
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(x=league_rain_win_pct, 
                label=f"{club_league_label}: {league_rain_win_pct.mean().round(3) * 100}% (avg)")
        ax.axvline(linewidth=6,
                   color=color,
                   x=club_rain_win_pct,
                   label=f"{self.name}: {club_rain_win_pct.round(3) * 100}%") 
        ax.set_xlabel("Rain win percentage")
        ax.set_ylabel(f"Number of teams in {club_league_label} (n = {len(league_rain_win_pct)})")
        ax.legend()
        ax.set_title(f"Comparing {self.name}'s rain win percentage against all other teams in the {club_league_label}, 2011")
        fig.tight_layout()

        if export:
            fig.savefig(f"visuals/{str(self.name).replace(' ', '_')}_2011_rain_win_pct.png",
                        dpi=175,
                        bbox_inches="tight")
            print(f"{self.name} rain win percentage histogram exported to visuals/ dir")

        return plt.show()


