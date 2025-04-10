import pygame as pg
from diner_config import Config
from diner_animation import AnimatedSprite


class Player:
    def __init__(self, name):
        self.__name = name
        self.__speed = Config.get("PLAYER_SPEED")
        self.__positions = [Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2]
        self.__normal_animation = AnimatedSprite("images/player_frame", 100, scale=(0.25, 0.25))
        self.__carrying_animation = AnimatedSprite("images/player_served", 100, scale=(0.25, 0.25))
        self.__current_animation = self.__normal_animation
        self.__is_busy = False
        self.__current_dish = None

    def get_position(self):
        return self.__positions

    def get_current_dish(self):
        return self.__current_dish

    def get_is_busy(self):
        return self.__is_busy

    def set_current_dish(self, current_dish):
        self.__current_dish = current_dish

    def set_position(self, x, y):
        self.__positions[0] = x
        self.__positions[1] = y

    def set_is_busy(self, busy):
        self.__is_busy = busy

    def move(self, keys):
        if not self.__is_busy:
            if keys[pg.K_UP]:
                self.__positions[1] -= self.__speed
            if keys[pg.K_DOWN]:
                self.__positions[1] += self.__speed
            if keys[pg.K_LEFT]:
                self.__positions[0] -= self.__speed
            if keys[pg.K_RIGHT]:
                self.__positions[0] += self.__speed

            # Ensure the player stays within the screen bounds
            self.__positions[0] = max(0, min(self.__positions[0], Config.get("SCREEN_WIDTH") - Config.get("PLAYER_SIZE")))
            self.__positions[1] = max(0, min(self.__positions[1], Config.get("SCREEN_HEIGHT") - Config.get("PLAYER_SIZE")))

    def draw(self, screen):
        self.__current_animation = self.__carrying_animation if self.__current_dish else self.__normal_animation

        self.__current_animation.update()
        self.__current_animation.draw(screen, self.__positions)

        # Display the name of player
        font = pg.font.Font(None, 24)
        name_text = font.render(self.__name, True, Config.get("WHITE"))
        screen.blit(name_text, (self.__positions[0] + 5, self.__positions[1] - 20))
