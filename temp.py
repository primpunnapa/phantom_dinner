import pygame as pg
import time
import random
from diner_config import Config
import os

# Initialize Pygame
pg.init()
screen = pg.display.set_mode((Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")))
clock = pg.time.Clock()
FPS = 60


class AnimatedSprite:
    def __init__(self, folder_path, frame_duration, scale=(1, 1)):
        self.frames = []  # List to store loaded frames
        self.frame_duration = frame_duration  # Time (in milliseconds) to display each frame
        self.current_frame = 0  # Index of the current frame
        self.last_update = pg.time.get_ticks()  # Time when the frame was last updated
        self.scale = scale  # Scaling factor for the frames

        # Load all frames from the folder
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):  # Ensure only PNG files are loaded
                frame = pg.image.load(os.path.join(folder_path, filename)).convert_alpha()
                # Scale the frame if scaling is needed
                if self.scale != (1, 1):
                    frame = pg.transform.scale(frame, (int(frame.get_width() * self.scale[0]), int(frame.get_height() * self.scale[1])))
                self.frames.append(frame)

    def update(self):
        """Update the current frame based on time."""
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # Loop frames

    def draw(self, screen, position):
        """Draw the current frame on the screen."""
        screen.blit(self.frames[self.current_frame], position)


class Customer:
    def __init__(self, table):
        self.patience_meter = 100
        self.order = "Spider Soup"
        self.table = table
        self.arrival_time = time.time()
        self.animation = AnimatedSprite("images/customer_frame", 100, scale=(0.2, 0.2))  # Scale frames to 50%

    def update_patience_meter(self):
        self.patience_meter -= 0.1
        if self.patience_meter < 0:
            self.patience_meter = 0

    def leave(self):
        return self.patience_meter == 0

    def draw(self, screen):
        self.animation.update()
        self.animation.draw(screen, self.table.position)

        # Draw the patience meter above the customer
        patience_bar_width = Config.get("CUSTOMER_SIZE")
        patience_bar_rect = pg.Rect(
            self.table.position[0],
            self.table.position[1] - Config.get("PATIENCE_BAR_HEIGHT") - 5,
            patience_bar_width * (self.patience_meter / 100),
            Config.get("PATIENCE_BAR_HEIGHT")
        )
        pg.draw.rect(screen, Config.get("RED"), patience_bar_rect)

        # Display the customer's order above the patience meter
        font = pg.font.Font(None, 24)
        order_text = font.render(self.order, True, Config.get("BLACK"))
        screen.blit(order_text, (self.table.position[0], self.table.position[1] - 30))


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.speed = Config.get("PLAYER_SPEED")
        self.positions = [Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2]
        self.animation = AnimatedSprite("images/player_frame", 100, scale=(0.2, 0.2))
        self.is_busy = False
        self.current_dish = None

    def move(self, keys):
        if not self.is_busy:
            if keys[pg.K_UP]:
                self.positions[1] -= self.speed
            if keys[pg.K_DOWN]:
                self.positions[1] += self.speed
            if keys[pg.K_LEFT]:
                self.positions[0] -= self.speed
            if keys[pg.K_RIGHT]:
                self.positions[0] += self.speed

            # Ensure the player stays within the screen bounds
            self.positions[0] = max(0, min(self.positions[0], Config.get("SCREEN_WIDTH") - Config.get("PLAYER_SIZE")))
            self.positions[1] = max(0, min(self.positions[1], Config.get("SCREEN_HEIGHT") - Config.get("PLAYER_SIZE")))

    def draw(self, screen):
        self.animation.update()
        self.animation.draw(screen, self.positions)


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

class Dish:
    def __init__(self, name, prep_time):
        self.name = name
        self.prep_time = prep_time
        self.position = pos
        #self.image = pg.image.load(Config.get("DISH_IMAGES")[name])  # Load dish image
        #self.image = pg.transform.scale(self.image, (Config.get("DISH_SIZE"), Config.get("DISH_SIZE")))

    def prepare(self):
        """Simulate dish preparation."""
        print(f"Preparing {self.name}...")
        time.sleep(self.prep_time)
        print(f"{self.name} is ready!")
    
    def draw(self, screen):
        """Draw the kitchen on the screen."""
        # draw bowl
        pg.draw.circle(screen, Config.get("BEIGE"), self.position, 5)
        # draw soup
        pg.draw.circle(screen, Config.get("BEIGE"), self.position, 5)

        #pg.draw.rect(screen, Config.get("RED"), (*self.position, Config.get("DISH_SIZE"), Config.get("DISH_SIZE")))
        if self.is_preparing:
            font = pg.font.Font(None, 24)
            text = font.render("Preparing...", True, Config.get("BLACK"))
            screen.blit(text, (self.position[0], self.position[1] - 20))



class Kitchen:
    def __init__(self, pos):
        self.position = pos  # (x, y) coordinates of the kitchen
        self.is_preparing = False  # Whether a dish is being prepared
        self.preparation_time = 5  # Time required to prepare the dish (in seconds)
        self.preparation_start_time = 0  # Time when dish preparation started
        self.current_dish = None  # The dish currently being prepared

    def start_preparation(self):
        """Start preparing the dish."""
        if not self.is_preparing:
            self.is_preparing = True
            self.preparation_start_time = time.time()
            self.current_dish = Dish("Spider Soup", self.preparation_time)  # Create a new dish

    def is_dish_ready(self):
        """Check if the dish is ready to be picked up."""
        if self.is_preparing and time.time() - self.preparation_start_time >= self.preparation_time:
            return True
        return False

    def draw(self, screen):
        """Draw the kitchen on the screen."""
        pg.draw.rect(screen, Config.get("BEIGE"), (*self.position, Config.get("KITCHEN_SIZE"), Config.get("KITCHEN_SIZE")))
        if self.is_preparing:
            font = pg.font.Font(None, 24)
            text = font.render("Preparing...", True, Config.get("BLACK"))
            screen.blit(text, (self.position[0], self.position[1] - 20))

class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.tables = [Table((100, 100)), Table((300, 100)), Table((500, 100))]
        self.customers = []  # Customers currently seated at tables
        self.waiting_customers = []  # Customers waiting in line
        self.kitchen = Kitchen((700, 100))  # Kitchen area
        self.level = 1
        self.score = 0
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
        for c in self.customers[:]:  # Iterate over a copy of the list
            c.update_patience_meter()
            if c.leave():
                print("Customer left! Haunt event trigger!")
                self.score -= 10
                c.table.clear_table()
                self.customers.remove(c)

    def check_level_progress(self):
        """Check if the player has achieved the minimum score to advance to the next level."""
        if self.score >= 100 and self.time_left > 0:
            self.level += 1
            self.score = 0
            self.time_left = 90  # Reset timer for the next level
            print(f"Advancing to Level {self.level}!")

    def draw_waiting_customers(self, screen):
        """Draw waiting customers at the bottom of the screen."""
        x = 10
        y = Config.get("SCREEN_HEIGHT") - Config.get("CUSTOMER_SIZE") - 10
        for customer in self.waiting_customers:
            screen.blit(customer.image, (x, y))
            x += Config.get("CUSTOMER_SIZE") + 10  # Space between customers

    def draw_kitchen(self, screen):
        """Draw the kitchen and its current state on the screen."""
        self.kitchen.draw(screen)
        if self.kitchen.is_preparing:
            font = pg.font.Font(None, 24)
            text = font.render("Preparing...", True, Config.get("BLACK"))
            screen.blit(text, (self.kitchen.position[0], self.kitchen.position[1] - 20))


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
        game.draw_kitchen(screen)
        game.player.draw(screen)
        game.draw_waiting_customers(screen)  # Draw waiting customers

        # Update display
        pg.display.update()

    pg.quit()