from phalcopulse.studio.application import PhalcoPulseStudio
from phalcopulse.studio.scene import PhalcoPulseFX
from phalcopulse.graphics import objects as pgfx


class ShapesShowcase(PhalcoPulseFX):
    """
    A scene to demonstrate drawing all the basic 3D shapes.
    """

    def setup(self, ui_manager):
        # No special setup needed for this static scene
        pass

    def loop(self, delta_time):
        # Draw a sphere at (-3, 1, 0)
        pgfx.draw_sphere(
            radius=0.7,
            color=(0.8, 0.2, 0.2),  # Red
            center=(-3, 1, 0)
        )

        # Draw a cube at the origin (0, 0.5, 0)
        pgfx.draw_cube(
            size=1.0,
            color=(0.2, 0.8, 0.2),  # Green
            center=(0, 0.5, 0)
        )

        # Draw a cylinder at (3, 1, 0) with height 2.0
        pgfx.draw_cylinder(
            start=(3, 0.0, 0),  # center.y - height/2
            end=(3, 2.0, 0),  # center.y + height/2
            radius=0.5,
            color=(0.2, 0.2, 0.8),  # Blue
            detail=32
        )

        # Draw a decorative triangle
        pgfx.draw_triangle(
            v1=(-2, 2.5, -2),
            v2=(0, 4, -2),
            v3=(2, 2.5, -2),
            color=(1, 1, 0)  # Yellow
        )

        # Draw a ground plane
        pgfx.draw_plane(
            size=(10, 10),
            color=(0.4, 0.4, 0.4)  # Gray
        )

        pgfx.draw_face(
            v1=(-2, 4.5, -2),
            v2=(0, 4, -2),
            v3=(2, 4.5, -2),
            color1=(1.0, 0.0, 0.0),  # Red
            color2=(0.0, 1.0, 0.0),  # Green
            color3=(0.0, 0.0, 1.0)  # Blue
        )


if __name__ == '__main__':
    studio = PhalcoPulseStudio(scene_fx=ShapesShowcase())
    studio.run()
