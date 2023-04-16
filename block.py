import pygame
import math, sys
from object import Object
from utils import get_block, get_door


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


class ExitDoor(Object):
    def __init__(self, final_block, size, rotate):
        x_offset = 0
        y_offset = 0
        
        if rotate == 0:
             y_offset = -1*size
        elif rotate == 90:
            x_offset = -1*size
        elif rotate == 180:
            y_offset = size
        elif rotate == 270:
            x_offset = size
        x = final_block.rect.x + x_offset
        y = final_block.rect.y + y_offset
        super().__init__(x, y, size, size)
        exit_door = get_door(size)
        self.image.blit(exit_door, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = "ExitDoor"

    def show_level_complete_screen(self, screen, next_level):
        font = pygame.font.SysFont(None, 64)
        text = font.render("Level completed!", True, (255, 255, 255))
        text_rect = text.get_rect(center=screen.get_rect().center)
        
        next_button = pygame.Rect(0, 0, 200, 50)
        next_button.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)
        next_button_text = font.render("Next level", True, (255, 255, 255))
        next_button_text_rect = next_button_text.get_rect(center=next_button.center)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if next_button.collidepoint(event.pos):
                        return next_level
            
            screen.fill((0, 0, 0))
            screen.blit(text, text_rect)
            pygame.draw.rect(screen, (255, 255, 255), next_button)
            screen.blit(next_button_text, next_button_text_rect)
            
            pygame.display.flip()
    
    def rotate_block(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = rotated_rect    