#!python3.12
import pygame as pg
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import program_manager as pm
import primitives
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *


class Game():
    def __init__(self, size=(1920, 1080)):
        # set up pygame
        pg.init()
        self.viewsize = size
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
        verts = [[-0.5, -0.5, 0], [0, 0.5, 0], [0.5, -0.5, 0]]
        self.triangle = primitives.Primitive(vertices=verts, draw_mode=GL_TRIANGLES)
        self.triangle.enable_vertex_atribute(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))

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


if __name__ == '__main__':
    game = Game()
    game.run()
