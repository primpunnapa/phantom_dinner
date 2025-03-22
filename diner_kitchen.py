import pygame as pg
import time
from diner_config import Config
from diner_dish import Dish

class Kitchen:
    def __init__(self, pos):
        self.position = pos  # (x, y) coordinates of the kitchen
        self.is_preparing = False  # Whether a dish is being prepared
        self.preparation_time = 3  # Time required to prepare the dish (in seconds)
        self.preparation_start_time = 0  # Time when dish preparation started
        self.current_dish = None  # The dish currently being prepared

    def start_preparation(self):
        """Start preparing the dish."""
        if not self.is_preparing:
            print("Starting preparation...")
            self.is_preparing = True
            self.preparation_start_time = time.time()
            dish_position = (self.position[0] + Config.get("KITCHEN_SIZE") // 4, self.position[1] + Config.get("KITCHEN_SIZE") // 4)
            self.current_dish = Dish("Spider Soup", self.preparation_time, dish_position)

    def is_dish_ready(self, paused):
        """Check if the dish is ready to be picked up."""
        if self.is_preparing and not paused:
            if self.is_preparing and time.time() - self.preparation_start_time >= self.preparation_time:
                return True
            return False

    def draw(self, screen, paused):
        """Draw the kitchen on the screen."""
        kitchen_rect = pg.Rect(self.position[0], self.position[1], Config.get("KITCHEN_SIZE") // 2, Config.get("KITCHEN_SIZE") // 2)
        pg.draw.rect(screen, Config.get("BEIGE"), kitchen_rect)

        if self.is_preparing:
            if self.is_dish_ready(paused) and self.current_dish:
                self.current_dish.draw(screen)
            else:
                font = pg.font.Font(None, 24)
                text = font.render("Preparing...", True, Config.get("WHITE"))
                screen.blit(text, (self.position[0], self.position[1] - 20))