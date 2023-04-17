import pygame
from block import *
from player import Player


class StarterLevel:
    def __init__(self, screen_width, screen_height, block_size):
        # create the objects in the level
        floor = [Block(i * block_size, screen_height -
                       block_size, block_size) for i in range(5)]
        wall = []
        for i in range(3):
            block = floor[i]
            rotated_block = Block(block.rect.x + 750,
                                  block.rect.y - 380, block_size)
            rotated_block.image = pygame.transform.rotate(block.image, 90)
            if i == 0:
                wall.append(rotated_block)
            else:
                prev_block = wall[i - 1]
                offset_y = prev_block.rect.y - 3 * block_size
                new_block = Block(rotated_block.rect.x - i * block_size,
                                  rotated_block.rect.y + offset_y, block_size)
                new_block.image = rotated_block.image
                wall.append(new_block)

        player = Player(100, 100, 50, 50)
        exit_door = ExitDoor(wall[-1], block_size, 90)
        exit_door.rotate_block(90)

        # create sprite groups for collision detection and rendering
        objects_group = pygame.sprite.Group()
        objects_group.add(floor)
        objects_group.add(wall)
        objects_group.add(exit_door)

        self.objects_group = objects_group
        self.player = player
        self.exit_door = exit_door

class Level1:
    def __init__(self, screen_width, screen_height, block_size):

        floor = [Block(i * block_size, screen_height -
                       block_size, block_size) for i in range(5)]
        # create an array of blocks for the platform
        platform_blocks = [Block(i * block_size, screen_height - 5*block_size, block_size) for i in range(6, 10)]
        platform_blocks_inner = [InnerBlock(i * block_size, screen_height - 4*block_size, block_size) for i in range(6, 10)]

        platform_blocks_down = [Block(i * block_size, screen_height - 2*block_size, block_size) for i in range(6, 10)]
        platform_blocks_inner_down = [InnerBlock(i * block_size, screen_height - block_size, block_size) for i in range(6, 10)]

        wall = []
        for i in range(3):
            block = floor[i]
            rotated_block = Block(block.rect.x + 1510,
                                  block.rect.y - 380, block_size)
            rotated_block.image = pygame.transform.rotate(block.image, 90)
            if i == 0:
                wall.append(rotated_block)
            else:
                prev_block = wall[i - 1]
                offset_y = prev_block.rect.y - 3 * block_size
                new_block = Block(rotated_block.rect.x - i * block_size,
                                  rotated_block.rect.y + offset_y, block_size)
                new_block.image = rotated_block.image
                wall.append(new_block)

        spikes = Danger(floor[-1], 70, 70, 0)
        spikes.rotate_block(90)
        spikes.on()
        spikes.loop()
        spikes.rect.y -= 30

        # create exit door
        exit_door = ExitDoor(wall[0], block_size, 180)
        exit_door.rotate_block(180)
        
        player = Player(100, 100, 50, 50)
        
        # create sprite groups for collision detection and rendering
        objects_group = pygame.sprite.Group()
        objects_group.add(spikes)
        objects_group.add(floor)
        objects_group.add(platform_blocks)
        objects_group.add(platform_blocks_inner)
        objects_group.add(platform_blocks_down)
        objects_group.add(platform_blocks_inner_down)
        objects_group.add(wall)
        objects_group.add(exit_door)

        self.objects_group = objects_group
        self.player = player
        self.exit_door = exit_door