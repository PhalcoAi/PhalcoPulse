# File: examples/full_ui_showcase.py
from phalcopulse import PhalcoPulseStudio, PhalcoPulseFX, pgfx
from phalcopulse.ui import Label, Button, TextInput, ToggleSwitch, Slider, Checkbox
from phalcopulse.ui.widgets import ProgressBar, Dropdown


class FullUIShowcase(PhalcoPulseFX):
    def setup(self, ui_manager):
        self.is_rotating = True
        self.rotation_angle = 0
        self.cube_label = "My Cube"
        self.progress = 0.0

        # --- Callbacks ---
        def toggle_rotation(is_on): self.is_rotating = is_on

        def reset_scene():
            self.rotation_angle = 0
            status_label.text = "Cube Reset!"

        def set_cube_label(new_label):
            self.cube_label = new_label
            status_label.text = f"Label: {self.cube_label}"

        def set_rotation_speed(val): self.rotation_speed = val

        def toggle_wireframe(is_checked): self.wireframe = is_checked

        def dropdown_changed(option): status_label.text = f"Dropdown: {option}"

        # --- UI Widgets ---
        ui_manager.add_widget("title", Label((15, 200, 300, 20), "-- Full UI Showcase --", align='left'))

        ui_manager.add_widget("rotation_toggle", ToggleSwitch((15, 170, 50, 25), self.is_rotating, toggle_rotation))
        ui_manager.add_widget("toggle_label", Label((75, 172, 200, 20), "Toggle Rotation", align='left'))

        ui_manager.add_widget("label_input", TextInput((15, 130, 200, 30), self.cube_label, callback=set_cube_label))
        ui_manager.add_widget("reset_button", Button((230, 130, 100, 30), "Reset", reset_scene))

        ui_manager.add_widget("speed_slider", Slider((15, 90, 200, 20), "Speed", 10, 200, 40, set_rotation_speed))

        ui_manager.add_widget("wireframe_check", Checkbox((15, 60, 200, 20), "Wireframe", False, toggle_wireframe))

        ui_manager.add_widget("dropdown",
                              Dropdown((15, 30, 150, 25), ["Option A", "Option B", "Option C"], 0, dropdown_changed))

        self.progressbar = ui_manager.add_widget("progress", ProgressBar((230, 30, 150, 25), 0, 100, 0))

        status_label = ui_manager.add_widget("status_label",
                                             Label((15, 10, 300, 20), f"Label: {self.cube_label}", align='left'))

        # Scene vars
        self.rotation_speed = 40

    def loop(self, delta_time):
        if self.is_rotating:
            self.rotation_angle += self.rotation_speed * delta_time

        # Update progress bar continuously
        self.progress = (self.progress + 20 * delta_time) % 100
        self.progressbar.set_value(self.progress)

        pgfx.draw_cube(
            size=1.5,
            color=(0.2, 0.7, 0.3),
            center=(0, 1, 0),
            rotation=(0, self.rotation_angle, 0)
        )


if __name__ == '__main__':
    studio = PhalcoPulseStudio(scene_fx=FullUIShowcase())
    studio.run()
