from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


def _set_color(color):
    """A helper to set the OpenGL color."""
    if color:
        glColor3fv(color)


def draw_cube(size=1.0, color=(1, 1, 1), center=(0, 0, 0), rotation=(0, 0, 0)):
    """
    Draws a cube or cuboid.

    Args:
        size (float or tuple): The size of the cube. A float for a uniform cube,
                               or a tuple (width, height, depth) for a cuboid.
        color (tuple): The (R, G, B) color of the cube.
        center (tuple): The (x, y, z) center position of the cube.
    """
    if isinstance(size, (int, float)):
        sx, sy, sz = size / 2, size / 2, size / 2
    else:
        sx, sy, sz = size[0] / 2, size[1] / 2, size[2] / 2

    vertices = [
        (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz),  # Front
        (-sx, -sy, -sz), (-sx, sy, -sz), (sx, sy, -sz), (sx, -sy, -sz),  # Back
        (-sx, sy, -sz), (-sx, sy, sz), (sx, sy, sz), (sx, sy, -sz),  # Top
        (-sx, -sy, -sz), (sx, -sy, -sz), (sx, -sy, sz), (-sx, -sy, sz),  # Bottom
        (sx, -sy, -sz), (sx, sy, -sz), (sx, sy, sz), (sx, -sy, sz),  # Right
        (-sx, -sy, -sz), (-sx, -sy, sz), (-sx, sy, sz), (-sx, sy, -sz)  # Left
    ]

    normals = [
        (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)
    ]

    indices = [
        (0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15), (16, 17, 18, 19), (20, 21, 22, 23)
    ]

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
    """
    Draws a sphere.

    Args:
        radius (float): The radius of the sphere.
        color (tuple): The (R, G, B) color of the sphere.
        center (tuple): The (x, y, z) center position of the sphere.
        detail (int): The number of slices and stacks for sphere resolution.
    """
    glPushMatrix()
    glTranslatef(*center)
    _set_color(color)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, detail, detail)
    gluDeleteQuadric(quadric)
    glPopMatrix()


def draw_cylinder(radius=0.5, height=1.0, color=(1, 1, 1), center=(0, 0, 0), detail=32):
    """
    Draws a solid cylinder oriented along the Y-axis.

    Args:
        radius (float): The radius of the cylinder.
        height (float): The height of the cylinder.
        color (tuple): The (R, G, B) color of the cylinder.
        center (tuple): The (x, y, z) center position of the cylinder.
        detail (int): The resolution of the cylinder's circumference.
    """
    glPushMatrix()
    glTranslatef(center[0], center[1] - height / 2, center[2])  # Center the cylinder
    glRotatef(-90, 1, 0, 0)  # Orient along Y-axis
    _set_color(color)

    quadric = gluNewQuadric()
    # Bottom disk
    gluDisk(quadric, 0, radius, detail, 1)
    # Cylindrical body
    gluCylinder(quadric, radius, radius, height, detail, 1)
    # Top disk
    glTranslatef(0, 0, height)
    gluDisk(quadric, 0, radius, detail, 1)

    gluDeleteQuadric(quadric)
    glPopMatrix()


def draw_plane(size=(2.0, 2.0), color=(1, 1, 1), center=(0, 0, 0)):
    """
    Draws a simple plane on the XZ axis (a floor).

    Args:
        size (tuple): The (width, depth) of the plane.
        color (tuple): The (R, G, B) color of the plane.
        center (tuple): The (x, y, z) center position of the plane.
    """
    sx, sz = size[0] / 2, size[1] / 2

    glPushMatrix()
    glTranslatef(*center)
    _set_color(color)

    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)  # Normal pointing up
    glVertex3f(-sx, 0, -sz)
    glVertex3f(sx, 0, -sz)
    glVertex3f(sx, 0, sz)
    glVertex3f(-sx, 0, sz)
    glEnd()

    glPopMatrix()


def draw_triangle(v1, v2, v3, color=(1, 1, 1)):
    """
    Draws a single triangle from three vertices.

    Args:
        v1, v2, v3 (tuple): The three (x, y, z) vertices of the triangle.
        color (tuple): The (R, G, B) color of the triangle.
    """
    # Calculate normal for lighting
    vec1 = np.array(v2) - np.array(v1)
    vec2 = np.array(v3) - np.array(v1)
    normal = np.cross(vec1, vec2)
    normal /= np.linalg.norm(normal)

    _set_color(color)
    glBegin(GL_TRIANGLES)
    glNormal3fv(normal)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glVertex3fv(v3)
    glEnd()


def draw_face(v1, v2, v3, color1=(1, 1, 1), color2=(1, 1, 1), color3=(1, 1, 1)):
    """
    Draws a single triangle face with vertex colors.

    Args:
        v1, v2, v3 (tuple): The three (x, y, z) vertices of the triangle.
        color1, color2, color3 (tuple): The (R, G, B) colors for each vertex.
    """
    # Calculate normal for lighting
    vec1 = np.array(v2) - np.array(v1)
    vec2 = np.array(v3) - np.array(v1)
    normal = np.cross(vec1, vec2)
    normal /= np.linalg.norm(normal)

    glBegin(GL_TRIANGLES)
    glNormal3fv(normal)

    glColor3fv(color1)
    glVertex3fv(v1)

    glColor3fv(color2)
    glVertex3fv(v2)

    glColor3fv(color3)
    glVertex3fv(v3)

    glEnd()
