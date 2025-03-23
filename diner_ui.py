from diner_config import Config
import pygame as pg

class UI:
    def __init__(self, screen):
        self.screen = screen

    def draw_time(self, time_left):
        """Draw the remaining time on the screen with a background box."""
        font = pg.font.Font(None, 36)
        time_text = font.render(f"TIME: {int(time_left)}", True, Config.get("YELLOW"))

        # Calculate the position and size of the background box
        text_width, text_height = time_text.get_size()
        box_x = Config.get("SCREEN_WIDTH") - 150 - 10  # Add padding
        box_y = 5 - 5  # Add padding
        box_width = text_width + 30  # Add padding
        box_height = text_height + 20  # Add padding

        # Draw the background box
        pg.draw.rect(self.screen, Config.get("GREEN"), (box_x, box_y, box_width, box_height))

        # Draw the text on top of the box
        self.screen.blit(time_text, (Config.get("SCREEN_WIDTH") - 150, 10))

    def draw_score(self, score):
        """Draw the player's score on the screen with a background box."""
        font = pg.font.Font(None, 36)
        score_text1 = font.render("SCORE : ", True, Config.get("YELLOW"))
        score_text2 = font.render(str(score), True, Config.get("YELLOW"))

        # Calculate the position and size of the background box
        text1_width, text1_height = score_text1.get_size()
        text2_width, text2_height = score_text2.get_size()
        box_x = 140 - 5  # Add padding
        box_y = 5 - 5  # Add padding
        box_width = text1_width + text2_width + 50  # Add padding
        box_height = max(text1_height, text2_height) + 20  # Add padding

        # Draw the background box
        pg.draw.rect(self.screen, Config.get("DARKPURPLE"), (box_x, box_y, box_width, box_height))

        # Draw the text on top of the box
        self.screen.blit(score_text1, (150, 10))
        self.screen.blit(score_text2, (270, 10))

    def draw_level(self, level):
        """Draw the current level on the screen with a background box."""
        font = pg.font.Font(None, 36)
        level_text1 = font.render("LEVEL : ", True, Config.get("YELLOW"))
        level_text2 = font.render(str(level), True, Config.get("YELLOW"))

        # Calculate the position and size of the background box
        text1_width, text1_height = level_text1.get_size()
        text2_width, text2_height = level_text2.get_size()
        box_x = Config.get("SCREEN_WIDTH") // 2 - 10
        box_y = 5 - 5  # Add padding
        box_width = text1_width + text2_width + 30  # Add padding
        box_height = max(text1_height, text2_height) + 20  # Add padding

        # Draw the background box
        pg.draw.rect(self.screen, Config.get("DARKBLUE"), (box_x, box_y, box_width, box_height))

        # Draw the text on top of the box
        self.screen.blit(level_text1, (Config.get("SCREEN_WIDTH") // 2, 10))
        self.screen.blit(level_text2, (Config.get("SCREEN_WIDTH") // 2 + 100, 10))

    def draw_pause_button(self, paused):
        """Draw the pause button on the screen."""
        center_x = 40
        center_y = 20

        radius = Config.get("BUTTON_SIZE") // 2
        button_color = Config.get("GREY") if not paused else Config.get("RED")

        # Draw the circular button
        pg.draw.circle(self.screen, button_color, (center_x, center_y), radius)

        # Draw the pause icon ("||")
        font = pg.font.Font(None, 36)
        button_text = font.render("||", True, Config.get("WHITE"))

        # Center the text within the circle
        text_x = center_x - button_text.get_width() // 2
        text_y = center_y - button_text.get_height() // 2
        self.screen.blit(button_text, (text_x, text_y))

        button_rect = pg.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)

        return button_rect  # Return the button's rectangle for click detection

    def draw_game_over(self, score):
        """Display the Game Over screen and wait for the player to press enter."""
        tmp_opacity = pg.Surface((Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")), pg.SRCALPHA)
        tmp_opacity.fill((0, 0, 0, 200))
        tmp = pg.Surface((Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")), pg.SRCALPHA)
        tmp.fill((0, 0, 0, 0))

        font = pg.font.Font(None, 48)
        game_over_text = font.render("Game Over!", True, Config.get("WHITE"))
        score_text = font.render(f"Final Score: {score}", True, Config.get("WHITE"))
        continue_text = font.render("Press ENTER to play again", True, Config.get("WHITE"))

        # Position the text
        rect1 = game_over_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2 - 50))
        rect2 = score_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2))
        rect3 = continue_text.get_rect(center=(Config.get("SCREEN_WIDTH") // 2, Config.get("SCREEN_HEIGHT") // 2 + 50))

        tmp.blit(game_over_text, rect1)
        tmp.blit(score_text, rect2)
        tmp.blit(continue_text, rect3)

        # Draw the messages on the screen
        self.screen.blit(tmp_opacity, (0, 0))
        self.screen.blit(tmp, (0, 0))

        # Update the display
        pg.display.update()

        # Wait for the player to press enter
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # pg.quit()
                    # sys.exit()
                    return False  # Quit the game
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    waiting = False
        return True  # Restart the game

    def draw_level_complete_screen(self, level, score):
        """Draw the level completion screen with the level, score, and continue message."""
        tmp_opacity = pg.Surface((Config.get("SCREEN_WIDTH"), Config.get("SCREEN_HEIGHT")), pg.SRCALPHA)
        tmp_opacity.fill((0, 0, 0, 128))  # Semi-transparent black

        self.screen.blit(tmp_opacity, (0, 0))

        # Display the level completion message
        font = pg.font.Font(None, 48)
        level_text = font.render(f"Level {level} Complete!", True, Config.get("WHITE"))
        score_text = font.render(f"Score: {score}", True, Config.get("WHITE"))
        continue_text = font.render("Press ENTER to continue", True, Config.get("WHITE"))

        # Position the text in the center of the screen
        text_x = Config.get("SCREEN_WIDTH") // 2 - level_text.get_width() // 2
        text_y = Config.get("SCREEN_HEIGHT") // 2 - level_text.get_height() // 2

        self.screen.blit(level_text, (text_x, text_y - 50))
        self.screen.blit(score_text, (text_x, text_y))
        self.screen.blit(continue_text, (text_x, text_y + 50))

        # Update the display
        pg.display.update()