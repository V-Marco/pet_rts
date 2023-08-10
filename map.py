import pygame
import colors

screen_width = 600
screen_hegiht = 400

class Map:

    def __init__(self):
        self.surface = pygame.display.set_mode((screen_width, screen_hegiht))
        self.refresh()

    def refresh(self):
        self.surface.fill(colors.white)
        