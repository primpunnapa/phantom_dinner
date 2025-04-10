import pandas as pd
import os
import csv


class StatisticsManager:
    def __init__(self):
        self.__statistics_file = "game_statistics.csv"
        self.__statistics_df = self.load_statistics()

    def get_statistics_df(self):
        return self.__statistics_df

    def load_statistics(self):
        """Load game statistics from CSV file"""
        columns = ["Player", "Score", "Waiting Time", "Haunt Events", "Level", "Dishes Served"]
        if os.path.exists(self.__statistics_file):
            try:
                return pd.read_csv(self.__statistics_file)
            except:
                return pd.DataFrame(columns=columns)
        return pd.DataFrame(columns=columns)

    def get_latest_player(self):
        """Get lastest player"""
        if not self.__statistics_df.empty:
            latest = self.__statistics_df.iloc[-1]
            return {
                'Player': latest['Player'],
                'Score': latest['Score'],
                'Level': latest['Level']
            }
        return None
    def get_highest_score(self):
        """Get player with highest score"""
        if not self.__statistics_df.empty:
            return self.__statistics_df.loc[self.__statistics_df['Score'].idxmax()]
        return None

    def get_highest_level(self):
        """Get player with highest level"""
        if not self.__statistics_df.empty:
            return self.__statistics_df.loc[self.__statistics_df['Level'].idxmax()]
        return None

    def get_numerical_stats(self):
        """Calculate numerical statistics"""
        if self.__statistics_df.empty:
            return None

        return {
            "Score": {
                "Mean": self.__statistics_df['Score'].mean(),
                "Median": self.__statistics_df['Score'].median(),
                "Std Dev": self.__statistics_df['Score'].std(),
                "Min": self.__statistics_df['Score'].min(),
                "Max": self.__statistics_df['Score'].max()
            },
            "Waiting Time": {
                "Average": self.__statistics_df['Waiting Time'].mean(),
                "Max": self.__statistics_df['Waiting Time'].max()
            },
            "Haunt Events": {
                "Total": self.__statistics_df['Haunt Events'].sum(),
                "Mean per level": self.__statistics_df['Haunt Events'].mean()
            },
            "Dishes Served": {
                "Average per level": self.__statistics_df['Dishes Served'].mean()
            }
        }
