from perlin_noise import PerlinNoise
from block import Block
from constants import CHUNK_SIZE, BLOCK_SCALE
import numpy as np
from OpenGL.GL import *

class Chunk:
    def __init__(self, chunk_x, chunk_z):
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.blocks = {}
        self.vao = None
        self.vbo = None
        self.vertex_count = 0
        print(f"Creating chunk ({chunk_x}, {chunk_z})")
        self.generate()

    def generate(self):
        """Генерация чанка с использованием шума Перлина."""
        noise = PerlinNoise(octaves=2, seed=42)
        scale = 0.1
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                world_x = self.chunk_x * CHUNK_SIZE + x
                world_z = self.chunk_z * CHUNK_SIZE + z
                height = int(noise([world_x * scale, world_z * scale]) * 5 + 5)
                for y in range(height):
                    block_type = "grass" if y == height - 1 else "dirt"
                    self.blocks[(x, y, z)] = Block(block_type)
        self.setup_vbo()

    def setup_vbo(self):
        """Создание VAO и VBO для рендеринга."""
        vertex_data = []
        color_data = []
        for (x, y, z), block in self.blocks.items():
            block_vertices = Block.get_vertex_data()
            for i in range(0, len(block_vertices), 3):
                vertex_data.extend([
                    block_vertices[i] + x * BLOCK_SCALE,
                    block_vertices[i + 1] + y * BLOCK_SCALE,
                    block_vertices[i + 2] + z * BLOCK_SCALE
                ])
                color_data.extend(block.get_color())
        
        self.vertex_count = len(vertex_data) // 3
        vertex_data = np.array(vertex_data, dtype=np.float32)
        color_data = np.array(color_data, dtype=np.float32)
        
        # Создание VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        # Создание VBO
        self.vbo = glGenBuffers(2)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
        glBufferData(GL_ARRAY_BUFFER, color_data.nbytes, color_data, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self, shader_program):
        """Рендеринг чанка с использованием шейдера."""
        if not self.vao or not self.vbo:
            print(f"Chunk ({self.chunk_x}, {self.chunk_z}) not initialized properly")
            return
        
        glUseProgram(shader_program)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, self.vertex_count)
        glBindVertexArray(0)
        glUseProgram(0)

    def cleanup(self):
        """Очистка ресурсов чанка."""
        if self.vbo:
            glDeleteBuffers(2, self.vbo)
            self.vbo = None
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            self.vao = None