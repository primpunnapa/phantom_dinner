from diner_config import Config
import pygame as pg

class UI:
    def __init__(self, screen):
        self.screen = screen

    def draw_time(self, time_left):
        """Draw the remaining time on the screen."""
        font = pg.font.Font(None, 36)
        time_text = font.render(f"Time: {int(time_left)}", True, Config.get("WHITE"))
        self.screen.blit(time_text, (Config.get("SCREEN_WIDTH") - 150, 50))

    def draw_score(self, score):
        """Draw the player's score on the screen."""
        font = pg.font.Font(None, 36)
        score_text1 = font.render("SCORE : ", True, Config.get("WHITE"))
        score_text2 = font.render(str(score), True, Config.get("WHITE"))
        self.screen.blit(score_text1, (80, 50))
        self.screen.blit(score_text2, (200, 50))

    def draw_level(self, level):
        """Draw the current level on the screen."""
        font = pg.font.Font(None, 36)
        level_text1 = font.render("LEVEL : ", True, Config.get("WHITE"))
        level_text2 = font.render(str(level), True, Config.get("WHITE"))
        self.screen.blit(level_text1, (Config.get("SCREEN_WIDTH") // 2 - 50, 50))
        self.screen.blit(level_text2, (Config.get("SCREEN_WIDTH") // 2 + 50, 50))

    def draw_pause_screen(self, level, score):
        """Draw the pause screen between levels."""
        tmp_opacity = pg.Surface((Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")), pg.SRCALPHA)
        tmp_opacity.fill((0, 0, 0, 200))
        tmp = pg.Surface((Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")), pg.SRCALPHA)
        tmp.fill((0, 0, 0, 0))

        font = pg.font.Font(None, 48)
        level_text = font.render(f"Level {level} Complete!", True, Config.get("WHITE"))
        score_text = font.render(f"Score: {score}", True, Config.get("WHITE"))
        continue_text = font.render("Press SPACE to continue", True, Config.get("WHITE"))

        rect1 = level_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, (Config.get("SCREEN_HEIGHT") // 2) - 60))
        rect2 = score_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2))
        rect3 = continue_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, (Config.get("SCREEN_HEIGHT") // 2) + 60))

        tmp.blit(level_text, rect1)
        tmp.blit(score_text, rect2)
        tmp.blit(continue_text, rect3)

        # Draw the messages on the screen
        self.screen.blit(tmp_opacity, (0, 0))
        self.screen.blit(tmp, (0, 0))

        pg.display.update()

    def draw_game_over(self, score):
        """Display the Game Over screen and wait for the player to press spacebar."""
        font = pg.font.Font(None, 48)
        game_over_text = font.render("Game Over!", True, Config.get("WHITE"))
        score_text = font.render(f"Final Score: {score}", True, Config.get("WHITE"))
        continue_text = font.render("Press SPACE to play again", True, Config.get("WHITE"))

        # Position the text
        rect1 = game_over_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2 - 50))
        rect2 = score_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2))
        rect3 = continue_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2 + 50))

        # Draw the messages on the screen
        self.screen.blit(game_over_text, rect1)
        self.screen.blit(score_text, rect2)
        self.screen.blit(continue_text, rect3)

        # Update the display
        pg.display.update()

        # Wait for the player to press spacebar
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return False  # Quit the game
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    waiting = False
        return True  # Restart the game
