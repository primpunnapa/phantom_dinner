import pygame as pg
import os

class AnimatedSprite:
    def __init__(self, folder_path, frame_duration, scale=(1, 1)):
        self.frames = []  # List to store loaded frames
        self.frame_duration = frame_duration  # Time (in milliseconds) to display each frame
        self.current_frame = 0  # Index of the current frame
        self.last_update = pg.time.get_ticks()  # Time when the frame was last updated
        self.scale = scale  # Scaling factor for the frames

        # Load all frames from the folder
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png") or filename.endswith(".PNG"):  # Ensure only PNG files are loaded
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
