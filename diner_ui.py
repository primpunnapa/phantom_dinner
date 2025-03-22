from diner_config import Config
import pygame as pg

class UI:
    def __init__(self, screen):
        self.screen = screen

    def draw_time(self, time_left):
        """Draw the remaining time on the screen with a background box."""
        font = pg.font.Font(None, 36)
        time_text = font.render(f"Time: {int(time_left)}", True, Config.get("WHITE"))

        # Calculate the position and size of the background box
        text_width, text_height = time_text.get_size()
        box_x = Config.get("SCREEN_WIDTH") - 150 - 10  # Add padding
        box_y = 30 - 5  # Add padding
        box_width = text_width + 20  # Add padding
        box_height = text_height + 10  # Add padding

        # Draw the background box
        pg.draw.rect(self.screen, Config.get("BLACK"), (box_x, box_y, box_width, box_height))

        # Draw the text on top of the box
        self.screen.blit(time_text, (Config.get("SCREEN_WIDTH") - 150, 30))

    def draw_score(self, score):
        """Draw the player's score on the screen with a background box."""
        font = pg.font.Font(None, 36)
        score_text1 = font.render("SCORE : ", True, Config.get("WHITE"))
        score_text2 = font.render(str(score), True, Config.get("WHITE"))

        # Calculate the position and size of the background box
        text1_width, text1_height = score_text1.get_size()
        text2_width, text2_height = score_text2.get_size()
        box_x = 100 - 5  # Add padding
        box_y = 30 - 5  # Add padding
        box_width = text1_width + text2_width + 30  # Add padding
        box_height = max(text1_height, text2_height) + 10  # Add padding

        # Draw the background box
        pg.draw.rect(self.screen, Config.get("BLACK"), (box_x, box_y, box_width, box_height))

        # Draw the text on top of the box
        self.screen.blit(score_text1, (130, 30))
        self.screen.blit(score_text2, (250, 30))

    def draw_level(self, level):
        """Draw the current level on the screen with a background box."""
        font = pg.font.Font(None, 36)
        level_text1 = font.render("LEVEL : ", True, Config.get("WHITE"))
        level_text2 = font.render(str(level), True, Config.get("WHITE"))

        # Calculate the position and size of the background box
        text1_width, text1_height = level_text1.get_size()
        text2_width, text2_height = level_text2.get_size()
        box_x = Config.get("SCREEN_WIDTH") // 2 - 50 - 10  # Add padding
        box_y = 30 - 5  # Add padding
        box_width = text1_width + text2_width + 20  # Add padding
        box_height = max(text1_height, text2_height) + 10  # Add padding

        # Draw the background box
        pg.draw.rect(self.screen, Config.get("BLACK"), (box_x, box_y, box_width, box_height))

        # Draw the text on top of the box
        self.screen.blit(level_text1, (Config.get("SCREEN_WIDTH") // 2 - 50, 30))
        self.screen.blit(level_text2, (Config.get("SCREEN_WIDTH") // 2 + 50, 30))

    def draw_pause_button(self, paused):
        """Draw the pause button on the screen."""
        button_rect = pg.Rect(10, 10, Config.get("BUTTON_SIZE"), Config.get("BUTTON_SIZE"))  # Position and size of the button
        button_color = Config.get("BLUE") if not paused else Config.get("RED")  # Change color when paused
        pg.draw.rect(self.screen, button_color, button_rect)

        # Draw the text on the button
        font = pg.font.Font(None, 24)
        button_text = font.render("||" if not paused else "||", True, Config.get("WHITE"))
        text_x = button_rect.x + (button_rect.width - button_text.get_width()) // 2
        text_y = button_rect.y + (button_rect.height - button_text.get_height()) // 2
        self.screen.blit(button_text, (text_x, text_y))

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
                    pg.quit()
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