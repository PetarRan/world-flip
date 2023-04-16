import pygame
from block import Block, ExitDoor, Danger
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

    def show_level_complete_screen(self, screen):
        # show level complete screen and load next level
        font = pygame.font.Font(None, 50)
        text = font.render("Level Completed!", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

        # load next level
        return None


class Level1:
    def __init__(self, screen_width, screen_height, block_size):

        # create blocks for the L-shaped platform on the left
        #left_platform_blocks = [Block(0, screen_height - block_size * 2, block_size) for i in range(2)] + \
                            #[Block(block_size, screen_height - block_size * 2, block_size)] + \
                            #[Block(block_size * i, screen_height - block_size * 3, block_size) for i in range(2)]

        # create blocks for the L-shaped platform on the top left
        #top_left_platform_blocks = [Block(0, screen_height - block_size * (i + 1) - 100, block_size) for i in range(2)] + \
                                #[Block(block_size, screen_height - block_size * 2 - 100, block_size)] + \
                                #[Block(block_size * i, screen_height - block_size * 3 - 100, block_size) for i in range(2)]

        # create blocks for the flat platform on the right
        ##right_platform_blocks = [Block(400 + i * block_size, screen_height - block_size, block_size) for i in range(7)]

        middle_platform_blocks = [Block(screen_width / 2 - block_size / 2, screen_height / 2 - block_size / 2, block_size)]



        # create exit door
        #exit_door = ExitDoor(right_platform_blocks[-1], block_size, 90)
        player = Player(100, 100, 50, 50)
        # create sprite groups for collision detection and rendering
        objects_group = pygame.sprite.Group()
        objects_group.add(middle_platform_blocks)
        #objects_group.add(left_platform_blocks)
        #objects_group.add(top_left_platform_blocks)
        #objects_group.add(right_platform_blocks)
        #objects_group.add(exit_door)

        self.objects_group = objects_group
        self.player = player
        #self.exit_door = exit_door

    def show_level_complete_screen(self, screen):
        # show level complete screen and load next level
        font = pygame.font.Font(None, 50)
        text = font.render("Level Completed!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

        # load next level
        return None