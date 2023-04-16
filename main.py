import pygame
import sys
import time
import math
from os.path import join
from player import Player, Snake
from block import Block, ExitDoor, Danger
from levels import *
from utils import *

pygame.init()

# Global Variables
BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
WINDOW_TITLE = "World Flip"
FPS = 60
PLAYER_VEL = 5
WHITE = (255, 255, 255)
ROTATE_EVENT = pygame.USEREVENT + 1
ROTATE_INTERVAL = 5000
ROTATE_POSITION = 0
FALL_OFF = pygame.USEREVENT + 2

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

    player.x_vel = 0

    collide_left = handle_horizontal_collision(
        player, objects, -PLAYER_VEL * 2)
    collide_right = handle_horizontal_collision(
        player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    collide_vertical = handle_vertical_collision(player, objects, player.y_vel)

    to_check = [collide_left, collide_right, *collide_vertical]
    for obj in to_check:
        if obj and obj.name == "danger":
            player.make_hit()
        if obj and obj.name == "ExitDoor":
            obj.show_level_complete_screen(window, Level1)


block_size = 140
player = Player(100, 100, 50, 50)


def rotate_world(objects):
    # Convert the angle from degrees to radians
    angle = math.radians(90)

    global ROTATE_POSITION
    ROTATE_POSITION += 1
    ROTATE_POSITION %= 4

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
        block.rotate_block(-90)


def restart_all(objects):
    player.rect.x = 100
    player.rect.y = 100
    player.y_vel = 0
    player.x_vel = 0
    for i in range(4 - ROTATE_POSITION):
        rotate_world(objects)
    pygame.time.set_timer(ROTATE_EVENT, ROTATE_INTERVAL)
    main(window)


def game_over_screen(objects):
    game_over = True
    last_time = time.time()
    pygame.mixer.Sound.play(deadfx)
    while game_over:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
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
            game_over = False
            restart_all(objects)

        window.fill(WHITE)
        window.blit(title_bg, (0, 0))
        restartMessage = font_small.render("RESTART", True, (255, 255, 255))
        window.blit(restartMessage, (window.get_width() /
                    2 - restartMessage.get_width()/2, 350))
        gameOverMessage = font.render("GAME OVER", True, (255, 255, 255))
        window.blit(gameOverMessage, (window.get_width() /
                    2 - gameOverMessage.get_width()/2, 200))

        pygame.display.update()
        pygame.time.delay(10)


def show_level_complete_screen(self, window, next_level):
    # clear the screen
    window.fill((255, 255, 255))

    # render the "LEVEL COMPLETE" message
    font = pygame.font.Font(None, 64)
    text = font.render("LEVEL COMPLETE", True, (0, 0, 0))
    text_rect = text.get_rect(center=window.get_rect().center)
    window.blit(text, text_rect)

    # render the "CONTINUE TO NEXT LEVEL" message
    font = pygame.font.Font(None, 32)
    text = font.render("CONTINUE TO NEXT LEVEL", True, (255, 255, 255))
    text_rect = text.get_rect(
        center=(window.get_width() // 2, window.get_height() // 2 + 50))
    window.blit(text, text_rect)

    # update the screen
    pygame.display.update()

    # wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check if the user clicked on the "CONTINUE TO NEXT LEVEL" message
                if text_rect.collidepoint(event.pos):
                    self.current_level = next_level
                    return


## Main ####


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("bg.png")
    level = StarterLevel(WIDTH, HEIGHT, block_size)

    spikes = Danger(100, HEIGHT - block_size - 140, 70, 70)
    spikes.on()

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
            pygame.time.set_timer(ROTATE_EVENT, ROTATE_INTERVAL)
            pygame.time.set_timer(FALL_OFF, 100)

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
                rotate_world(level.objects_group)
            if event.type == FALL_OFF:
                if player.rect.top > HEIGHT:
                    pygame.time.set_timer(FALL_OFF, 0)
                    game_over_screen(level.objects_group)
                    return

        player.loop(FPS)
        spikes.loop()
        handle_move(player, level.objects_group)

        draw(window, background, bg_image, player,
             level.objects_group, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()

## End of Main ##


if __name__ == "__main__":
    main(window)
