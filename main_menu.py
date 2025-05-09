import tkinter as tk
from tkinter import ttk
from main_nameinput import NameInputDialog
from main_manual import ManualWindow
from main_stat import StatisticsFrame
from PIL import Image, ImageTk

class MainMenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load background image
        self.original_image = Image.open("images/cover.png")
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Background label
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Button frame
        self.button_frame = ttk.Frame(self, style="Transparent.TFrame")
        self.button_frame.place(relx=0.5, rely=0.9, anchor="center")

        self.create_styles()
        self.create_widgets()
        self.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        new_width, new_height = event.width, event.height
        resized = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_image)

    def create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Style for PLAY GAME button
        style.configure("Play.TButton",
                        font=("David", 18, "bold"),
                        foreground="#13056B",
                        background="#FC5658",
                        padding=10,
                        borderwidth=0)
        style.map("Play.TButton",
                  background=[("active", "#3eb96a")],
                  foreground=[("active", "#13056B")])

        # Style for STATISTICS button
        style.configure("Stats.TButton",
                        font=("David", 18, "bold"),
                        foreground="#13056B",
                        background="#FFBD59",
                        padding=10,
                        borderwidth=0)
        style.map("Stats.TButton",
                  background=[("active", "#3eb96a")],
                  foreground=[("active", "#13056B")])

        # Style for QUIT button
        style.configure("Quit.TButton",
                        font=("David", 18, "bold"),
                        foreground="#13056B",
                        background="#37B1BC",
                        padding=10,
                        borderwidth=0)
        style.map("Quit.TButton",
                  background=[("active", "#3eb96a")],
                  foreground=[("active", "#13056B")])

        # Style for MANUAL button
        style.configure("Manual.TButton",
                        font=("David", 18, "bold"),
                        foreground="#13056B",
                        background="#FFA8B0",
                        padding=10,
                        borderwidth=0)
        style.map("Manual.TButton",
                  background=[("active", "#3eb96a")],
                  foreground=[("active", "#13056B")])

    def create_widgets(self):
        self.btn_game = ttk.Button(self.button_frame, text="PLAY GAME",
                                   command=self.start_game, style="Play.TButton")
        self.btn_stat = ttk.Button(self.button_frame, text="STATISTICS",
                                   command=self.show_statistics, style="Stats.TButton")
        self.btn_quit = ttk.Button(self.button_frame, text="QUIT",
                                   command=self.controller.destroy, style="Quit.TButton")
        self.btn_manual = ttk.Button(self.button_frame, text="MANUAL",
                                   command=self.show_manual, style="Manual.TButton")

        self.btn_game.grid(row=0, column=0, padx=10, pady=5)
        self.btn_stat.grid(row=0, column=1, padx=10, pady=5)
        self.btn_manual.grid(row=0, column=2, padx=10, pady=5)
        self.btn_quit.grid(row=0, column=3, padx=10, pady=5)

    def start_game(self):
        NameInputDialog(self.controller)

    def show_statistics(self):
        StatisticsFrame(self.controller)

    def show_manual(self):
        ManualWindow(self.controller)