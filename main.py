import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from world import generate_world, render_world
from player import Player
from constants import *

def main():
    # Инициализация GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        return
    
    # Создание окна (убираем версию OpenGL)
    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Minecraft Clone", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    # Настройка OpenGL
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Вывод версии OpenGL для диагностики
    print("OpenGL Version:", glGetString(GL_VERSION).decode('utf-8'))
    
    # Скрыть курсор и захватить его
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    # Инициализация мира и игрока
    world = generate_world()
    player = Player()
    
    # Главный цикл
    while not glfw.window_should_close(window):
        # Обработка ввода
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        # Обновление игрока
        player.update(window)
        
        # Очистка экрана
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Настройка камеры и рендеринг
        player.apply_camera()
        render_world(world)
        
        # Обновление окна
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    # Завершение
    glfw.terminate()

if __name__ == "__main__":
    main()