import pygame as pg
from diner_config import Config
import time

class Dish:
    def __init__(self, name, prep_time, pos):
        self.name = name
        self.prep_time = prep_time
        self.position = pos

    def prepare(self):
        """Simulate dish preparation."""
        print(f"Preparing {self.name}...")
        time.sleep(self.prep_time)
        print(f"{self.name} is ready!")

    def draw(self, screen):
        """Draw the dish on the screen."""
        # Draw bowl (centered at self.position)
        pg.draw.circle(screen, Config.get("BLACK"), self.position, 12, 2)
        # Draw soup (centered at self.position)
        border_rect = pg.Rect(self.position[0] - 11, self.position[1] - 12, 22, 12)
        soup_rect = pg.Rect(self.position[0] - 10, self.position[1] - 12, 20, 10)
        pg.draw.ellipse(screen, Config.get("BLACK"), border_rect)
        pg.draw.ellipse(screen, Config.get("RED"), soup_rect)
