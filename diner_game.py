import pygame as pg
import time
from diner_config import Config
from diner_player import Player
from diner_customer import Customer
from diner_table import Table
from diner_kitchen import Kitchen
from diner_ui import UI
from diner_sound import SoundEffect
import os
import csv
import sys



class Game:
    def __init__(self, player_name, screen):
        self.screen = screen
        self.bg_image = pg.image.load('images/bg.PNG').convert_alpha()
        self.bg_image = pg.transform.scale(self.bg_image,
                                           (Config.get("SCREEN_WIDTH"),
                                            Config.get("SCREEN_HEIGHT")))
        self.player = Player(player_name)
        self.tables = [Table((350, 250)), Table((550, 250)), Table((350, 350)), Table((550, 350))]
        self.customers = []  # Customers currently seated at tables
        self.waiting_customers = []  # Customers waiting in line
        self.kitchen = Kitchen((Config.get("SCREEN_WIDTH") // 2 + 5, 90))  # Kitchen area
        self.time_left = 60  # 1 minute
        self.run = True
        self.last_customer_time = time.time()  # Track the last time a customer arrived
        self.paused = False

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

    def toggle_pause(self):
        """Toggle the pause state of the game."""
        self.paused = not self.paused
        print("Game Paused" if self.paused else "Game Resumed")

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
        self.player.set_current_dish(None)
        self.player.set_is_busy(False)
        self.player.set_position(Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2)

    def place_customer(self):
        """Add a new customer to the waiting list or seat them at an available table."""
        if self.paused:
            return

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
        if not self.paused:
            for customer in self.customers + self.waiting_customers:
                customer.update_patience_meter(self.paused)

            for c in self.customers[:]:
                if c.table.order_status == "waiting":
                    c.update_patience_meter(self.paused)
                    if c.leave():
                        print("Customer left! Haunt event trigger!")
                        self.score -= 10
                        self.haunt_events += 1
                        self.waiting_times.append(time.time() - c.arrival_time)
                        c.table.clear_table()
                        self.customers.remove(c)

                elif c.table.order_status == "served" and c.leave_time is not None:
                    if c.should_leave(self.paused):  # Check if 3 seconds have passed
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
        px, py = player.get_position()
        kx, ky = self.kitchen.position
        return abs(px - kx) < 50 and abs(py - ky) < 50  # Adjust range as needed

    def near_table(self, player, table):
        """Check if the player is near a table."""
        px, py = player.get_position()
        tx, ty = table.position
        return abs(px - tx) < 50 and abs(py - ty) < 50  # Adjust range as needed

    def handle_spacebar(self):
        """Perform context-sensitive actions when Spacebar is pressed."""
        if self.paused:
            return # do nothing if the game is paused

        # If near the kitchen and not preparing a dish → Start cooking
        if self.near_kitchen(self.player) and not self.kitchen.is_preparing:
            self.kitchen.start_preparation()
            return

        # If near the kitchen and the dish is ready → Pick up the dish
        if self.near_kitchen(self.player) and self.kitchen.is_dish_ready(self.paused) and self.player.get_current_dish() is None:
            self.player.set_current_dish(self.kitchen.current_dish) # Player picks up the dish
            self.kitchen.is_preparing = False  # Reset kitchen
            self.kitchen.current_dish = None  # Remove dish from kitchen
            print("Dish picked up!")
            return

        # If holding a dish and near a table with a waiting customer → Serve the dish
        for t in self.tables:
            if self.near_table(self.player, t) and self.player.get_current_dish() and t.order_status == "waiting":
                t.order_status = "served"
                t.dish = self.player.get_current_dish()   # Place the dish on the table
                t.dish.position = (t.position[0] + Config.get("TABLE_SIZE") // 2, t.position[1] + Config.get("TABLE_SIZE") // 2)
                self.player.set_current_dish(None)     # Remove dish from player
                self.score += 10                    # Increase score for serving a dish
                self.dishes_served += 1             # Increment dishes served

                print(f"Dish served! Score: {self.score}")

                # Set a timer for customer to disappear after 3 seconds
                for chair in t.chairs:
                    if chair.customer:
                        chair.customer.serve()
                        # chair.customer.leave_time = time.time() + 3  # Store the future time
                        break
                return

    def check_level_progress(self):
        """Check if the player has achieved the minimum score to advance to the next level."""
        if self.time_left <= 0:  # Time has run out
            if self.score >= 100:  # Check if the score is sufficient
                self.save_statistics()
                self.ui.draw_level_complete_screen(self.level, self.score)
                self.wait_for_enter()  # Wait for the player to press enter

                self.level += 1
                self.score = 0
                # Reset timer for the next level
                self.time_left = 60 + (self.level // 4) * 10

                self.reset_game_state()  # Reset the game state
                print(f"Advancing to Level {self.level}!")

            else:  # Score is insufficient
                self.save_statistics()
                SoundEffect.get_instance().play_sound("over")
                print("Game over! Score is less than 100.")
                if not self.ui.draw_game_over(self.score):  # Display Game Over screen
                    self.run = False  # Quit the game if the player closes the window
                    pg.quit()
                    # sys.exit()
                    return False
                else:
                    # Restart the game
                    self.level = 1
                    self.score = 0
                    self.time_left = 60
                    self.reset_game_state()
        return True

    def draw(self):
        """Draw all game objects on the screen."""
        self.screen.blit(self.bg_image, (0, 0))

        for table in self.tables:
            table.draw(self.screen)
        self.player.draw(self.screen)
        self.kitchen.draw(self.screen, self.paused)
        self.ui.draw_time(self.time_left)
        self.ui.draw_score(self.score)
        self.ui.draw_level(self.level)
        self.draw_waiting_customers()

        # Draw the pause button
        pause_button_rect, resume_button_rect = self.ui.draw_pause_screen(self.paused)

        return pause_button_rect, resume_button_rect

    def wait_for_enter(self):
        """Wait for the player to press enter."""
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                    waiting = False
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    waiting = False
                    SoundEffect.get_instance().play_sound("press")

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
        clock = pg.time.Clock()
        FPS = 60

        while self.run:
            clock.tick(FPS)
            pause_button_rect, resume_button_rect = self.draw()

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.save_statistics()
                    pg.quit()
                    return False  # Signal to close the game

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.handle_spacebar()
                        SoundEffect.get_instance().play_sound("press")
                    elif event.key == pg.K_ESCAPE:  # Add escape key to quit
                        self.save_statistics()
                        pg.quit()
                        return False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if pause_button_rect.collidepoint(event.pos) and not self.paused:
                        self.toggle_pause()
                        SoundEffect.get_instance().play_sound("click")
                    elif self.paused and resume_button_rect and resume_button_rect.collidepoint(event.pos):
                        self.toggle_pause()
                        SoundEffect.get_instance().play_sound("click")

            # Update game state if not paused
            if not self.paused:
                keys = pg.key.get_pressed()
                self.player.move(keys)
                self.place_customer()
                self.update_customers()
                self.check_level_progress()

                # Update timer
                self.time_left -= 1 / 60
                if self.time_left <= 0:
                    self.check_level_progress()

            pg.display.update()

            # Additional check for pygame window close
            if not pg.get_init():
                return False

        return True  # Signal game completed normally


