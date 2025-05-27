import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  # Для текста в меню
from world import generate_world, render_world
from player import Player
from menu import Menu
from constants import *

def main():
    # Инициализация GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        return
    
    # Инициализация GLUT для текста
    glutInit()

    # Создание окна
    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Minecraft Clone", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    # Настройка OpenGL
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Скрыть курсор и захватить его
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)  # Курсор видим в меню
    
    # Инициализация меню, мира и игрока
    menu = Menu()
    world = None
    player = None
    game_state = "menu"  # "menu" или "game"
    
    # Обработка клика мыши
    def mouse_button_callback(window, button, action, mods):
        nonlocal game_state, world, player
        if game_state == "menu" and button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            result = menu.handle_click(x, y)
            if result == "game":
                if world is None:
                    world = generate_world()
                    player = Player()
                game_state = "game"
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            elif result == "exit":
                glfw.set_window_should_close(window, True)
    
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    
    # Главный цикл
    while not glfw.window_should_close(window):
        # Обработка ввода
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            if game_state == "game":
                game_state = "menu"
                menu.state = "main"
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            elif game_state == "menu" and menu.state == "settings":
                menu.state = "main"
        
        # Очистка экрана
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Рендеринг в зависимости от состояния
        if game_state == "menu":
            menu.render()
        elif game_state == "game":
            player.update(window)
            player.apply_camera()
            render_world(world)
        
        # Обновление окна
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    # Завершение
    glfw.terminate()

if __name__ == "__main__":
    main()