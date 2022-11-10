import pygame
from constants import H, W


class Walls(object):
    def create_list(self, size):
        ''' Creates a list of wall Rect objects.'''
        walls = []
        walls.append(pygame.Rect((0, 0), (W, size)))  # top wall
        walls.append(pygame.Rect((0, H - size), (W, size)))  # bottom wall
        return walls
