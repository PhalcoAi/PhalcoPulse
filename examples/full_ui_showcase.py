# File: examples/full_ui_showcase.py

from OpenGL.GL import *
from phalcopulse.studio.application import PhalcoPulseStudio
from phalcopulse.studio.scene import PhalcoPulseFX
from phalcopulse.ui.widgets import Label, Button, TextInput, ToggleSwitch


class FullUIShowcase(PhalcoPulseFX):
    def setup(self, ui_manager):
        # Scene state
        self.is_rotating = True
        self.rotation_angle = 0
        self.cube_label = "My Cube"

        # --- Define callbacks ---
        def toggle_rotation(is_on):
            self.is_rotating = is_on

        def reset_scene():
            self.rotation_angle = 0
            # We can even update other widgets from a callback
            label_widget.text = "Cube Reset!"

        def set_cube_label(new_label):
            self.cube_label = new_label
            label_widget.text = f"Label: {self.cube_label}"

        # --- Add new widgets ---
        # Add a non-interactive title label
        ui_manager.add_widget("title_label", Label(rect=(15, 120, 300, 20), text="-- Custom Widgets --", align='left'))

        # Add a toggle switch to control rotation
        ui_manager.add_widget("rotation_toggle",
                              ToggleSwitch(rect=(15, 80, 50, 25), is_on=self.is_rotating, callback=toggle_rotation))
        ui_manager.add_widget("toggle_label", Label(rect=(75, 82, 200, 20), text="Toggle Rotation", align='left'))

        # Add a text input to change the cube's label
        ui_manager.add_widget("label_input",
                              TextInput(rect=(15, 40, 200, 30), initial_text=self.cube_label, callback=set_cube_label))

        # Add a button to reset the scene
        ui_manager.add_widget("reset_button", Button(rect=(230, 40, 100, 30), text="Reset", callback=reset_scene))

        # Add a label that can be updated by other widgets
        label_widget = ui_manager.add_widget("status_label",
                                             Label(rect=(15, 15, 300, 20), text=f"Label: {self.cube_label}",
                                                   align='left'))

    def loop(self, delta_time):
        if self.is_rotating:
            self.rotation_angle += 40 * delta_time

        glRotatef(self.rotation_angle, 0, 1, 0)
        glColor3f(1.0, 0.55, 0.0)  # Orange

        # Draw a 1x1x1 cube
        glBegin(GL_QUADS)
        # ... (Vertex data for cube) ...
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
    studio = PhalcoPulseStudio(scene_fx=FullUIShowcase())
    studio.run()
