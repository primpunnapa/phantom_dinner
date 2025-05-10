import tkinter as tk
from main_nameinput import NameInputDialog
from PIL import Image, ImageTk


class ManualWindow(tk.Toplevel):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.title("Game Manual")
        self.geometry("800x600")
        self.images = ["images/manual/manual1.1.png", "images/manual/manual2.1.png", "images/manual/manual3.1.png", "images/manual/manual4.1.png"]
        self.index = 0

        # Load and show the first image
        self.image_label = tk.Label(self)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.transient(controller)  # Keeps the dialog on top of the parent window.
        self.grab_set()             # block interaction outside

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.back_btn = tk.Button(btn_frame, text="Back", command=self.show_previous)
        self.next_btn = tk.Button(btn_frame, text="Next", command=self.show_next)
        self.play_btn = tk.Button(btn_frame, text="Play", command=self.start_game)

        self.back_btn.pack(side=tk.LEFT, padx=10)
        self.next_btn.pack(side=tk.RIGHT, padx=10)
        self.play_btn.pack(side=tk.RIGHT, padx=10)

        self.update_image()
        self.bind("<Configure>", lambda e: self.update_image())

    def update_image(self):
        width = self.winfo_width()
        height = self.winfo_height() - 50

        if width < 1 or height < 1:
            return

        img = Image.open(self.images[self.index])
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_img)

    def show_next(self):
        if self.index < len(self.images) - 1:
            self.index += 1
            self.update_image()

    def show_previous(self):
        if self.index > 0:
            self.index -= 1
            self.update_image()

    def start_game(self):
        NameInputDialog(self.controller)