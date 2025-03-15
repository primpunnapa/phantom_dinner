import pygame as pg
from diner_config import Config
from diner_customer import Customer

class Table:
    def __init__(self, pos):
        self.position = pos  # (x,y)
        self.order_status = "empty"  # Can be "waiting", "served", or "empty"
        self.dish = None    # The dish served to the customer
        self.chairs = []    # List of chairs associated with the table
        self.chairs.append(Chair((pos[0] - Config.get("TABLE_SIZE"), pos[1])))  # Chair to the left of the table

    def seat_customer(self, customer):
        """Seat a customer at the table."""
        for chair in self.chairs:
            if not chair.customer:  # Find the first empty chair
                chair.seat_customer(customer)
                self.order_status = "waiting"
                break

    def clear_table(self):
        self.order_status = "empty"
        self.dish = None
        for chair in self.chairs:
            chair.clear_chair()

    def draw(self, screen):
        # Draw the table
        table_rect = pg.Rect(
            self.position[0],
            self.position[1],
            Config.get("TABLE_SIZE"),
            Config.get("TABLE_SIZE")
        )
        pg.draw.rect(screen, Config.get("WHITE"), table_rect)

        # Draw the chairs
        for chair in self.chairs:
            chair.draw(screen)

        # Draw the dish on the table if served
        if self.order_status == "served" and self.dish:
            self.dish.draw(screen)

class Chair:
    def __init__(self, pos):
        self.position = pos  # (x, y) coordinates of the chair
        self.customer = None  # The customer seated on the chair

    def seat_customer(self, customer):
        """Seat a customer on the chair."""
        self.customer = customer

    def clear_chair(self):
        """Clear the chair (remove the customer)."""
        self.customer = None

    def draw(self, screen):
        """Draw the chair on the screen."""
        chair_rect = pg.Rect(
            self.position[0],
            self.position[1],
            Config.get("CHAIR_SIZE"),
            Config.get("CHAIR_SIZE")
        )
        pg.draw.rect(screen, Config.get("LIGHTBROWN"), chair_rect)  # Draw the chair

        # Draw the customer if seated
        if self.customer:
            self.customer.draw(screen)