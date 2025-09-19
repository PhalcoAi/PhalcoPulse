# File: phalcopulse/studio/camera.py

import copy
from OpenGL.GL import glTranslatef, glRotatef


class Camera:
    """Manages the 3D camera's state and user-input-based movement."""

    def __init__(self, position=[0.0, -1.0, -8], rotation=[15, -45]):
        self.translation = list(position)
        self.rotation = list(rotation)  # [pitch, yaw]
        self.initial_state = (copy.deepcopy(self.translation), copy.deepcopy(self.rotation))

        self.last_mouse_pos = None
        self.mouse_buttons = {'left': False, 'right': False}

    def reset(self):
        """Resets the camera to its initial position and rotation."""
        self.translation, self.rotation = copy.deepcopy(self.initial_state)

    def handle_mouse_move(self, pos, mouse_buttons):
        """Updates camera rotation or position based on mouse movement."""
        if self.last_mouse_pos is None:
            self.last_mouse_pos = pos
            return

        dx = pos[0] - self.last_mouse_pos[0]
        dy = pos[1] - self.last_mouse_pos[1]

        if mouse_buttons['left']:  # Rotate
            self.rotation[1] += dx * 0.2  # Yaw
            self.rotation[0] = max(-90, min(90, self.rotation[0] + dy * 0.2))  # Clamp pitch

        if mouse_buttons['right']:  # Pan
            pan_sensitivity = 0.002 * (abs(self.translation[2]) + 1)
            self.translation[0] += dx * pan_sensitivity
            self.translation[1] -= dy * pan_sensitivity

        self.last_mouse_pos = pos

    def handle_scroll(self, button):
        """Updates camera zoom based on mouse wheel scrolling."""
        zoom_sensitivity = 0.8 * (abs(self.translation[2]) * 0.1 + 1)
        if button == 4:  # Scroll up
            self.translation[2] += zoom_sensitivity
        elif button == 5:  # Scroll down
            self.translation[2] -= zoom_sensitivity

    def apply_transformations(self):
        """Applies the camera's transformations to the OpenGL matrix."""
        glTranslatef(*self.translation)
        glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
        glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
