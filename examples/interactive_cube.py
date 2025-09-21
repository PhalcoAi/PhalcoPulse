# File: examples/folding_cubes.py
"""
3D Folding Cube Showcase

- Draws cubes at each vertex of a 2D fractal-like array (lsq) to form a 3D structure.
- Slider controls "fold" amount: 0.0 = flat, 1.0 = full height.
- Uses UI widgets (Label, Slider, ToggleSwitch, Button) to control behavior.
"""

import numpy as np
from phalcopulse import PhalcoPulseStudio, PhalcoPulseFX, pgfx
from phalcopulse.ui import Label, Slider, ToggleSwitch, Button


def make_lsq(iterations=2, d=2):
    """Construct a fractal height array."""
    lsq = np.eye(d, dtype=float)
    for _ in range(iterations):
        lsq = d * np.kron(lsq, np.ones((d, d))) + np.kron(np.ones_like(lsq), np.eye(d))
    return lsq


class FoldingCubes(PhalcoPulseFX):
    def __init__(self, iterations=2, d=2):
        super().__init__()
        self.lsq = make_lsq(iterations=iterations, d=d)
        self.m, self.n = self.lsq.shape

        self.is_rotating = False
        self.rotation_angle = 0.0
        self.fold = 1.0
        self.cube_scale = 0.6

        # normalize heights for better scaling
        self.norm_heights = self.lsq.astype(float)

    def setup(self, ui_manager):
        # Toggle rotation
        ui_manager.add_widget("rotation_toggle",
                              ToggleSwitch(rect=(15, 165, 50, 25), is_on=self.is_rotating,
                                           callback=lambda val: setattr(self, "is_rotating", val)))
        ui_manager.add_widget("toggle_label",
                              Label(rect=(75, 167, 220, 20), text="Rotate Scene", align='left'))

        # Fold slider
        ui_manager.add_widget("fold_slider",
                              Slider(rect=(15, 130, 260, 18), label="Fold Amount",
                                     min_val=0.0, max_val=1.0, initial_val=self.fold,
                                     callback=lambda val: setattr(self, "fold", val)))

        # Cube scale slider
        ui_manager.add_widget("scale_slider",
                              Slider(rect=(15, 96, 260, 18), label="Cube Scale",
                                     min_val=0.1, max_val=1.2, initial_val=self.cube_scale,
                                     callback=lambda val: setattr(self, "cube_scale", val)))

        # Reset button
        def reset_scene():
            self.rotation_angle = 0.0
            self.fold = 1.0
            self.cube_scale = 0.6

        ui_manager.add_widget("reset_button",
                              Button(rect=(15, 30, 120, 28), text="Reset", callback=reset_scene))

        # Status label
        ui_manager.add_widget("status_label",
                              Label(rect=(15, 8, 400, 18), text="Folding Cubes", align='left'))

    def loop(self, delta_time):
        if self.is_rotating:
            self.rotation_angle = (self.rotation_angle + 20.0 * delta_time) % 360.0

        # scale factor for height
        heights = self.norm_heights * self.fold
        for i in range(self.m):
            for j in range(self.n):
                h = float(heights[i, j])
                center = (i - self.m / 2, h, j - self.n / 2)
                # simple coloring making chess patter
                color = ((i + j) % 2, (i + j) % 2, (i + j) % 2)
                rotation = (0.0, self.rotation_angle, 0.0)
                size = self.cube_scale
                pgfx.draw_cube(size=size, color=color, center=center, rotation=rotation)

        # update status label
        try:
            ui_status = self.scene_manager.ui_manager.get_widget("status_label")
            ui_status.text = f"Fold: {self.fold:.2f}, Scale: {self.cube_scale:.2f}"
        except Exception:
            pass


if __name__ == "__main__":
    studio = PhalcoPulseStudio(scene_fx=FoldingCubes(iterations=3, d=2))
    studio.run()
