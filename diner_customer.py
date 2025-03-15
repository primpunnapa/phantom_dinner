import pygame as pg
import time
from diner_config import Config
from diner_animation import AnimatedSprite

class Customer:
    def __init__(self, table, level):
        self.patience_meter = 100 - (level * 5)  # Decrease patience by 5% per level
        self.order = "Spider Soup"
        self.table = table
        self.arrival_time = time.time()
        self.leave_time = None
        self.animation = AnimatedSprite("images/customer_frame", 150, scale=(0.2, 0.2))

    def update_patience_meter(self):
        if self.table.order_status == "waiting":
            self.patience_meter -= 0.05
            if self.patience_meter < 0:
                self.patience_meter = 0

    def leave(self):
        return self.patience_meter == 0

    def draw(self, screen):
        self.animation.update()
        #self.animation.draw(screen, (self.table.position[0] + 1, self.table.position[1]))
        # Draw the customer on their chair (if seated)

        chair_position = None     # Find the chair the customer is seated on
        for chair in self.table.chairs:
            if chair.customer == self:
                chair_position = chair.position
                break

        if chair_position:
            # Draw the customer on their chair
            self.animation.draw(screen, (chair_position[0] - 10, chair_position[1] - 10))

            # Draw the patience meter above the customer
            patience_bar_width = Config.get("CUSTOMER_SIZE")
            patience_bar_rect = pg.Rect(
                chair_position[0] - (patience_bar_width // 2) + 5,  # Center the bar above the customer
                chair_position[1] - Config.get("PATIENCE_BAR_HEIGHT") - 3,  # Position above the customer
                patience_bar_width * (self.patience_meter / 100),  # Width based on patience
                Config.get("PATIENCE_BAR_HEIGHT")
            )

            pg.draw.rect(screen, Config.get("RED"), patience_bar_rect)
            if self.table.order_status == "waiting":
                # Display the customer's order above the patience meter
                font = pg.font.Font(None, 24)
                order_text = font.render(self.order, True, Config.get("WHITE"))
                text_x = chair_position[0] - (order_text.get_width() // 2 + 5) # Center the text
                text_y = chair_position[1] - Config.get("PATIENCE_BAR_HEIGHT") - 30  # Position above the patience bar
                screen.blit(order_text, (text_x, text_y))

