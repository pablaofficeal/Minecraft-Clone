from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import numpy as np
import ctypes

class Menu:
    def __init__(self):
        self.buttons = [
            {"text": "Play", "x": SCREEN_WIDTH//2 - 100, "y": SCREEN_HEIGHT//2 - 50, "w": 200, "h": 50},
            {"text": "Settings", "x": SCREEN_WIDTH//2 - 100, "y": SCREEN_HEIGHT//2 + 20, "w": 200, "h": 50},
            {"text": "Exit", "x": SCREEN_WIDTH//2 - 100, "y": SCREEN_HEIGHT//2 + 90, "w": 200, "h": 50},
        ]
        self.state = "main"
        self.shader_program = self.setup_shaders()
        self.vao = None
        self.vbo = None
        self.setup_buffers()

    def setup_shaders(self):
        """Создание шейдеров для 2D-рендеринга."""
        vertex_shader_source = """
        #version 330 core
        layout(location = 0) in vec2 aPos;
        void main() {
            gl_Position = vec4(aPos.x / %f - 1.0, 1.0 - aPos.y / %f, 0.0, 1.0);
        }
        """ % (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        fragment_shader_source = """
        #version 330 core
        out vec4 FragColor;
        uniform vec3 buttonColor;
        void main() {
            FragColor = vec4(buttonColor, 1.0);
        }
        """

        vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        shader_program = compileProgram(vertex_shader, fragment_shader)
        
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        
        return shader_program

    def setup_buffers(self):
        """Создание VAO и VBO для кнопок."""
        vertex_data = []
        for button in self.buttons:
            x, y, w, h = button["x"], button["y"], button["w"], button["h"]
            vertex_data.extend([
                x, y, x + w, y, x + w, y + h,
                x, y, x + w, y + h, x, y + h
            ])
        
        vertex_data = np.array(vertex_data, dtype=np.float32)
        
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        """Рендеринг меню."""
        glUseProgram(self.shader_program)
        
        glBindVertexArray(self.vao)
        
        for i, button in enumerate(self.buttons):
            if self.state == "main":
                glUniform3f(glGetUniformLocation(self.shader_program, "buttonColor"), 0.5, 0.5, 0.5)
                glDrawArrays(GL_TRIANGLES, i * 6, 6)
            elif self.state == "settings" and i == 0:
                glUniform3f(glGetUniformLocation(self.shader_program, "buttonColor"), 0.0, 0.0, 0.0)
                glDrawArrays(GL_TRIANGLES, 0, 6)
        
        glBindVertexArray(0)
        glUseProgram(0)

    def handle_click(self, x, y):
        """Обработка клика мыши."""
        if self.state == "main":
            for button in self.buttons:
                bx, by, bw, bh = button["x"], button["y"], button["w"], button["h"]
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    if button["text"] == "Play":
                        return "game"
                    elif button["text"] == "Settings":
                        self.state = "settings"
                    elif button["text"] == "Exit":
                        return "exit"
        return None