import pygame
from object import Object
from utils import load_sprite_sheets

class Danger(Object):
    ANIM_DELAY = 3

    def __init__(self, x, y, width, height):
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
