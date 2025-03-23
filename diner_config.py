
class Config:
    __ALL_CONFIGS = {
        "SCREEN_WIDTH": 800,
        "SCREEN_HEIGHT": 600,
        # player
        "PLAYER_SIZE": 50,
        "PLAYER_SPEED": 6,
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
        "KITCHEN_SIZE": 100,

        #chair
        "CHAIR_SIZE": 30,

        #pause botton
        "BUTTON_SIZE": 40,

        #min patience
        "MIN_PATIENCE": 30,
        
        # colors
        "BLACK": (0, 0, 0),
        "WHITE": (255, 255, 255),
        "GREEN": (3, 76, 83),
        "RED": (205, 24, 24),
        "LIGHTRED": (229, 32, 32),
        "BLUE": (41, 115, 178),
        "BEIGE": (255, 246, 233),
        "LIGHTBROWN": (255, 200, 150),
        "DARKBLUE": (43, 42, 76),
        "DARKPURPLE": (79, 28, 81),
        "ORANGE": (241, 74, 0),
        "YELLOW": (255, 178, 0),
        "GREY": (76, 88, 91)
    }

    @classmethod
    def get(cls, key):
        return cls.__ALL_CONFIGS[key]
