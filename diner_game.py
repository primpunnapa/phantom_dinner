import pygame as pg
import time
from diner_config import Config
from diner_player import Player
from diner_customer import Customer
from diner_table import Table
from diner_kitchen import Kitchen
from diner_ui import UI
import os
import csv

# Initialize Pygame
pg.init()
screen = pg.display.set_mode((Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")))
pg.display.set_caption("Phantom Diner")
bg_image = pg.image.load('images/darkbg.jpg').convert_alpha()
bg_image = pg.transform.scale(bg_image, (Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")))

clock = pg.time.Clock()
FPS = 60


class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.tables = [Table((350, 250)), Table((550, 250)), Table((350, 350)), Table((550, 350))]
        self.customers = []  # Customers currently seated at tables
        self.waiting_customers = []  # Customers waiting in line
        self.kitchen = Kitchen((Config.get("SCREEN_WIDTH") // 2 + 5, 90))  # Kitchen area

        self.time_left = 90  # 1 minute and 30 seconds
        self.run = True
        self.last_customer_time = time.time()  # Track the last time a customer arrived

        # statistics
        self.score = 0
        self.level = 1
        self.haunt_events = 0
        self.dishes_served = 0
        self.waiting_times = []
        self.player_name = player_name

        # UI
        self.screen = screen
        self.ui = UI(screen)

    def reset_game_state(self):
        """Reset the game state for the next level."""
        # Clear all customers
        self.customers = []
        self.waiting_customers = []

        # Clear all tables
        for table in self.tables:
            table.clear_table()

        # Reset the kitchen
        self.kitchen.is_preparing = False
        self.kitchen.current_dish = None

        # Reset the player's state
        self.player.current_dish = None
        self.player.is_busy = False

    def place_customer(self):
        """Add a new customer to the waiting list or seat them at an available table."""
        current_time = time.time()
        if current_time - self.last_customer_time >= 5:  # 5 seconds have passed
            self.last_customer_time = current_time  # Reset the timer
            customer = Customer(None, self.level)  # Create a new customer
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
        for customer in self.customers + self.waiting_customers:
            customer.update_patience_meter()

        for c in self.customers[:]:
            if c.table.order_status == "waiting":
                c.update_patience_meter()
                if c.leave():
                    print("Customer left! Haunt event trigger!")
                    self.score -= 10
                    self.haunt_events += 1
                    c.table.clear_table()
                    self.customers.remove(c)

            elif c.table.order_status == "served" and c.leave_time is not None:
                if time.time() >= c.leave_time:  # Check if 3 seconds have passed
                    print("Customer is Happy")
                    c.table.clear_table()
                    self.customers.remove(c)

    def draw_waiting_customers(self):
        """Draw waiting customers at the bottom of the screen."""
        x = 30
        y = Config.get("SCREEN_HEIGHT") - Config.get("CUSTOMER_SIZE") - 15
        for customer in self.waiting_customers:
            customer.position = (x, y)  # Set the position for waiting customers
            customer.draw(self.screen)  # Draw the customer and their patience meter
            x += Config.get("CUSTOMER_SIZE") + 30  # Space between customers

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
                t.dish = self.player.current_dish   # Place the dish on the table
                t.dish.position = (t.position[0] + Config.get("TABLE_SIZE") // 2, t.position[1] + Config.get("TABLE_SIZE") // 2)
                self.player.current_dish = None     # Remove dish from player
                self.score += 10                    # Increase score for serving a dish
                self.dishes_served += 1             # Increment dishes served

                print(f"Dish served! Score: {self.score}")

                # Set a timer for customer to disappear after 3 seconds
                for chair in t.chairs:
                    if chair.customer:
                        chair.customer.serve()
                        chair.customer.leave_time = time.time() + 3  # Store the future time
                        break
                return

    def check_level_progress(self):
        """Check if the player has achieved the minimum score to advance to the next level."""
        if self.time_left <= 0:  # Time has run out
            if self.score >= 100:  # Check if the score is sufficient
                self.ui.draw_pause_screen(self.level, self.score)  # Pause and display results
                self.wait_for_enter()  # Wait for the player to press enter

                self.level += 1
                self.score = 0
                self.time_left = 90  # Reset timer for the next level

                self.reset_game_state()  # Reset the game state
                print(f"Advancing to Level {self.level}!")
            else:  # Score is insufficient
                print("Game over! Score is less than 100.")
                if not self.ui.draw_game_over(self.score):  # Display Game Over screen
                    self.run = False  # Quit the game if the player closes the window
                else:
                    # Restart the game
                    self.level = 1
                    self.score = 0
                    self.time_left = 90
                    self.reset_game_state()

    def draw(self):
        """Draw all game objects on the screen."""
        # self.screen.fill(Config.get("BLACK"))
        for table in self.tables:
            table.draw(self.screen)
        self.player.draw(self.screen)
        self.kitchen.draw(self.screen)
        self.ui.draw_time(self.time_left)
        self.ui.draw_score(self.score)
        self.ui.draw_level(self.level)
        self.draw_waiting_customers()

    def wait_for_enter(self):
        """Wait for the player to press enter."""
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    waiting = False

    def save_statistics(self):
        """Save the game statistics to a CSV file."""
        filename = "game_statistics.csv"
        file_exists = os.path.isfile(filename)  # Check if the file already exists

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            # Write the header if the file is new
            if not file_exists:
                writer.writerow(
                    ["Player", "Score", "Waiting Time", "Haunt Events", "Level", "Dishes Served"])

            # Calculate average waiting time
            avg_waiting_time = sum(self.waiting_times) / len(self.waiting_times) if self.waiting_times else 0

            # Write the current game statistics
            writer.writerow([
                self.player_name,
                self.score,
                round(avg_waiting_time, 2),  # Average waiting time
                self.haunt_events,
                self.level,
                self.dishes_served
            ])

    def running(self):
        """Run the main game loop."""
        while self.run:
            clock.tick(FPS)

            # draw background
            screen.blit(bg_image, (0,0))

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.handle_spacebar()  # Handle spacebar actions

            # Get the state of all keys
            keys = pg.key.get_pressed()

            # Update player position based on keys pressed
            self.player.move(keys)

            # Place new customers and seat waiting customers
            self.place_customer()

            # Update customers' patience meters
            self.update_customers()

            # Check level progress
            self.check_level_progress()

            # Update timer
            self.time_left -= 1 / 60  # Decrease time by 1 second per frame
            if self.time_left <= 0:
                self.check_level_progress()

            # Draw game objects
            self.draw()

            # Update display
            pg.display.update()

        game.save_statistics()
        pg.quit()

# Main program
if __name__ == "__main__":
    player_name = input("Enter your name: ")
    game = Game(player_name)
    game.running()