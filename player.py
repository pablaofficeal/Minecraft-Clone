import numpy as np
from constants import *

class Player:
    def __init__(self):
        self.pos = [WORLD_SIZE / 2, 10, WORLD_SIZE / 2]
        self.angle = [0, 0]
        self.last_mouse_pos = None

    def update(self, window):
        import glfw
        if self.last_mouse_pos is None:
            self.last_mouse_pos = glfw.get_cursor_pos(window)
        
        mouse_pos = glfw.get_cursor_pos(window)
        mouse_dx = mouse_pos[0] - self.last_mouse_pos[0]
        mouse_dy = mouse_pos[1] - self.last_mouse_pos[1]
        self.last_mouse_pos = mouse_pos
        
        self.angle[0] += mouse_dx * MOUSE_SENSITIVITY
        self.angle[1] = max(min(self.angle[1] - mouse_dy * MOUSE_SENSITIVITY, 90), -90)

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

    def get_view_matrix(self):
        view = np.identity(4, dtype=np.float32)
        view = np.dot(view, np.array([
            [1, 0, 0, -self.pos[0]],
            [0, 1, 0, -self.pos[1]],
            [0, 0, 1, -self.pos[2]],
            [0, 0, 0, 1]
        ], dtype=np.float32))
        view = np.dot(view, np.array([
            [np.cos(np.radians(self.angle[0])), 0, np.sin(np.radians(self.angle[0])), 0],
            [0, 1, 0, 0],
            [-np.sin(np.radians(self.angle[0])), 0, np.cos(np.radians(self.angle[0])), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32))
        view = np.dot(view, np.array([
            [1, 0, 0, 0],
            [0, np.cos(np.radians(self.angle[1])), -np.sin(np.radians(self.angle[1])), 0],
            [0, np.sin(np.radians(self.angle[1])), np.cos(np.radians(self.angle[1])), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32))
        return view