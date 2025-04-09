import tkinter as tk
from tkinter import ttk
from main_menu import MainMenuFrame
import pygame as pg


class PhantomDinerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Phantom Diner")
        self.geometry("800x600")
        self.minsize(800, 600)

        # Create container frame
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Show main menu
        self.show_frame(MainMenuFrame)

    def show_frame(self, frame_class):
        """Show a frame for the given class"""
        # Destroy current frame if exists
        for widget in self.container.winfo_children():
            widget.destroy()

        # Create and show new frame
        frame = frame_class(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


if __name__ == "__main__":
    app = PhantomDinerApp()
    app.mainloop()