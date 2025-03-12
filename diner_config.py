
class Config:
    __ALL_CONFIGS = {
        "SCREEN_WIDTH": 800,
        "SCREEN_HEIGHT": 600,
        # player
        "PLAYER_SIZE": 50,
        "PLAYER_SPEED": 10,
        "PLAYER_IMG": "images/waiter.png",
        "PATIENCE_BAR_HEIGHT": 5,
        # dish
        "DISH_SIZE": 30,

        # customer
        "CUSTOMER_SIZE": 50,
        "CUSTOMER_IMG": "images/customer.png",
        #table
        "TABLE_SIZE": 50,
        
        #kitchen
        "KITCHEN_SIZE": 50,
        
        # colors
        "BLACK": (0, 0, 0),
        "WHITE": (255, 255, 255),
        "GREEN": (0, 255, 0),
        "RED": (255, 0, 0),
        "BLUE": (64, 162, 227),
        "BEIGE": (255, 246, 233),
        "LIGHTBROWN": (255, 200, 150),
    }

    @classmethod
    def get(cls, key):
        return cls.__ALL_CONFIGS[key]
