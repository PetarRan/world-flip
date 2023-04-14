import pygame
class Snake: 
    def __init__(self):
        self.sprite = pygame.image.load('assets/wf_players/snake_main/dead.png')
        self.position = pygame.Vector2()
        self.position.xy