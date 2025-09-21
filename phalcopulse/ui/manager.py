# File: phalcopulse/ui/manager.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from . import drawing


class UIManager:
    """Manages a collection of UI widgets."""

    def __init__(self, app):
        self.app = app
        self.widgets = {}
        self.is_mouse_over_ui = False

    def add_widget(self, name, widget):
        """Add a new, named widget to the UI."""
        self.widgets[name] = widget
        return widget

    def handle_event(self, event):
        """Pass an event to all widgets and check for hover state."""
        pygame_mouse_pos = pygame.mouse.get_pos()
        gl_mouse_pos = (pygame_mouse_pos[0], self.app.display[1] - pygame_mouse_pos[1])

        self.is_mouse_over_ui = False

        for widget in self.widgets.values():
            widget.handle_event(event, gl_mouse_pos)
            if widget.is_hovered:
                self.is_mouse_over_ui = True

    def draw(self):
        """Draw all widgets and info panels."""
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glMatrixMode(GL_PROJECTION);
        glPushMatrix();
        glLoadIdentity()
        gluOrtho2D(0, self.app.display[0], 0, self.app.display[1])
        glMatrixMode(GL_MODELVIEW);
        glPushMatrix();
        glLoadIdentity()
        glDisable(GL_LIGHTING);
        glDisable(GL_DEPTH_TEST)

        drawing.draw_panels(self.app)

        for widget in self.widgets.values():
            widget.draw(self.app)

        drawing.draw_info_panel(self.app)

        glMatrixMode(GL_PROJECTION);
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW);
        glPopMatrix()
        glPopAttrib()
