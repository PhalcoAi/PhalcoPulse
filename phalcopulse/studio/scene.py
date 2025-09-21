# File: phalcopulse/studio/scene.py

class PhalcoPulseFX:
    """
    Base class for creating PhalcoPulse visual effects (FX).
    Users should inherit from this class and override the setup() and loop()
    methods to create their custom 3D scenes.
    """

    def setup(self, ui_manager):
        """Called once at the beginning to initialize the scene."""
        pass

    def loop(self, delta_time):
        """
        Called every frame to update and draw the scene.
        Args:
            delta_time (float): The frame-rate independent time step.
        """
        pass
