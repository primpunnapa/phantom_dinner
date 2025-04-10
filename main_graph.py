import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import tkinter as tk
import tkinter.ttk as ttk

class GraphGenerator:
    def __init__(self, stats_manager):
        self.stats_manager = stats_manager
        self.stats_data = self.stats_manager.get_statistics_df()

    def create_score_boxplot(self, notebook):
        """create boxplot of score distribution by level"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Score Distribution")

        # Keep levels that represent at least 2% of the data
        min_percentage = 0.02
        level_percentages = self.stats_data['Level'].value_counts(normalize=True)
        valid_levels = level_percentages[level_percentages >= min_percentage].index
        # print(valid_levels)
        filtered_data = self.stats_data[self.stats_data['Level'].isin(valid_levels)]
        if not filtered_data.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.boxplot(x='Level', y='Score', data=filtered_data)
            plt.title(f"Score Distribution (Levels with ≥ 2% of data)")

            canvas = FigureCanvasTkAgg(fig, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_dishes_graph(self, notebook):
        """Create bar graph of average dishes served by level"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Dishes Served")

        # Keep levels that represent at least 1% of the data
        min_percentage = 0.01
        level_percentages = self.stats_data['Level'].value_counts(normalize=True)
        valid_levels = level_percentages[level_percentages >= min_percentage].index
        filtered_data = self.stats_data[self.stats_data['Level'].isin(valid_levels)]

        if not filtered_data.empty:
            avg_dishes = filtered_data.groupby('Level')['Dishes Served'].mean().reset_index()
            # print(avg_dishes.index)

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(avg_dishes['Level'], avg_dishes['Dishes Served'])
            ax.set_title("Average Dishes Served by Level")
            ax.set_xticks(avg_dishes['Level'])
            ax.set_xlabel("Level")
            ax.set_ylabel("Average Dishes Served")

            canvas = FigureCanvasTkAgg(fig, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_haunt_time(self, notebook):
        """Create scatter plot between haunt level and waiting time"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Haunt Events")

        fig, ax = plt.subplots(figsize=(8, 4))

        haunt_data = self.stats_data[self.stats_data['Haunt Events'] > 0]
        ax.scatter(haunt_data['Waiting Time'], haunt_data['Haunt Events'], c='red')
        ax.set_title("Haunt Events vs Wait Time")
        ax.set_xlabel("Wait time (seconds)")
        ax.set_ylabel("Haunt events")

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_pie_level(self, notebook):
        """Create level Progression Pie Chart"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Level Progression")

        fig, ax = plt.subplots(figsize=(8, 8))

        max_levels = self.stats_data.groupby('Player')['Level'].max()
        level_counts = max_levels.value_counts()
        # print(level_counts)
        total = level_counts.sum()
        percentages = (level_counts / total) * 100

        # Threshold for small slices
        threshold = 2
        main_levels = level_counts[percentages >= threshold]
        other_levels = level_counts[percentages < threshold]
        if not other_levels.empty:
            main_levels['Other levels'] = other_levels.sum()

        ax.pie(main_levels, labels=main_levels.index, autopct='%1.0f%%', startangle=90)
        ax.set_title("Highest Level Reached by Players")

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)