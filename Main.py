import pygame, DataGame
from pygame import *

pygame.init()
pygame.display.set_caption("Snake")
dataGame = DataGame.Load()
while True : dataGame.update()