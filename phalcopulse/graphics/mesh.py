import os
from OpenGL.GL import *


class Mesh:
    """
    Load and render a mesh from an OBJ file with support for normals and lighting.
    """

    def __init__(self, file_path, color=(0.8, 0.8, 0.8)):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"OBJ file not found: {file_path}")

        self.vertices = []
        self.normals = []
        self.faces = []
        self.color = color

        self._load_obj(file_path)

    def _load_obj(self, file_path):
        with open(file_path, "r") as f:
            for line in f:
                if line.startswith("v "):
                    parts = line.strip().split()
                    self.vertices.append(tuple(map(float, parts[1:4])))
                elif line.startswith("vn "):
                    parts = line.strip().split()
                    self.normals.append(tuple(map(float, parts[1:4])))
                elif line.startswith("f "):
                    parts = line.strip().split()[1:]
                    face = []
                    for p in parts:
                        v_idx, t_idx, n_idx = (p.split("/") + [None, None])[:3]
                        v_idx = int(v_idx) - 1 if v_idx else None
                        n_idx = int(n_idx) - 1 if n_idx else None
                        face.append((v_idx, n_idx))
                    self.faces.append(face)

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for v_idx, n_idx in face:
                if n_idx is not None and n_idx < len(self.normals):
                    glNormal3fv(self.normals[n_idx])
                if v_idx is not None and v_idx < len(self.vertices):
                    glVertex3fv(self.vertices[v_idx])
        glEnd()
