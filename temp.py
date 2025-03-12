import pygame as pg
import time
from diner_config import Config
from diner_player import Player
from diner_customer import Customer
from diner_table import Table
from diner_kitchen import Kitchen

# Initialize Pygame
pg.init()
screen = pg.display.set_mode((Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")))
clock = pg.time.Clock()
FPS = 60


class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.tables = [Table((100, 100)), Table((300, 100)), Table((500, 100))]
        self.customers = []  # Customers currently seated at tables
        self.waiting_customers = []  # Customers waiting in line
        self.kitchen = Kitchen((700, 300))  # Kitchen area
        self.level = 1
        self.time_left = 90  # 1 minute and 30 seconds
        self.run = True
        self.last_customer_time = time.time()  # Track the last time a customer arrived

    def place_customer(self):
        """Add a new customer to the waiting list or seat them at an available table."""
        current_time = time.time()
        if current_time - self.last_customer_time >= 10:  # 10 seconds have passed
            self.last_customer_time = current_time  # Reset the timer
            customer = Customer(None)  # Create a new customer
            print(f"New customer arrived and is waiting in line!")
            self.waiting_customers.append(customer)  # Add to the waiting list

        # Try to seat waiting customers if tables are available
        for table in self.tables:
            if table.order_status == "empty" and self.waiting_customers:
                customer = self.waiting_customers.pop(0)  # Seat the first customer in line
                table.seat_customer(customer)
                customer.table = table
                self.customers.append(customer)
                print(f"Customer seated at table {table.position}!")

    def update_customers(self):
        """Update the patience meters of all customers and handle haunt events."""
        for c in self.customers:
            if c.table.order_status == "waiting":
                c.update_patience_meter()
                if c.leave():
                    print("Customer left! Haunt event trigger!")
                    self.player.score -= 10
                    c.table.clear_table()
                    self.customers.remove(c)
            elif c.table.order_status == "served" and c.leave_time is not None:
                if time.time() >= c.leave_time:  # Check if 3 seconds have passed
                    print("Customer left after being served!")
                    c.table.clear_table()
                    self.customers.remove(c)

    def check_level_progress(self):
        """Check if the player has achieved the minimum score to advance to the next level."""
        if self.player.score >= 100 and self.time_left > 0:
            self.level += 1
            self.player.score = 0
            self.time_left = 90  # Reset timer for the next level
            print(f"Advancing to Level {self.level}!")

    def draw_waiting_customers(self, screen):
        """Draw waiting customers at the bottom of the screen."""
        x = 10
        y = Config.get("SCREEN_HEIGHT") - Config.get("CUSTOMER_SIZE") - 15
        for customer in self.waiting_customers:
            customer.animation.draw(screen, (x, y))
            x += Config.get("CUSTOMER_SIZE") + 10  # Space between customers

    def near_kitchen(self, player):
        """Check if the player is near the kitchen."""
        px, py = player.positions
        kx, ky = self.kitchen.position
        return abs(px - kx) < 50 and abs(py - ky) < 50  # Adjust range as needed

    def near_table(self, player, table):
        """Check if the player is near a table."""
        px, py = player.positions
        tx, ty = table.position
        return abs(px - tx) < 50 and abs(py - ty) < 50  # Adjust range as needed

    def handle_spacebar(self):
        """Perform context-sensitive actions when Spacebar is pressed."""

        # If near the kitchen and not preparing a dish → Start cooking
        if self.near_kitchen(self.player) and not self.kitchen.is_preparing:
            self.kitchen.start_preparation()
            return

        # If near the kitchen and the dish is ready → Pick up the dish
        if self.near_kitchen(self.player) and self.kitchen.is_dish_ready() and self.player.current_dish is None:
            self.player.current_dish = self.kitchen.current_dish  # Player picks up the dish
            self.kitchen.is_preparing = False  # Reset kitchen
            self.kitchen.current_dish = None  # Remove dish from kitchen
            print("Dish picked up!")
            return

        # If holding a dish and near a table with a waiting customer → Serve the dish
        for t in self.tables:
            if self.near_table(self.player, t) and self.player.current_dish and t.order_status == "waiting":
                t.order_status = "served"
                self.player.current_dish = None  # Remove dish from player
                self.player.score += 10  # Increase score for serving a dish
                print(f"Dish served! Score: {self.player.score}")

                # Set a timer for customer to disappear after 3 seconds
                t.customer.leave_time = time.time() + 3  # Store the future time
                return


# Main program
if __name__ == "__main__":
    player_name = input("Enter your name: ")
    game = Game(player_name)

    # Game loop
    run = True
    while run:
        clock.tick(FPS)

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                game.handle_spacebar()  # Handle spacebar actions

        # Get the state of all keys
        keys = pg.key.get_pressed()

        # Update player position based on keys pressed
        game.player.move(keys)

        # Place new customers and seat waiting customers
        game.place_customer()

        # Update customers' patience meters
        game.update_customers()

        # Check level progress
        game.check_level_progress()

        # Update timer
        game.time_left -= 1 / 60  # Decrease time by 1 second per frame
        if game.time_left <= 0:
            print("Time's up! Game over.")
            run = False

        # Draw game objects
        screen.fill(Config.get("BLACK"))
        for table in game.tables:
            table.draw(screen)
        game.player.draw(screen)
        game.draw_waiting_customers(screen)  # Draw waiting customers
        game.kitchen.draw(screen)

        # Update display
        pg.display.update()

    pg.quit()