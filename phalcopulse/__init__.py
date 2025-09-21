# This file makes the main classes and functions available at the top level.

# Promote the main application and scene classes from the 'studio' sub-package
from .studio.application import PhalcoPulseStudio
from .studio.scene import PhalcoPulseFX

# Promote the Mesh class from the 'graphics' sub-package
from .graphics.mesh import Mesh

# Make the primitive drawing functions available as 'phalcopulse.pgfx'
from .graphics import objects as pgfx
