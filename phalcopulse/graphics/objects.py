from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math


def _set_color(color):
    """A helper to set the OpenGL color."""
    if color:
        glColor3fv(color)


def draw_cube(size=1.0, color=(1, 1, 1), center=(0, 0, 0), rotation=(0, 0, 0)):
    # ... (this function is unchanged) ...
    if isinstance(size, (int, float)):
        sx, sy, sz = size / 2, size / 2, size / 2
    else:
        sx, sy, sz = size[0] / 2, size[1] / 2, size[2] / 2
    vertices = [
        (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz),
        (-sx, -sy, -sz), (-sx, sy, -sz), (sx, sy, -sz), (sx, -sy, -sz),
        (-sx, sy, -sz), (-sx, sy, sz), (sx, sy, sz), (sx, sy, -sz),
        (-sx, -sy, -sz), (sx, -sy, -sz), (sx, -sy, sz), (-sx, -sy, sz),
        (sx, -sy, -sz), (sx, sy, -sz), (sx, sy, sz), (sx, -sy, sz),
        (-sx, -sy, -sz), (-sx, -sy, sz), (-sx, sy, sz), (-sx, sy, -sz)
    ]
    normals = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    indices = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15), (16, 17, 18, 19), (20, 21, 22, 23)]
    glPushMatrix()
    glRotatef(rotation[0], 1, 0, 0)
    glRotatef(rotation[1], 0, 1, 0)
    glRotatef(rotation[2], 0, 0, 1)
    glTranslatef(*center)
    _set_color(color)
    for i, face in enumerate(indices):
        glBegin(GL_QUADS)
        glNormal3fv(normals[i])
        for vertex_index in face:
            glVertex3fv(vertices[vertex_index])
        glEnd()
    glPopMatrix()


def draw_sphere(radius=0.5, color=(1, 1, 1), center=(0, 0, 0), detail=32):
    # ... (this function is unchanged) ...
    glPushMatrix()
    glTranslatef(*center)
    _set_color(color)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, detail, detail)
    gluDeleteQuadric(quadric)
    glPopMatrix()


def draw_plane(size=(2.0, 2.0), color=(1, 1, 1), center=(0, 0, 0)):
    # ... (this function is unchanged, assumes Z-up) ...
    sx, sy = size[0] / 2, size[1] / 2
    glPushMatrix()
    glTranslatef(*center)
    _set_color(color)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)  # Normal pointing up in Z
    glVertex3f(-sx, -sy, 0)
    glVertex3f(sx, -sy, 0)
    glVertex3f(sx, sy, 0)
    glVertex3f(-sx, sy, 0)
    glEnd()
    glPopMatrix()


def draw_triangle(v1, v2, v3, color=(1, 1, 1)):
    # ... (this function is unchanged) ...
    vec1 = np.array(v2) - np.array(v1)
    vec2 = np.array(v3) - np.array(v1)
    normal = np.cross(vec1, vec2)
    norm_len = np.linalg.norm(normal)
    if norm_len > 0: normal /= norm_len
    _set_color(color)
    glBegin(GL_TRIANGLES)
    glNormal3fv(normal)
    glVertex3fv(v1);
    glVertex3fv(v2);
    glVertex3fv(v3)
    glEnd()


def draw_face(v1, v2, v3, color1, color2, color3):
    """
    Draws a single triangle with a different color for each vertex.
    OpenGL will interpolate the colors across the face (Gouraud shading).
    """
    # Calculate a single normal for the whole face for lighting purposes
    vec1 = np.array(v2) - np.array(v1)
    vec2 = np.array(v3) - np.array(v1)
    normal = np.cross(vec1, vec2)
    norm_len = np.linalg.norm(normal)
    if norm_len > 0: normal /= norm_len

    glBegin(GL_TRIANGLES)
    glNormal3fv(normal)
    # Set color, then vertex, for each point
    glColor3fv(color1);
    glVertex3fv(v1)
    glColor3fv(color2);
    glVertex3fv(v2)
    glColor3fv(color3);
    glVertex3fv(v3)
    glEnd()


def draw_cylinder(start, end, radius=0.5, color=(1, 1, 1), detail=16):
    """
    Draws a solid cylinder between two points in 3D.

    Args:
        start (tuple or np.ndarray): The (x, y, z) start point.
        end (tuple or np.ndarray): The (x, y, z) end point.
        radius (float): Cylinder radius.
        color (tuple): RGB color.
        detail (int): Number of segments for smoothness.
    """
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)  # ✅ removed the minus
    direction = end - start
    height = np.linalg.norm(direction)
    if height == 0:
        return  # Avoid zero-length cylinder

    # Normalize direction
    direction /= height

    # Compute rotation axis/angle from cylinder's default +z to direction
    z_axis = np.array([0, 0, 1])  # ✅ gluCylinder is along Z
    axis = np.cross(z_axis, direction)
    angle = np.degrees(np.arccos(np.clip(np.dot(z_axis, direction), -1.0, 1.0)))

    glPushMatrix()
    glTranslatef(*start)
    if np.linalg.norm(axis) > 1e-6:
        glRotatef(angle, *axis)

    glColor3fv(color)
    quadric = gluNewQuadric()

    # Draw cylinder body
    gluCylinder(quadric, radius, radius, height, detail, 1)

    # Draw bottom disk
    glPushMatrix()
    glRotatef(180, 1, 0, 0)  # flip to cover the base
    gluDisk(quadric, 0, radius, detail, 1)
    glPopMatrix()

    # Draw top disk
    glTranslatef(0, 0, height)
    gluDisk(quadric, 0, radius, detail, 1)

    gluDeleteQuadric(quadric)
    glPopMatrix()
