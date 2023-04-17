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
COUNTER = 0

# Game Window Setup
pygame.display.set_caption(WINDOW_TITLE)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(Snake().sprite)
# Set Menu fonts
font = pygame.font.Font('assets/fonts/font.otf', 100)
font_small = pygame.font.Font('assets/fonts/font.otf', 32)
font_20 = pygame.font.Font('assets/fonts/font.otf', 20)
title_bg = pygame.image.load('assets/wf_background/menu-bg.png')
lvl0_bg = pygame.image.load('assets/wf_background/level0.png')
lvl1_bg = pygame.image.load('assets/wf_background/level1.png')
lvl2_bg = pygame.image.load('assets/wf_background/level2.png')
lvl3_bg = pygame.image.load('assets/wf_background/level3.png')
end_bg = pygame.image.load('assets/wf_background/end_bg.png')
# Get SFXs
jumpfx = pygame.mixer.Sound("assets/sfx/jump.wav")
double_jumpfx = pygame.mixer.Sound("assets/sfx/double_jump.wav")
world_flipx = pygame.mixer.Sound("assets/sfx/world_flip.wav")
deadfx = pygame.mixer.Sound("assets/sfx/death.wav")

block_size = 140
start = StarterLevel(WIDTH, HEIGHT, block_size)
level1 = Level1(WIDTH, HEIGHT, block_size)
level2 = Level2(WIDTH, HEIGHT, block_size)
level3 = Level3(WIDTH, HEIGHT, block_size)
current_level = start


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
    global current_level
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
            player.dead = True
        if obj and obj.name == "ExitDoor":
            current_level = show_level_complete_screen(window, current_level)
            restart_all(objects)
            player.rect.x = current_level.player.rect.x
            player.rect.y = current_level.player.rect.y
            main(window)


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
    player = current_level.player
    player.y_vel = 0
    player.x_vel = 0
    player.fall_count = 0
    player.dead = False
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
        restartMessage = font_small.render(" RESTART ", True, (255, 255, 255), (0,0,0))
        restartMessage.set_alpha(128)
        window.blit(restartMessage, (window.get_width() /
                    2 - restartMessage.get_width()/2, 350))
        gameOverMessage = font.render(" GAME OVER ", True, (255, 255, 255), (0,0,0))
        gameOverMessage.set_alpha(128)
        window.blit(gameOverMessage, (window.get_width() /
                    2 - gameOverMessage.get_width()/2, 200))

        pygame.display.update()
        pygame.time.delay(10)


def show_level_complete_screen(window, level):

    # render the "LEVEL COMPLETE" message
    font = pygame.font.Font(None, 64)
    text = font.render(" LEVEL COMPLETE ", True, (255, 255, 255), (0,0,0))
    text.set_alpha(128)
    text_rect = text.get_rect(center=window.get_rect().center)
    window.blit(text, text_rect)

    # Level Description and tip
    if level.name == "LvlSpace":
        description = font_20.render(
            " You have finished the Demo! Great job. You've reached the spaceship. ", True, (255, 255, 255) , (0,0,0))
        description_rect = description.get_rect(
            center=window.get_rect().center)
        window.fill(WHITE)
        window.blit(lvl3_bg, (0, 0))
    elif level.name == "Lvl1":
        description = font_20.render(" You got the jist! Tip: Before the world flips, jump once in case the platform moves. ", True, (255, 255, 255) , (0,0,0))
        description_rect = description.get_rect(
            center=window.get_rect().center)
        window.fill(WHITE)
        window.blit(lvl0_bg, (0, 0))
    elif level.name == "Lvl2":
        description = font_20.render(" Good job! If you don't know where to go. Wait for the world to rotate! ", True, (255, 255, 255) , (0,0,0))
        description_rect = description.get_rect(
            center=window.get_rect().center)
        window.fill(WHITE)
        window.blit(lvl1_bg, (0, 0))
    elif level.name == "Lvl3":
        description = font_20.render(" Reach the spaceship. Dont wander too far from spawn. World flips can surprise you. ", True, (255, 255, 255) , (0,0,0))
        description_rect = description.get_rect(
            center=window.get_rect().center)
        window.fill(WHITE)
        window.blit(lvl2_bg, (0, 0))
    else:
        window.fill((255, 255, 255))
    # Background set

    description.set_alpha(128)
    window.blit(description, description_rect)

    # render the "CONTINUE TO NEXT LEVEL" message
    font = pygame.font.Font(None, 32)
    text = font.render(" CONTINUE TO NEXT LEVEL ", True, (255, 255, 255), (0,0,0))
    text.set_alpha(128)
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
                    if level == start:
                        return level1
                    elif level == level1:
                        return level2
                    elif level == level2:
                        return level3
                    else:
                        show_game_complete_screen(window)


