from hunk import Chunk
from constants import RENDER_DISTANCE, CHUNK_SIZE
from OpenGL.GL import *
import numpy as np

class World:
    def __init__(self):
        self.chunks = {}
        self.shader_program = None

    def generate_chunks(self, player_pos):
        """Генерация и выгрузка чанков вокруг игрока."""
        player_chunk_x = int(player_pos[0] // CHUNK_SIZE)
        player_chunk_z = int(player_pos[2] // CHUNK_SIZE)
        
        # Создаём новые чанки
        new_chunks = {}
        for cx in range(player_chunk_x - RENDER_DISTANCE, player_chunk_x + RENDER_DISTANCE + 1):
            for cz in range(player_chunk_z - RENDER_DISTANCE, player_chunk_z + RENDER_DISTANCE + 1):
                if (cx, cz) not in self.chunks:
                    print(f"Generating chunk ({cx}, {cz})")
                    new_chunks[(cx, cz)] = Chunk(cx, cz)
                else:
                    new_chunks[(cx, cz)] = self.chunks[(cx, cz)]
        
        # Выгружаем дальние чанки
        for (cx, cz), chunk in self.chunks.items():
            if abs(cx - player_chunk_x) > RENDER_DISTANCE or abs(cz - player_chunk_z) > RENDER_DISTANCE:
                print(f"Unloading chunk ({cx}, {cz})")
                chunk.cleanup()
        
        self.chunks = new_chunks

    def render(self, view_matrix, projection_matrix):
        """Рендеринг всех чанков."""
        glUseProgram(self.shader_program)
        
        model_loc = glGetUniformLocation(self.shader_program, "model")
        view_loc = glGetUniformLocation(self.shader_program, "view")
        proj_loc = glGetUniformLocation(self.shader_program, "projection")
        
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view_matrix)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection_matrix)
        
        for hunk in self.chunks.values():
            model = np.identity(4, dtype=np.float32)
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            hunk.render(self.shader_program)
        
        glUseProgram(0)