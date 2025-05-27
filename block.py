from OpenGL.GL import *

# Описание вершин и граней куба
BLOCK_SCALE = 1.0  # Масштаб блока (можно изменить при необходимости)
CUBE_VERTICES = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),  # Перед
    (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, -1, 1)        # Зад
)
CUBE_FACES = (
    (0, 1, 2, 3),  # Перед
    (5, 4, 7, 6),  # Зад
    (0, 4, 5, 1),  # Право
    (3, 7, 6, 2),  # Лево
    (1, 5, 6, 2),  # Верх
    (4, 0, 3, 7)   # Низ
)

def draw_block(x, y, z, block_type):
    """Рендеринг блока с цветом в зависимости от типа."""
    glPushMatrix()
    glTranslatef(x * BLOCK_SCALE, y * BLOCK_SCALE, z * BLOCK_SCALE)
    
    if block_type == "grass":
        glColor3f(0, 1, 0)  # Зелёный для травы
    elif block_type == "dirt":
        glColor3f(0.5, 0.3, 0.1)  # Коричневый для земли
    else:
        glColor3f(0.5, 0.5, 0.5)  # Серый для неизвестного типа
    
    glBegin(GL_QUADS)
    for face in CUBE_FACES:
        for vertex in face:
            glVertex3fv(CUBE_VERTICES[vertex])
    glEnd()
    
    glPopMatrix()

def get_block_type(y, height):
    """Определяет тип блока по высоте."""
    return "grass" if y == height - 1 else "dirt"