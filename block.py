from OpenGL.GL import *
import numpy as np

class Block:
    BLOCK_TYPES = {
        "grass": (0.0, 1.0, 0.0),
        "dirt": (0.5, 0.3, 0.1),
        "stone": (0.5, 0.5, 0.5)
    }
    VERTICES = (
        (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
        (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, -1, 1)
    )
    FACES = (
        (0, 1, 2, 3), (5, 4, 7, 6), (0, 4, 5, 1),
        (3, 7, 6, 2), (1, 5, 6, 2), (4, 0, 3, 7)
    )

    def __init__(self, block_type):
        self.type = block_type
        self.color = self.BLOCK_TYPES.get(block_type, (0.5, 0.5, 0.5))

    @staticmethod
    def get_vertex_data():
        vertex_data = []
        for face in Block.FACES:
            for vertex in face:
                vertex_data.extend(Block.VERTICES[vertex])
        return vertex_data

    def get_color(self):
        return self.color