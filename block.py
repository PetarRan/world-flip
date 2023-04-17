import pygame
import math, sys
from object import Object
from utils import get_block, get_door, load_sprite_sheets, get_inner_blcok, get_space_block

## Platform Block
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


class SpaceBlock(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_space_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def rotate_block(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = rotated_rect

## InnerPlatform Block
class InnerBlock(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_inner_blcok(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def rotate_block(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = rotated_rect


## Exit Door leading to new level
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

## Obstacles that cause damage resulting in level fail
class Danger(Object):
    ANIM_DELAY = 3

    def __init__(self, final_block, width, height, rotate):
        x_offset = 0
        y_offset = 0
        
        if rotate == 0:
             y_offset = -1*height
        elif rotate == 90:
            x_offset = -1*width
        elif rotate == 180:
            y_offset = height
        elif rotate == 270:
            x_offset = width
        x = final_block.rect.x + x_offset
        y = final_block.rect.y + y_offset

        super().__init__(x, y, width, height)
        self.danger = load_sprite_sheets("wf_terrain", "spikes", width, height)
        self.image = self.danger["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"
        self.name = "danger"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.danger[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIM_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIM_DELAY > len(sprites):
            self.animation_count = 0
    def rotate_block(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = rotated_rect