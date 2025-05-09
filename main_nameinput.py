import tkinter as tk
import pygame as pg
from diner_game import Game


class NameInputDialog(tk.Toplevel):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.title("Enter Your Name")
        self.geometry("300x200")

        self.game_running = False
        self.controller_alive = True  # Track if main window exists

        self.transient(controller)
        self.grab_set()

        # Widgets
        tk.Label(self, text="Please enter your name:", font=("David", 15)).pack(pady=10)
        self.name_entry = tk.Entry(self, font=("David", 12), width=25)
        self.name_entry.pack(pady=10)
        self.name_entry.focus_set()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Submit", command=self.submit, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.safe_destroy, width=10).pack(side=tk.LEFT, padx=5)

        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

        # Track controller destruction
        self.controller.bind("<Destroy>", lambda e: self.handle_controller_destroy())

    def handle_controller_destroy(self):
        """Callback when main window is destroyed"""
        self.controller_alive = False

    def safe_destroy(self):
        """Safely destroy this window"""
        try:
            if self.winfo_exists():
                self.destroy()
        except tk.TclError:
            pass

    def submit(self):
        name = self.name_entry.get().strip()
        if name:
            self.game_running = True
            self.withdraw()  # Hide this dialog
            self.launch_game(name)

    def launch_game(self, player_name):
        """Launch the pygame game with proper cleanup"""
        try:
            pg.init()
            screen = pg.display.set_mode((800, 600))
            pg.display.set_caption("Phantom Diner")

            game = Game(player_name, screen)
            game_completed = game.running()  # This blocks until game ends

            if not game_completed and self.controller_alive:
                # Game was force-closed, but main window still exists
                self.controller.destroy()

        except Exception as e:
            print(f"Game error: {e}")

        finally:
            self.game_running = False
            pg.quit()

            # Only try to show main window if it still exists
            if self.controller_alive:
                try:
                    self.controller.deiconify()
                except tk.TclError:
                    pass  # Main window was already destroyed

            self.safe_destroy()  # Close this dialog