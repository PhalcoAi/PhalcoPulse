# File: examples/rotating_cube.py

# Import the engine and scene base class from your new package
from phalcopulse.studio.application import *
from phalcopulse.studio.scene import *


class RotatingCubeScene(PhalcoPulseFX):
    """A clean example scene that draws a single, rotating white cube."""

    def setup(self):
        self.rotation_angle = 0

    def loop(self, delta_time):
        self.rotation_angle += 40 * delta_time  # Rotate 40 degrees per second
        glRotatef(self.rotation_angle, 0, 1, 0)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        # Front Face
        glNormal3f(0, 0, 1);
        glVertex3f(-0.5, -0.5, 0.5);
        glVertex3f(0.5, -0.5, 0.5);
        glVertex3f(0.5, 0.5, 0.5);
        glVertex3f(-0.5, 0.5, 0.5)
        # Back Face
        glNormal3f(0, 0, -1);
        glVertex3f(-0.5, -0.5, -0.5);
        glVertex3f(0.5, -0.5, -0.5);
        glVertex3f(0.5, 0.5, -0.5);
        glVertex3f(-0.5, 0.5, -0.5)
        # Top Face
        glNormal3f(0, 1, 0);
        glVertex3f(-0.5, 0.5, -0.5);
        glVertex3f(-0.5, 0.5, 0.5);
        glVertex3f(0.5, 0.5, 0.5);
        glVertex3f(0.5, 0.5, -0.5)
        # Bottom Face
        glNormal3f(0, -1, 0);
        glVertex3f(-0.5, -0.5, -0.5);
        glVertex3f(0.5, -0.5, -0.5);
        glVertex3f(0.5, -0.5, 0.5);
        glVertex3f(-0.5, -0.5, 0.5)
        # Right face
        glNormal3f(1, 0, 0);
        glVertex3f(0.5, -0.5, -0.5);
        glVertex3f(0.5, 0.5, -0.5);
        glVertex3f(0.5, 0.5, 0.5);
        glVertex3f(0.5, -0.5, 0.5)
        # Left Face
        glNormal3f(-1, 0, 0);
        glVertex3f(-0.5, -0.5, -0.5);
        glVertex3f(-0.5, -0.5, 0.5);
        glVertex3f(-0.5, 0.5, 0.5);
        glVertex3f(-0.5, 0.5, -0.5)
        glEnd()


if __name__ == '__main__':
    # Instantiate the example scene and the studio engine
    my_scene = RotatingCubeScene()
    studio = PhalcoPulseStudio(scene_fx=my_scene)

    # Run the main loop
    studio.run()
