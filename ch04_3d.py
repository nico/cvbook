from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame, pygame.image
from pygame.locals import *
import numpy


width, height = 1000, 747


def set_projection_from_camera(K):
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()

  fx = K[0, 0]
  fy = K[1, 1]
  fovy = 2 * numpy.arctan(0.5 * height / fy) * 180 / numpy.pi
  aspect = (width * fy) / (height * fx)

  near, far = 0.1, 100
  gluPerspective(fovy, aspect, near, far)
  glViewport(0, 0, width, height)


def setup():
  pygame.init()
  pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
  pygame.display.set_caption('Look, an OpenGL window!')


setup()
K = numpy.array([[1, 0], [0, 1]])  # FIXME
set_projection_from_camera(K)

while True:
  event = pygame.event.poll()
  if event.type in (QUIT, KEYDOWN):
    break
  pygame.display.flip()
