import pygame
import imageio
import numpy as np
from OpenGL.GL import *
from datetime import datetime
import os


def take_screenshot(display_size, filename=None):
    """Captures the current OpenGL buffer and saves it as a PNG."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"phalcopulse_capture_{timestamp}.png"

    # Ensure the 'captures' directory exists
    if not os.path.exists("captures"):
        os.makedirs("captures")
    filepath = os.path.join("captures", filename)

    viewport = glGetIntegerv(GL_VIEWPORT)
    width, height = viewport[2], viewport[3]

    glReadBuffer(GL_FRONT)
    pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)

    # Convert pixels to a Pygame surface
    surface = pygame.image.fromstring(pixels, (width, height), "RGB")
    # OpenGL and Pygame have inverted Y-axes
    surface = pygame.transform.flip(surface, False, True)

    pygame.image.save(surface, filepath)
    print(f"Screenshot saved to {filepath}")


class VideoRecorder:
    """Handles the process of recording frames to a video file."""

    def __init__(self, display_size, fps=30):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"phalcopulse_video_{timestamp}.mp4"

        if not os.path.exists("captures"):
            os.makedirs("captures")
        self.filepath = os.path.join("captures", filename)

        self.writer = imageio.get_writer(self.filepath, fps=fps, format='FFMPEG',
                                         codec='libx264', quality=8)
        self.is_recording = False
        print(f"Started recording to {self.filepath}")

    def start(self):
        self.is_recording = True

    def capture_frame(self):
        if not self.is_recording:
            return

        viewport = glGetIntegerv(GL_VIEWPORT)
        width, height = viewport[2], viewport[3]

        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)

        # Convert raw pixels to a NumPy array and flip vertically
        frame = np.frombuffer(pixels, dtype=np.uint8).reshape(height, width, 3)
        frame = np.flipud(frame)

        self.writer.append_data(frame)

    def stop(self):
        if self.is_recording:
            self.writer.close()
            self.is_recording = False
            print(f"Video saved to {self.filepath}")
