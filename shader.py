from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

def load_shaders():
    """Загрузка и компиляция шейдеров."""
    vertex_shader_source = """
    #version 330 core
    layout(location = 0) in vec3 aPos;
    layout(location = 1) in vec3 aColor;
    out vec3 ourColor;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    void main() {
        gl_Position = projection * view * model * vec4(aPos, 1.0);
        ourColor = aColor;
    }
    """

    fragment_shader_source = """
    #version 330 core
    in vec3 ourColor;
    out vec4 FragColor;
    void main() {
        FragColor = vec4(ourColor, 1.0);
    }
    """

    try:
        vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        shader_program = compileProgram(vertex_shader, fragment_shader)
    except Exception as e:
        print(f"Shader compilation failed: {e}")
        raise
    
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return shader_program