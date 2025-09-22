from phalcopulse.studio.application import PhalcoPulseStudio
from phalcopulse.studio.scene import PhalcoPulseFX
from phalcopulse.graphics import objects as pgfx
from phalcopulse.graphics.mesh import Mesh


class MeshShowcase(PhalcoPulseFX):
    """
    A scene to demonstrate drawing a custom OBJ mesh.
    """

    def setup(self, ui_manager):
        self.mesh = Mesh("docs/bunny.obj", color=(0.9, 0.6, 0.3), scale=10.0)

    def loop(self, delta_time):
        pgfx.draw_plane(size=(10, 10), color=(0.4, 0.4, 0.4))

        # draw mesh
        self.mesh.draw()


if __name__ == '__main__':
    studio = PhalcoPulseStudio(scene_fx=MeshShowcase())
    studio.run()
