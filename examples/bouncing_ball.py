# File: examples/bouncing_ball.py

from phalcopulse import PhalcoPulseStudio, PhalcoPulseFX, pgfx
from phalcopulse.ui import Label, Button, TextInput, ToggleSwitch


class BouncingBall(PhalcoPulseFX):
    """A clean example scene that draws a single, bouncing ball."""

    def setup(self):
        self.position = 2.0  # Initial height
        self.velocity = 0.5  # Initial upward velocity
        self.gravity = -0.98  # Gravity acceleration
        self.e = 0.95  # Coefficient of restitution

    def loop(self, delta_time):
        # Update position and velocity
        self.velocity += self.gravity * delta_time
        self.position += self.velocity * delta_time

        # Bounce off the ground
        if self.position < 0.5:
            self.position = 0.5
            self.velocity = -self.velocity * self.e

        pgfx.draw_sphere(
            radius=0.5,
            color=(0.2, 0.6, 0.9),
            center=(0, self.position, 0)
        )


if __name__ == '__main__':
    # Instantiate the example scene and the studio engine
    my_scene = BouncingBall()
    studio = PhalcoPulseStudio(scene_fx=my_scene)

    # Run the main loop
    studio.run()
