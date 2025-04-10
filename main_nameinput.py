import tkinter as tk
from tkinter import ttk
import pygame as pg
from diner_game import Game


class NameInputDialog(tk.Toplevel):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.title("Enter Your Name")
        self.geometry("300x200")

        self.transient(controller)  # Keeps the dialog on top of the parent window.
        self.grab_set()  # block interaction outside

        # Widgets
        tk.Label(self, text="Please enter your name:", font=("David", 15)).pack(pady=10)

        self.name_entry = tk.Entry(self, font=("David", 12), width=25)
        self.name_entry.pack(pady=10)
        self.name_entry.focus_set()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Submit", command=self.submit, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.destroy, width=10).pack(side=tk.LEFT, padx=5)

        # self.protocol("WM_DELETE_WINDOW", self.destroy)

    def submit(self):
        name = self.name_entry.get().strip()
        if name:
            self.controller.withdraw()  # Hide tkinter window
            self.launch_game(name)
            self.destroy()

    def launch_game(self, player_name):
        """Launch the pygame game"""
        try:
            pg.init()
            screen = pg.display.set_mode((800, 600))
            pg.display.set_caption("Phantom Diner")

            game = Game(player_name, screen)
            game.running()
        finally:
            pg.quit()
            self.controller.deiconify()  # Show tkinter window again