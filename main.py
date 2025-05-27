import glfw
from OpenGL.GL import *
from world import World
from player import Player
from menu import Menu
from shader import load_shaders
from constants import *
import numpy as np

def main():
    # Инициализация GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        return
    
    # Создание окна
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Minecraft Clone", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    print("OpenGL Version:", glGetString(GL_VERSION).decode('utf-8'))
    
    # Настройка OpenGL
    glEnable(GL_DEPTH_TEST)
    
    # Загрузка шейдеров
    try:
        shader_program = load_shaders()
    except Exception as e:
        print(f"Failed to load shaders: {e}")
        glfw.terminate()
        return
    
    # Инициализация меню, мира и игрока
    menu = Menu()
    world = World()
    world.shader_program = shader_program
    player = None
    game_state = "menu"
    
    # Обработка клика мыши
    def mouse_button_callback(window, button, action, mods):
        nonlocal game_state, player
        if game_state == "menu" and button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            result = menu.handle_click(x, y)
            if result == "game":
                if player is None:
                    player = Player()
                    print("Generating initial chunks...")
                    world.generate_chunks(player.pos)
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
        
        # Рендеринг
        if game_state == "menu":
            menu.render()
        elif game_state == "game":
            player.update(window)
            # Матрицы для шейдеров
            projection = np.array([
                [1.0 / np.tan(np.radians(FOV / 2)) * (SCREEN_WIDTH / SCREEN_HEIGHT), 0, 0, 0],
                [0, 1.0 / np.tan(np.radians(FOV / 2)), 0, 0],
                [0, 0, -(FAR_PLANE + NEAR_PLANE) / (FAR_PLANE - NEAR_PLANE), -1],
                [0, 0, -2 * FAR_PLANE * NEAR_PLANE / (FAR_PLANE - NEAR_PLANE), 0]
            ], dtype=np.float32)
            
            view = player.get_view_matrix()
            
            world.generate_chunks(player.pos)
            world.render(view, projection)
        
        # Обновление окна
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    # Завершение
    glfw.terminate()

if __name__ == "__main__":
    main()