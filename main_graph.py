import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import tkinter as tk
import tkinter.ttk as ttk

class GraphGenerator:
    def __init__(self, stats_manager):
        self.stats_manager = stats_manager
        self.stats_data = self.stats_manager.get_statistics_df()
        self.figures = []  # Track all created figures

    @staticmethod
    def remove_outlier(df, feature):
        """Remove outlier by iqr and return new dataset"""
        q1 = df[feature].quantile(0.25)
        q3 = df[feature].quantile(0.75)
        iqr = q3 - q1
        temp_df = df[~((df[feature] < q1 - 1.5 * iqr) | (df[feature] > q3 + 1.5 * iqr))]
        return temp_df.copy()

    def create_score_boxplot(self, notebook):
        """create boxplot of score distribution by level"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Score Distribution per Level")

        new_df = self.remove_outlier(self.stats_data, "Level")
        filter_df = self.remove_outlier(new_df, "Score")
        fig, ax = plt.subplots(figsize=(8, 4))
        self.figures.append(fig)

        sns.boxplot(x='Level', y='Score', data=filter_df, fliersize=0)
        plt.title(f"Score Distribution")

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_dishes_graph(self, notebook):
        """Create bar graph of average dishes served by level"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Dishes Served")

        filter_df = self.remove_outlier(self.stats_data, "Level").copy()
        filter_df['New Dishes'] = (
            filter_df.groupby('Player')['Dishes Served'].diff().fillna(filter_df['Dishes Served'])
        )

        avg_dishes = filter_df.groupby('Level')['New Dishes'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(8, 4))
        self.figures.append(fig)

        ax.bar(avg_dishes['Level'], avg_dishes['New Dishes'], color='#9a5ea1')
        ax.set_title("Average Dishes Served by Level")
        ax.set_xticks(avg_dishes['Level'])
        ax.set_xlabel("Level")
        ax.set_ylabel("Average Dishes Served")
        ax.grid(linestyle=':')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_haunt_time(self, notebook):
        """Create scatter plot between haunt level and waiting time"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Haunt Events")

        fig, ax = plt.subplots(figsize=(8, 4))
        self.figures.append(fig)

        haunt_data = self.stats_data[self.stats_data['Haunt Events'] > 0]
        ax.scatter(haunt_data['Waiting Time'], haunt_data['Haunt Events'], c='red')
        ax.set_title("Relationships between Haunt Events and Wait Time")
        ax.set_xlabel("Wait time (seconds)")
        ax.set_ylabel("Haunt events")

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_pie_level(self, notebook):
        """Create level Progression Pie Chart"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Level Progression")

        fig, ax = plt.subplots()
        self.figures.append(fig)
        max_levels = self.stats_data.groupby('Player')['Level'].max()
        level_counts = max_levels.value_counts()
        total = level_counts.sum()
        percentages = (level_counts / total) * 100

        # Threshold for small slices
        threshold = 2
        main_levels = level_counts[percentages >= threshold]
        other_levels = level_counts[percentages < threshold]
        if not other_levels.empty:
            main_levels['Other levels'] = other_levels.sum()

        slices, texts, numbers = ax.pie(main_levels, autopct='%1.0f%%', startangle=90, counterclock=False)
        ax.set_title("Highest Level Reached by Players")
        ax.legend(slices,main_levels.index, title="Levels",bbox_to_anchor=(1, 1))

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def close_figures(self):
        """Close all matplotlib figures to prevent memory leaks"""
        for fig in self.figures:
            plt.close(fig)
        self.figures = []