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

        temp_df = self.__statistics_df.copy()
        temp_df['New Dishes'] = self.__statistics_df.groupby('Player')['Dishes Served'].diff().fillna(self.__statistics_df['Dishes Served'])

        units = {
            "Score": "points",
            "Waiting Time": "seconds",
            "Haunt Events": "events",
            "Dish served": "dishes",
        }

        features = {
            'Score': self.__statistics_df['Score'],
            'Waiting Time': self.__statistics_df['Waiting Time'],
            'Haunt Events': self.__statistics_df['Haunt Events'],
            'Dishes Served': temp_df['New Dishes']
        }

        stats = []
        for name, values in features.items():

            stats.append([
                name,
                min(values) if min(values) > 0 else abs(min(values)),
                max(values),
                round(values.median(), 2),
                round(values.mean(), 2),
                round(values.std(), 2) if len(values) > 1 else 0
            ])
        return stats, units
