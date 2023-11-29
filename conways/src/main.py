#!python3.12
import pygame as pg
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import program_manager as pm
import numpy as np
from collections import namedtuple

from OpenGL.GL import *
from OpenGL.GLU import *

Dimension = namedtuple("Dimension", "w h")

class Game():
    def __init__(self, size=Dimension(1920, 1080), scale=1):
        # set up pygame
        pg.init()
        self.viewsize = size
        self.scale = scale
        self.statesize = Dimension(size.w / scale, size.h / scale)
        self.clock = pg.time.Clock()
        # got to set flags and gl attributes
        self.flags = pg.OPENGL | pg.DOUBLEBUF
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        self.screen = pg.display.set_mode(self.viewsize, self.flags)
        # set gl clear color
        glClearColor(34 / 255, 105 / 255, 142 / 255, 0.77)
        # select shader program
        shaders = pm.build_shader_dirs()
        self.shader = shaders['default']

        self.triangle = Triangle()

    def handle_input(self):
        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONUP:
                (x, y) = pg.mouse.get_pos()
                print('click', (x, y))

    def run(self):
        while True:
            self.handle_input()
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(self.shader)
            self.triangle.draw()
            pg.display.flip()



class Triangle():

    def __init__(self):
        # specify verticies
        verticies = (
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0
        )
        verticies = np.array(verticies, dtype=np.float32)
        
        # create a vertex array object
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # create a vertex buffer object
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, verticies.nbytes, verticies, GL_STATIC_DRAW)

        # enable vertex attributes
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))

    def draw(self):
        # bind the vao we made
        glBindVertexArray(self.vao)
        # and draw the triangle
        glDrawArrays(GL_TRIANGLES, 0, 3)

if __name__ == '__main__':
    game = Game()
    game.run()
