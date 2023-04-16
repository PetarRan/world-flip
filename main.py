import pygame
import sys
import time
import math
from os.path import join
from snake import Snake
from player import Player
from danger import Danger
from block import Block
from utils import *

pygame.init()

# Global Variables
BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
WINDOW_TITLE = "World Flip"
FPS = 60
PLAYER_VEL = 5
WHITE = (255, 255, 255)

# Game Window Setup
pygame.display.set_caption(WINDOW_TITLE)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(Snake().sprite)
# Set Menu fonts
font = pygame.font.Font('assets/fonts/font.otf', 100)
font_small = pygame.font.Font('assets/fonts/font.otf', 32)
font_20 = pygame.font.Font('assets/fonts/font.otf', 20)
title_bg = pygame.image.load('assets/wf_background/menu-bg.png')
# Get SFXs
jumpfx = pygame.mixer.Sound("assets/sfx/jump.wav")
double_jumpfx = pygame.mixer.Sound("assets/sfx/double_jump.wav")
world_flipx = pygame.mixer.Sound("assets/sfx/world_flip.wav")
deadfx = pygame.mixer.Sound("assets/sfx/death.wav")


def get_background(name):
    image = pygame.image.load(join("assets", "wf_background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i*width, j*height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for platform in objects:
        platform.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hithead()

            collided_objects.append(obj)

    return collided_objects


def handle_horizontal_collision(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_obj = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_obj = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided_obj


def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    collide_left = handle_horizontal_collision(
        player, objects, -PLAYER_VEL * 2)
    collide_right = handle_horizontal_collision(
        player, objects, PLAYER_VEL * 2)

    player.x_vel = 0
    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    collide_vertical = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *collide_vertical]
    for obj in to_check:
        if obj and obj.name == "danger":
            player.make_hit()


# World settings:
block_size = 140
player = Player(100, 100, 50, 50)
floor = [Block(i*block_size, HEIGHT - block_size, block_size)
         for i in range(5)]
wall = []
for i in range(3):
    block = floor[i]
    rotated_block = Block(block.rect.x + 750, block.rect.y - 380, block_size)
    rotated_block.image = pygame.transform.rotate(block.image, 90)
    if i == 0:
        wall.append(rotated_block)
    else:
        prev_block = wall[i-1]
        offset_y = prev_block.rect.y - 3*block_size
        new_block = Block(rotated_block.rect.x - i * block_size,
                          rotated_block.rect.y + offset_y, block_size)
        new_block.image = rotated_block.image
        wall.append(new_block)

world_group = pygame.sprite.Group()
world_group.add(floor)
world_group.add(wall)

# End of World settings


import math

def rotate_world(objects):
    # Convert the angle from degrees to radians
    angle = math.radians(90)

    # Calculate the center of the screen
    center_x = WIDTH / 2
    center_y = HEIGHT / 2

    # Loop through all the blocks in the world
    for block in objects:
        # Calculate the offset from the center of the screen
        x_offset = block.rect.x - center_x
        y_offset = block.rect.y - center_y

        # Calculate the hypotenuse from the block's position to the center of the screen
        rho = math.sqrt(x_offset ** 2 + y_offset ** 2)

        # Calculate the angle between the hypotenuse and the x axis
        if x_offset >= 0:
            theta = math.atan(y_offset / x_offset)
        elif y_offset > 0:
            theta = math.atan(y_offset / x_offset) + math.pi
        else:
            theta = math.atan(y_offset / x_offset) - math.pi

        # Calculate the new angle after a 90 degree rotation
        theta1 = theta + math.pi / 2

        # Calculate the new coordinates of the block
        new_x = rho * math.cos(theta1) + center_x
        new_y = rho * math.sin(theta1) + center_y

        # Round the coordinates to the nearest integer
        new_x = round(new_x)
        new_y = round(new_y)

        # Update the block's position in the world
        block.rect.x = new_x
        block.rect.y = new_y



## Main ####


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("bg.png")
    ROTATE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ROTATE_EVENT, 5000)

    spikes = Danger(100, HEIGHT - block_size - 140, 70, 70)
    spikes.on()

    objects = [*floor, *wall]

    offset_x = 0
    scroll_area_width = 200

    # Title Screen
    last_time = time.time()
    splashScreenTimer = 0
    pygame.mixer.Sound.play(world_flipx)
    while splashScreenTimer < 100:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        splashScreenTimer += dt

        for event in pygame.event.get():
            # if the user clicks the button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill((255, 255, 255))
        # fill the start message on the top of the game
        startMessage = font_small.render("WORLD FLIP", True, (240, 95, 123))
        window.blit(startMessage, (window.get_width()/2 - startMessage.get_width() /
                    2, window.get_height()/2 - startMessage.get_height()/2))

        # update display
        pygame.display.update()
        # wait for 10 seconds
        pygame.time.delay(10)
    titleScreen = True
    # title screen
    pygame.mixer.Sound.play(jumpfx)
    while titleScreen:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        mouseX, mouseY = pygame.mouse.get_pos()
        clicked = False
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if (clicked):
            clicked = False
            pygame.mixer.Sound.play(double_jumpfx)
            titleScreen = False

        window.fill(WHITE)
        window.blit(title_bg, (0, 0))
        startMessage = font_small.render("START", True, (255, 255, 255))
        window.blit(startMessage, (window.get_width() /
                    2 - startMessage.get_width()/2, 350))

        pygame.display.update()
        pygame.time.delay(10)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player.jump_count < 2:
                    player.jump()
                    if player.jump_count > 1:
                        pygame.mixer.Sound.play(double_jumpfx)
                    else:
                        pygame.mixer.Sound.play(jumpfx)
            if event.type == ROTATE_EVENT:
                pygame.mixer.Sound.play(world_flipx)
                rotate_world(objects)

        player.loop(FPS)
        spikes.loop()
        handle_move(player, objects)

        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()

## End of Main ##


if __name__ == "__main__":
    main(window)
