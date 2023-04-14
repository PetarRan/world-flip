import pygame
import math
from object import Object
from utils import get_block

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
    def rotate_block(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = rotated_rect
