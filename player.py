import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from constants import *

class Player:
    def __init__(self):
        self.pos = [WORLD_SIZE / 2, 10, WORLD_SIZE / 2]
        self.angle = [0, 0]  # Углы: yaw (x), pitch (y)
        self.last_mouse_pos = None

    def update(self, window):
        """Обновление позиции и углов игрока."""
        import glfw
        if self.last_mouse_pos is None:
            self.last_mouse_pos = glfw.get_cursor_pos(window)
        
        # Получаем движение мыши
        mouse_pos = glfw.get_cursor_pos(window)
        mouse_dx = mouse_pos[0] - self.last_mouse_pos[0]
        mouse_dy = mouse_pos[1] - self.last_mouse_pos[1]
        self.last_mouse_pos = mouse_pos
        
        self.angle[0] += mouse_dx * MOUSE_SENSITIVITY
        self.angle[1] = max(min(self.angle[1] - mouse_dy * MOUSE_SENSITIVITY, 90), -90)

        # Управление клавишами
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.pos[0] -= np.sin(np.radians(self.angle[0])) * PLAYER_SPEED
            self.pos[2] += np.cos(np.radians(self.angle[0])) * PLAYER_SPEED
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.pos[0] += np.sin(np.radians(self.angle[0])) * PLAYER_SPEED
            self.pos[2] -= np.cos(np.radians(self.angle[0])) * PLAYER_SPEED
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.pos[0] -= np.cos(np.radians(self.angle[0])) * PLAYER_SPEED
            self.pos[2] -= np.sin(np.radians(self.angle[0])) * PLAYER_SPEED
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.pos[0] += np.cos(np.radians(self.angle[0])) * PLAYER_SPEED
            self.pos[2] += np.sin(np.radians(self.angle[0])) * PLAYER_SPEED

    def apply_camera(self):
        """Настройка камеры от лица игрока."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, SCREEN_WIDTH / SCREEN_HEIGHT, NEAR_PLANE, FAR_PLANE)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(self.angle[1], 1, 0, 0)
        glRotatef(self.angle[0], 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])