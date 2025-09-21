import pygame
from OpenGL.GL import *
from phalcopulse.studio.application import PhalcoPulseStudio
from phalcopulse.studio.scene import PhalcoPulseFX
from phalcopulse.ui.widgets import Button, Slider


class InteractiveCube(PhalcoPulseFX):
    def setup(self, ui_manager):
        # Scene state
        self.rotation_angle = 0
        self.rotation_speed = 40.0
        self.cube_color = [1.0, 0.55, 0.0]

        # ---- Define callback functions ----
        def reset_rotation():
            """A function to reset the cube's angle."""
            self.rotation_angle = 0

        def change_color_to_blue():
            """A function to change the cube's color."""
            self.cube_color = [0.2, 0.6, 1.0]

        def update_speed(new_speed):
            """A function to be called by the slider."""
            self.rotation_speed = new_speed

        # ---- Add NAMED widgets to the UI Manager ----
        # The first argument is now a unique string name for the widget.
        ui_manager.add_widget("reset_button",
                              Button(rect=(15, 115, 150, 35), text="Reset Rotation", callback=reset_rotation))
        ui_manager.add_widget("color_button",
                              Button(rect=(180, 115, 150, 35), text="Change Color", callback=change_color_to_blue))
        ui_manager.add_widget("speed_slider_custom",
                              Slider(rect=(15, 170, 315, 20), label="Rotation Speed", min_val=0, max_val=200,
                                     initial_val=self.rotation_speed, callback=update_speed))

    def loop(self, delta_time):
        self.rotation_angle += self.rotation_speed * delta_time

        glRotatef(self.rotation_angle, 0, 1, 0)
        glColor3fv(self.cube_color)

        # Draw a 1x1x1 cube
        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1);
        glVertex3f(-0.5, -0.5, 0.5);
        glVertex3f(0.5, -0.5, 0.5);
        glVertex3f(0.5, 0.5, 0.5);
        glVertex3f(-0.5, 0.5, 0.5)
        glNormal3f(0, 0, -1);
        glVertex3f(-0.5, -0.5, -0.5);
        glVertex3f(0.5, -0.5, -0.5);
        glVertex3f(0.5, 0.5, -0.5);
        glVertex3f(-0.5, 0.5, -0.5)
        glNormal3f(0, 1, 0);
        glVertex3f(-0.5, 0.5, -0.5);
        glVertex3f(-0.5, 0.5, 0.5);
        glVertex3f(0.5, 0.5, 0.5);
        glVertex3f(0.5, 0.5, -0.5)
        glNormal3f(0, -1, 0);
        glVertex3f(-0.5, -0.5, -0.5);
        glVertex3f(0.5, -0.5, -0.5);
        glVertex3f(0.5, -0.5, 0.5);
        glVertex3f(-0.5, -0.5, 0.5)
        glNormal3f(1, 0, 0);
        glVertex3f(0.5, -0.5, -0.5);
        glVertex3f(0.5, 0.5, -0.5);
        glVertex3f(0.5, 0.5, 0.5);
        glVertex3f(0.5, -0.5, 0.5)
        glNormal3f(-1, 0, 0);
        glVertex3f(-0.5, -0.5, -0.5);
        glVertex3f(-0.5, -0.5, 0.5);
        glVertex3f(-0.5, 0.5, 0.5);
        glVertex3f(-0.5, 0.5, -0.5)
        glEnd()


if __name__ == '__main__':
    studio = PhalcoPulseStudio(scene_fx=InteractiveCube())
    studio.run()
