"""
Primitive definitions and behaviors. This I believe will make 2d rendering 
a bit more flexible. Because basically everything is a triangle even a 
fullscreen quad!
"""

from OpenGL import GL as gl
import numpy as np
import ctypes
from collections import namedtuple

Dimension = namedtuple("Program", "w h")


class Primitive(object):
    """Base class for other primitives."""

    def __init__(self, vertices: list[float], draw_mode):
        self.verticies = np.array(vertices, dtype=np.float32)
        self.vertex_count = Dimension(*np.shape(vertices))
        self.draw_mode = draw_mode

    def get_vao(self):
        """create a vertex array object"""
        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

    def get_vbo(self, usage: gl.GLenum = gl.GL_STATIC_DRAW):
        """create a vertex buffer object"""
        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        self.verticies.nbytes,
                        self.verticies,
                        usage)

    def enable_vertex_atribute(
            self,
            index: np.uint,
            size: int,
            type: gl.GLenum,
            normalized: gl.GLboolean,
            stride: gl.GLsizei,
            pointer: ctypes.c_void_p
    ):
        # able vertex attributes
        gl.glEnableVertexAttribArray(index)
        gl.glVertexAttribPointer(index, size, type, normalized, stride, pointer)

    
    def draw(self):
        # bind the vao we made
        gl.glBindVertexArray(self.vao)
        # and draw the triangle
        gl.glDrawArrays(self.draw_mode, 0, self.vertex_count.h)
