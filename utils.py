import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
window = pygame.display.set_mode((1000, 800))

## Getting an asset for creating platforms
def get_block(size):
    path = join("assets", "wf_terrain", "tiles_terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(72, 432, size, size)  # 576 - [pos of tile block]
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


## Loading sprite sheets with orientations from assets folders
def load_sprite_sheets(dir1, name, width, height, direction=False):
    path = join("assets", dir1, name)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


## Flipping a sprite in a certain direction
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