def show_game_complete_screen(window):
    # Fill the screen with white color
    window.blit(end_bg, (0, 0))

    # Create a font object for the title and render the text
    font = pygame.font.Font('assets/fonts/font.otf', 100)
    title = font.render(" Congratulations! ", True, (255, 255, 255), (0, 0, 0))
    title.set_alpha(128)

    # Create a font object for the message and render the text
    font_small = pygame.font.Font('assets/fonts/font.otf', 32)
    message = font_small.render(
        " You have completed the Demo! Stay updated for more! ", True, (255, 255, 255), (0, 0, 0))
    message.set_alpha(128)

    # Create a font object for the instructions and render the text
    font_20 = pygame.font.Font('assets/fonts/font.otf', 20)
    instructions = font_20.render(" Press ESC to quit ", True, (255, 255, 255), (0, 0, 0))
    instructions.set_alpha(128)

    # Calculate the positions of the text objects
    title_rect = title.get_rect()
    title_rect.center = (WIDTH // 2, HEIGHT // 4)

    message_rect = message.get_rect()
    message_rect.center = (WIDTH // 2, HEIGHT // 2)

    instructions_rect = instructions.get_rect()
    instructions_rect.center = (WIDTH // 2, HEIGHT - 100)

    # Draw the text objects on the screen
    window.blit(title, title_rect)
    window.blit(message, message_rect)
    window.blit(instructions, instructions_rect)

    # Update the display
    pygame.display.flip()

    # Wait for the user to press SPACE or ESC
    while True:
        for event in pygame.event.get():
            if event.type == pygame.K_ESCAPE or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


## Main ####

def main(window):
    global COUNTER

    player = Player(current_level.player.rect.x,
                    current_level.player.rect.y, 50, 50)
    clock = pygame.time.Clock()
    if current_level.name == "LvlSpace":
        background, bg_image = get_background("bg_space.png")
    else:
        background, bg_image = get_background("bg.png")
    level = current_level

    offset_x = 0
    scroll_area_width = 200
    offset_y = 0
    scroll_area_height = 200

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
        startMessage = font_small.render(" START ", True, (255, 255, 255), (0,0,0))
        window.blit(startMessage, (window.get_width() /
                    2 - startMessage.get_width()/2, 350))

        pygame.display.update()
        pygame.time.delay(10)

    run = True
    while run:
        clock.tick(FPS)
        COUNTER += 1
        COUNTER %= 300
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
                COUNTER = 0
                pygame.mixer.Sound.play(world_flipx)
                rotate_world(level.objects_group)
            if event.type == FALL_OFF:
                if player.rect.top > HEIGHT or player.dead:
                    player.dead = False
                    pygame.time.set_timer(FALL_OFF, 0)
                    game_over_screen(level.objects_group)
                    return

        player.loop(FPS)
        handle_move(player, level.objects_group)

        draw(window, background, bg_image, player,
             level.objects_group, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
        if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0):
            offset_y += player.y_vel

    pygame.quit()
    quit()

## End of Main ##


if __name__ == "__main__":
    main(window)
