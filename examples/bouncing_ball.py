# File: examples/bouncing_ball.py

# Import the engine and scene base class from your new package
from phalcopulse.studio.application import *
from phalcopulse.studio.scene import *


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

        glTranslatef(0, self.position, 0)
        glColor3f(0.2, 0.6, 1.0)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.5, 32, 32)
        gluDeleteQuadric(quadric)


if __name__ == '__main__':
    # Instantiate the example scene and the studio engine
    my_scene = BouncingBall()
    studio = PhalcoPulseStudio(scene_fx=my_scene)

    # Run the main loop
    studio.run()
