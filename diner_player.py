import pygame as pg
from diner_config import Config
from diner_animation import AnimatedSprite


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.level = 1
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

        # Display score
        font1 = pg.font.Font(None, 36)
        score_text1 = font1.render("score : ", True, Config.get("WHITE"))
        score_text2 = font1.render(str(self.score), True, Config.get("WHITE"))
        screen.blit(score_text1, (80, 50))
        screen.blit(score_text2, (180, 50))

        # Display level
        score_text1 = font1.render("level : ", True, Config.get("WHITE"))
        score_text2 = font1.render(str(self.level), True, Config.get("WHITE"))
        screen.blit(score_text1, (Config.get("SCREEN_WIDTH") // 2 - 50, 50))
        screen.blit(score_text2, (Config.get("SCREEN_WIDTH") // 2 + 50, 50))

        # Display the name of player
        font = pg.font.Font(None, 24)
        name_text = font.render(self.name, True, Config.get("WHITE"))
        screen.blit(name_text, (self.positions[0], self.positions[1] - 30))

        # If holding a dish, draw it
        if self.current_dish:
            self.current_dish.draw(screen)