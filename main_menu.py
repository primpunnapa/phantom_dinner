import tkinter as tk
from tkinter import ttk
from main_nameinput import NameInputDialog
from PIL import Image, ImageTk

class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)  # For image to expand
        self.grid_rowconfigure(1, weight=0)  # For button row (fixed height)
        self.grid_columnconfigure(0, weight=1)

        # Load and display background image
        self.original_image = Image.open("images/wbutton.png")
        # self.bg_image = tk.PhotoImage(file="images/wbutton.png")
        self.bg_label = tk.Label(self)
        self.bg_label.grid(row=0, column=0, sticky="nsew",columnspan=3)
        self.bind("<Configure>", self.resize_image)

        # Create widgets
        self.create_widgets()

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height - self.winfo_children()[1].winfo_height()  # subtract button row height

        # Resize and update the image
        resized = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_image)

    def create_widgets(self):
        # Button style
        btn_style = {
            "font": ("Arial", 14),
            "width": 15,
            "height": 2,
        }

        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=3, sticky="s", pady=(0, 20))

        #Configure button frame columns
        for i in range(3):
            button_frame.grid_columnconfigure(i, weight=1)

        self.btn_game = tk.Button(button_frame, text="Play Game",
                                  command=self.start_game, **btn_style)
        self.btn_stat = tk.Button(button_frame, text="Statistics",
                                  command=self.show_statistics, **btn_style)
        self.btn_quit = tk.Button(button_frame, text="Quit",
                                  command=self.controller.destroy, **btn_style)

        self.btn_game.grid(row=0, column=0, padx=5, pady=5)
        self.btn_stat.grid(row=0, column=1, padx=5, pady=5)
        self.btn_quit.grid(row=0, column=2, padx=5, pady=5)

    def start_game(self):
        """Show name input dialog"""
        NameInputDialog(self.controller)

    def show_statistics(self):
        """Show statistics"""
        pass  # Implement this later