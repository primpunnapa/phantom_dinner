import pygame as pg
import time

class Dish:
    def __init__(self, name, prep_time, pos):
        self.name = name
        self.prep_time = prep_time
        self.position = pos
        self.image = pg.image.load("images/dish.PNG").convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))

    def prepare(self):
        """Simulate dish preparation."""
        print(f"Preparing {self.name}...")
        time.sleep(self.prep_time)
        print(f"{self.name} is ready!")

    def draw(self, screen):
        """Draw the dish on the screen."""
        screen.blit(self.image, (self.position[0] - 27, self.position[1] - 28))
