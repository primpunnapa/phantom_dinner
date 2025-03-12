import pygame as pg
from diner_config import Config
from diner_customer import Customer

class Table:
    def __init__(self, pos):
        self.position = pos  # (x,y)
        self.customer = None
        self.order_status = "empty"  # Can be "waiting", "served", or "empty"

    def seat_customer(self, customer: Customer):
        self.customer = customer
        self.order_status = "waiting"

    def clear_table(self):
        self.customer = None
        self.order_status = "empty"

    def draw(self, screen):
        # Draw the table
        table_rect = pg.Rect(
            self.position[0],
            self.position[1],
            Config.get("TABLE_SIZE"),
            Config.get("TABLE_SIZE")
        )
        pg.draw.rect(screen, Config.get("WHITE"), table_rect)

        # Draw the customer (if seated)
        if self.customer:
            self.customer.draw(screen)