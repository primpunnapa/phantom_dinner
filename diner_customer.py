import pygame as pg
import time
from diner_config import Config
from diner_animation import AnimatedSprite

class Customer:
    def __init__(self, table, level):
        self.patience_meter = max(Config.get("MIN_PATIENCE"), 100 - (level * 5))
        self.order = "Spider Soup"
        self.table = table
        self.arrival_time = time.time()
        self.leave_time = None
        self.position = None
        self.is_served = False
        self.animation = AnimatedSprite("images/customer_frame", 150, scale=(0.2, 0.2))
        self.served_time = None  # track when customer was served

    def update_patience_meter(self, paused):
        """Update the patience meter over time."""
        if not self.is_served and not paused:
            self.patience_meter -= 0.03
            if self.patience_meter < 0:
                self.patience_meter = 0

    def leave(self):
        return self.patience_meter == 0

    def serve(self):
        self.is_served = True
        self.served_time = time.time()
        self.leave_time = self.served_time + 3

    def should_leave(self, paused):
        if self.is_served and not paused:
            return time.time() >= self.leave_time
        return False

    def draw(self, screen):
        self.animation.update()

        # If the customer is seated at a table, draw them on their chair
        if self.table:
            for chair in self.table.chairs:
                if chair.customer == self:
                    self.position = (chair.position[0] - 10, chair.position[1] - 10)
                    break

        if self.position:
            # Draw the customer
            self.animation.draw(screen, self.position)

            # Draw the patience meter above the customer
            patience_bar_width = Config.get("CUSTOMER_SIZE")
            patience_bar_rect = pg.Rect(
                self.position[0] - (patience_bar_width // 2) + 30,  # Center the bar above the customer
                self.position[1] - Config.get("PATIENCE_BAR_HEIGHT") - 3,  # Position above the customer
                patience_bar_width * (self.patience_meter / 100),  # Width based on patience
                Config.get("PATIENCE_BAR_HEIGHT")
            )
            pg.draw.rect(screen, Config.get("RED"), patience_bar_rect)

            # Display the customer's order above the patience meter
            if not self.is_served:
                font = pg.font.Font(None, 24)
                order_text = font.render(self.order, True, Config.get("WHITE"))
                text_x = self.position[0] - (order_text.get_width() // 2) + 30  # Center the text
                text_y = self.position[1] - Config.get("PATIENCE_BAR_HEIGHT") - 30  # Position above the patience bar
                screen.blit(order_text, (text_x, text_y))

