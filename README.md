# PhalcoPulse Engine

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/)

PhalcoPulse is a lightweight, real-time 3D visualization engine for Python, built on PyOpenGL. It is designed for the
rapid prototyping of scientific simulations, physics-based animations, interactive art, and educational tools.

The engine provides a clean scene-based architecture and a modern, interactive GUI overlay, allowing you to focus on
your simulation logic while the studio handles the rendering and user interaction.


![PhalcoPulse Demo](docs/PhalcoPulseStudio.gif)

---

## ✨ Key Features

* **Real-Time 3D Rendering:** Leverages the power and speed of PyOpenGL for smooth, interactive 3D graphics.
* **Interactive Camera:** Built-in mouse controls for orbit (rotate), pan, and zoom.
* **Modern GUI Overlay:** An elegant and customizable UI with interactive widgets like buttons and sliders to control
  your scene in real-time.
* **Extensible Scene Architecture:** Simply inherit from the `PhalcoPulseFX` class to define your own scenes, separating
  your logic from the engine's boilerplate.
* **Helpful Environment:** Comes with a dynamic, adaptive grid and reference axes that make 3D space intuitive to work
  with.

---

## ⚙️ Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:

* Python 3.8 or newer
* `pip` (Python's package installer)
* `git` (for cloning the repository)

### Installation Steps

It is highly recommended to install the package in a virtual environment to isolate project dependencies.

1. **Clone the Repository**
   Open your terminal and clone the project's source code:
   ```bash
   git clone https://github.com/PhalcoAi/PhalcoPulse
   cd PhalcoPulse
   ```

2. **Create and Activate a Virtual Environment**
   From the project's root directory, create and activate a new environment.
   ```bash
   # Create the environment
   python3 -m venv .venv

   # Activate it (on macOS and Linux)
   source .venv/bin/activate
   
   # On Windows, use: .venv\Scripts\activate
   ```

3. **Install the Package**
   Install `PhalcoPulse` in "editable" mode. The `-e` flag links the installation to the source code, so your changes
   are reflected immediately.
   ```bash
   pip install -e .
   ```

---

## 🚀 Quick Start Example

Creating a new visualization is simple. The following script creates a scene with a ball that bounces under gravity.
Save it in the `examples/` folder and run it.

```python
# File: examples/bouncing_ball.py

# Import the necessary classes from the PhalcoPulse package
from phalcopulse.studio.application import *
from phalcopulse.studio.scene import *


class BouncingBall(PhalcoPulseFX):
    """A scene demonstrating simple physics for a bouncing ball."""

    def setup(self):
        """Initialize the ball's properties and rendering object."""
        self.position = 3.0  # Initial height
        self.velocity = 0.0  # Initial velocity
        self.gravity = -9.8  # Gravity acceleration
        self.e = 0.85  # Coefficient of restitution (bounciness)

        # For efficiency, create the reusable quadric object once during setup.
        self.quadric = gluNewQuadric()

    def loop(self, delta_time):
        """Update physics and draw the ball each frame."""
        # 1. Update Physics
        if delta_time > 0:
            self.velocity += self.gravity * delta_time
            self.position += self.velocity * delta_time

            # Check for collision with the "floor" (at y=0.5, the sphere's radius)
            if self.position < 0.5:
                self.position = 0.5
                self.velocity = -self.velocity * self.e  # Reverse and dampen velocity

        # 2. Draw the Object
        glTranslatef(0, self.position, 0)
        glColor3f(0.2, 0.6, 1.0)  # A pleasant blue
        gluSphere(self.quadric, 0.5, 64, 64)  # Draw sphere with radius 0.5


if __name__ == '__main__':
    # Instantiate your custom scene
    my_scene = BouncingBall()

    # Pass the scene to the studio engine
    studio = PhalcoPulseStudio(scene_fx=my_scene)

    # Run the main application loop
    studio.run()
```

---

## 📦 Dependencies

The core dependencies are managed by `pip` during installation.

* **PyOpenGL**: The core OpenGL wrapper for Python.
* **Pygame (Community Edition)**: Used for window creation and event handling.
* **NumPy**: Used for various numerical calculations.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page of the repository.

## 📜 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.