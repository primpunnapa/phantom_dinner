import tkinter as tk
from tkinter import ttk
from main_table import StatisticsManager
from main_graph import GraphGenerator

class StatisticsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.stats_manager = StatisticsManager()
        self.graph_generator = GraphGenerator(self.stats_manager)

        # Back button
        back_button = ttk.Button(self, text="Back",  command=lambda: self.controller.show_frame("MainMenuFrame"))
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.create_player_stats_tab()
        self.create_numerical_stats_tab()
        self.create_graphs_tab()

    def create_player_stats_tab(self):
        """Tab with player statistics"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Player Stats")

        # Highest Score
        highest_score = self.stats_manager.get_highest_score()
        if highest_score is not None:
            frame1 = ttk.LabelFrame(tab, text="Highest Score")
            frame1.pack(fill=tk.X, padx=10, pady=5)

            tree1 = ttk.Treeview(frame1, columns=("Name", "Score"), show="headings", height=2)
            tree1.heading("Name", text="Name")
            tree1.heading("Score", text="Score")
            tree1.pack(fill=tk.X)

            tree1.insert("", "end", values=(highest_score['Player'], highest_score['Score']))

        # Highest Level
        highest_level = self.stats_manager.get_highest_level()
        if highest_level is not None:
            frame2 = ttk.LabelFrame(tab, text="Highest Level")
            frame2.pack(fill=tk.X, padx=10, pady=5)

            tree2 = ttk.Treeview(frame2, columns=("Name", "Level"), show="headings", height=2)
            tree2.heading("Name", text="Name")
            tree2.heading("Level", text="Level")
            tree2.pack(fill=tk.X, padx=10, pady=5)

            tree2.insert("", "end", values=(highest_level['Player'], highest_level['Level']))

        # Latest Player
        latest_player = self.stats_manager.get_latest_player()
        if latest_player is not None:
            frame3 = ttk.LabelFrame(tab, text="Latest Player")
            frame3.pack(fill=tk.X, padx=10, pady=5)

            tree3 = ttk.Treeview(frame3, columns=("Name", 'Level', 'Score'), show="headings", height=2)
            tree3.heading("Name", text="Name")
            tree3.heading("Level", text="Level")
            tree3.heading("Score", text="Score")
            tree3.pack(fill=tk.X, padx=10, pady=5)

            tree3.insert("", "end", values=(latest_player['Player'], latest_player['Score'], latest_player['Level']))

    def create_numerical_stats_tab(self):
        """Tab with numerical statistics"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Numerical Stats")

        stats = self.stats_manager.get_numerical_stats()
        if stats is None:
            label = tk.Label(tab, text="No statistics available yet")
            label.pack(pady=50)
            return

        tree = ttk.Treeview(tab, columns=("Feature", "Statistical Value", "Value"), show="headings")
        tree.heading("Feature", text="Feature")
        tree.heading("Statistical Value", text="Statistical Value")
        tree.heading("Value", text="Value")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for feature, values in stats.items():
            for stat_name, stat_value in values.items():
                tree.insert("", "end", values=(feature, stat_name, round(stat_value, 2)))

    def create_graphs_tab(self):
        """Tab with graphs"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Graphs")

        # notebook for graph tabs
        graph_notebook = ttk.Notebook(tab)
        graph_notebook.pack(fill=tk.BOTH, expand=True)
        self.graph_generator.create_score_boxplot(graph_notebook)
        self.graph_generator.create_dishes_graph(graph_notebook)
        self.graph_generator.create_haunt_time(graph_notebook)
        self.graph_generator.create_pie_level(graph_notebook)
