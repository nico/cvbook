from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame, pygame.image
from pygame.locals import *

width, height = 1000, 747

def setup():
  pygame.init()
  pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
  pygame.display.set_caption('Look, an OpenGL window!')

setup()

while True:
  event = pygame.event.poll()
  if event.type in (QUIT, KEYDOWN):
    break
  pygame.display.flip()
