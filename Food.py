import pygame
from pygame import Rect

class Food():
    def __init__(self, pos, gameDisplay):
        self.pos = pos
        self.gameDisplay = gameDisplay

    def draw(self):
        pygame.draw.rect(self.gameDisplay, 0x00FF00, (self.pos[0]*20, self.pos[1]*20, 20, 20))
