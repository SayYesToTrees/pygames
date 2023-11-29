"""
This module is for convienience when working with shaders in pyopengl.

Pyopengl also offers a shaders convinience class for similar functionality.
However its compileProgram() function is not standard OpenGL. They reccomended
possibly copying the function to gaurd against PyOpenGL changes.
But I wanted to try to make my own version.
"""

from OpenGL.GL import (
    GLenum, GLError,
    GL_COMPILE_STATUS, GL_TRUE, GL_FALSE, GL_INFO_LOG_LENGTH, GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER, GL_LINK_STATUS, GL_TESS_EVALUATION_SHADER,
    GL_GEOMETRY_SHADER, GL_COMPUTE_SHADER, GL_TESS_CONTROL_SHADER,
    glCreateShader, glShaderSource, glCompileShader, glGetShaderiv,
    glGetShaderInfoLog, glDeleteShader, glCreateProgram, glAttachShader,
    glGetProgramiv, glGetProgramInfoLog, glLinkProgram,
)
import os
from collections import namedtuple

glsl_dir = os.getcwd() + '/glsl_shaders/'


def compile_shader(
        shader_type: GLenum,
        source_string: str,
        ):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source_string)
    glCompileShader(shader)
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if result != GL_TRUE:
        info_log = glGetShaderInfoLog(shader)
        glDeleteShader(shader)
        raise GLError(info_log)
    else:
        return shader


Program = namedtuple("Program", ["name", "shaders"])

def compile_shader_program(program: Program):
    compiled_shaders = []
    id = glCreateProgram()
    for shader in program.shaders:
        with open(glsl_dir + program.name + '/' + shader, 'r') as file:
            shader_type = None
            match shader[-4:]:
                case 'vert': shader_type = GL_VERTEX_SHADER
                case 'frag': shader_type = GL_FRAGMENT_SHADER
                case 'tese': shader_type = GL_TESS_EVALUATION_SHADER
                case 'tesc': shader_type = GL_TESS_CONTROL_SHADER
                case 'geom': shader_type = GL_GEOMETRY_SHADER
                case 'comp': shader_type = GL_COMPUTE_SHADER
                case _: raise Exception("shader ext not matched")
            glAttachShader(id, compile_shader(shader_type, file.readlines()))
    glLinkProgram(id)
    result = glGetProgramiv(id, GL_LINK_STATUS)
    if result != GL_TRUE:
        info_log = glGetProgramInfoLog(id)
        raise GLError(info_log)
    for shader in compiled_shaders:
        glDeleteShader(shader)
    return id


def build_shader_dirs():
    programs = {}
    dirnames = os.scandir(glsl_dir)
    for dname in dirnames:
        shaders = [shader_file.name for shader_file in os.scandir(glsl_dir + dname.name)]
        programs[dname.name] = compile_shader_program(Program(dname.name, shaders))


    return programs
