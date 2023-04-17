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
        self.name = "tutorial"


class Level1:
    def __init__(self, screen_width, screen_height, block_size):

        floor = [Block(i * block_size, screen_height -
                       block_size, block_size) for i in range(5)]
        # create an array of blocks for the platform
        platform_blocks = [Block(
            i * block_size, screen_height - 5*block_size, block_size) for i in range(6, 10)]
        platform_blocks_inner = [InnerBlock(
            i * block_size, screen_height - 4*block_size, block_size) for i in range(6, 10)]

        platform_blocks_down = [Block(
            i * block_size, screen_height - 2*block_size, block_size) for i in range(6, 10)]
        platform_blocks_inner_down = [InnerBlock(
            i * block_size, screen_height - block_size, block_size) for i in range(6, 10)]

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
        self.name = "Lvl1"


class Level2:
    def __init__(self, screen_width, screen_height, block_size):
        floor = [Block(i * block_size, screen_height -
                       2*block_size, block_size) for i in range(1, 3)]

        floor_1 = [Block(i * block_size, screen_height -
                         2*block_size, block_size) for i in range(4, 7)]

        floor_2 = [Block(i * block_size, screen_height -
                         5*block_size, block_size) for i in range(6, 9)]

        floor_3 = [Block(i * block_size, screen_height -
                         5*block_size, block_size) for i in range(10, 12)]
        
        floor_4 = [Block(i * block_size, screen_height -
                         5*block_size, block_size) for i in range(-4, -2)]
        wall = []
        for i in range(3):
            block = floor_1[i]
            rotated_block = Block(block.rect.x + 750,
                                  block.rect.y + 0, block_size)
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

        # Creating Spikes

        spikes = Danger(floor[-1], 70, 70, 0)
        spikes.rotate_block(90)
        spikes.on()
        spikes.loop()
        spikes.rect.y -= 30

        spikes_under = Danger(floor_2[-1], 70, 70, 0)
        spikes_under.rotate_block(180)
        spikes_under.on()
        spikes_under.loop()
        spikes_under.rect.y -= 30

        # create exit door
        exit_door = ExitDoor(floor_3[-1], block_size, 180)
        exit_door.rotate_block(180)

        # create sprite groups for collision detection and rendering
        player = Player(150, 100, 50, 50)

        objects_group = pygame.sprite.Group()
        objects_group.add(spikes)
        objects_group.add(spikes_under)
        objects_group.add(floor)
        objects_group.add(floor_1)
        objects_group.add(floor_2)
        objects_group.add(floor_3)
        objects_group.add(floor_4)
        objects_group.add(wall)
        objects_group.add(exit_door)

        self.objects_group = objects_group
        self.player = player
        self.exit_door = exit_door
        self.name = "Demo"


class Level3:
    def __init__(self, screen_width, screen_height, block_size):
        # create floor
        floor = [SpaceBlock(i * block_size, screen_height - 2 * block_size, block_size) for i in range(-5, 14)]

        # create upper platform
        upper_platform = [SpaceBlock(i * block_size, screen_height - 8 * block_size, block_size) for i in range(2, 8)]

        # create middle platform
        middle_platform = [SpaceBlock(i * block_size, screen_height - 14 * block_size, block_size) for i in range(-1, 6)]

        # create left wall
        left_wall = [SpaceBlock(-2 * block_size, screen_height - (i + 2) * block_size, block_size) for i in range(5)]

        # create right wall
        right_wall = [SpaceBlock(screen_width - block_size * 2, screen_height - (i + 2) * block_size, block_size) for i in range(5)]

        # Creating Spikes
        spikes = Danger(middle_platform[4], 70, 70, 0)
        spikes.rotate_block(90)
        spikes.on()
        spikes.loop()
        spikes.rect.y -= 30

        spikes2 = Danger(upper_platform[1], 70, 70, 0)
        spikes2.rotate_block(90)
        spikes2.on()
        spikes2.loop()
        spikes2.rect.y -= 30

        spikes3 = Danger(right_wall[-1], 70, 70, 0)
        spikes3.rotate_block(90)
        spikes3.on()
        spikes3.loop()
        spikes3.rect.y -= 30
        spikes3.rect.x += 30


        # create exit door
        exit_door = ExitDoor(right_wall[-1], block_size, 270)
        exit_door.rotate_block(-90)

        # create sprite groups for collision detection and rendering
        player = Player(150, 100, 50, 50)

        objects_group = pygame.sprite.Group()
        objects_group.add(spikes)
        objects_group.add(spikes2)
        objects_group.add(spikes3)
        objects_group.add(floor)
        objects_group.add(upper_platform)
        objects_group.add(middle_platform)
        objects_group.add(left_wall)
        objects_group.add(right_wall)
        objects_group.add(exit_door)

        self.objects_group = objects_group
        self.player = player
        self.exit_door = exit_door
        self.name = "LvlSpace"
