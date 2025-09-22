from phalcopulse.studio.application import PhalcoPulseStudio
from phalcopulse.studio.scene import PhalcoPulseFX
from phalcopulse.graphics import objects as pgfx


class ShapesShowcase(PhalcoPulseFX):
    """
    A scene to demonstrate drawing all the basic 3D shapes
    in a clean, aesthetic arrangement.
    """

    def setup(self, ui_manager):
        pass

    def loop(self, delta_time):
        # Ground stage
        pgfx.draw_plane(
            size=(12, 12),
            color=(0.35, 0.35, 0.35)
        )

        # Sphere (left, floating slightly)
        pgfx.draw_sphere(
            radius=0.8,
            color=(0.85, 0.2, 0.2),  # Red
            center=(-3.0, 0.8, 2.0)
        )

        # Cube (center, slightly lifted)
        pgfx.draw_cube(
            size=1.2,
            color=(0.2, 0.8, 0.3),  # Green
            center=(0.0, 0.6, 2.0)
        )

        # Cylinder (right, upright)
        pgfx.draw_cylinder(
            start=(3.0, 0.0, 0.0),
            end=(3.0, 2.0, 2.0),
            radius=0.5,
            color=(0.2, 0.3, 0.9),  # Blue
            detail=32
        )

        # Triangle panel (front left)
        pgfx.draw_triangle(
            v1=(-2, 0.01, 3),
            v2=(0, 0.01, 1.5),
            v3=(-4, 0.01, 1.5),
            color=(1.0, 1.0, 0.0)  # Yellow
        )

        # Gradient face (front right, elevated)
        pgfx.draw_face(
            v1=(2, 1.5, 2),
            v2=(4, 1.0, 2),
            v3=(3, 2.5, 2),
            color1=(1.0, 0.0, 0.0),  # Red
            color2=(0.0, 1.0, 0.0),  # Green
            color3=(0.0, 0.0, 1.0)  # Blue
        )


if __name__ == '__main__':
    studio = PhalcoPulseStudio(scene_fx=ShapesShowcase())
    studio.run()
