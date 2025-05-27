from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Menu:
    def __init__(self):
        self.buttons = [
            {"text": "Play", "x": SCREEN_WIDTH//2 - 100, "y": SCREEN_HEIGHT//2 - 50, "w": 200, "h": 50},
            {"text": "Settings", "x": SCREEN_WIDTH//2 - 100, "y": SCREEN_HEIGHT//2 + 20, "w": 200, "h": 50},
            {"text": "Exit", "x": SCREEN_WIDTH//2 - 100, "y": SCREEN_HEIGHT//2 + 90, "w": 200, "h": 50},
        ]
        self.state = "main"  # "main" или "settings"

    def draw_text(self, x, y, text):
        """Рендеринг простого текста (заглушка)."""
        glRasterPos2f(x, y)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    def render(self):
        """Рендеринг меню."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.state == "main":
            # Рендеринг кнопок
            for button in self.buttons:
                x, y, w, h = button["x"], button["y"], button["w"], button["h"]
                # Фон кнопки
                glColor3f(0.5, 0.5, 0.5)  # Серый фон
                glBegin(GL_QUADS)
                glVertex2f(x, y)
                glVertex2f(x + w, y)
                glVertex2f(x + w, y + h)
                glVertex2f(x, y + h)
                glEnd()
                # Текст кнопки
                glColor3f(1, 1, 1)  # Белый текст
                self.draw_text(x + 20, y + 35, button["text"])
        elif self.state == "settings":
            # Заглушка для настроек
            glColor3f(1, 1, 1)
            self.draw_text(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, "Settings: Work in Progress")

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