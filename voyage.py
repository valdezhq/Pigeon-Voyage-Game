import pygame
from sys import exit
import random

# configs do jogo
GAME_WIDTH = 400
GAME_HEIGHT = 600
FPS = 60
TITLE = "Pigeon Voyage"

# imagens do jogo
BACKGROUND_IMG = pygame.image.load("assets/images/background.png").convert()
PIGEON_IMG = pygame.image.load("assets/images/pigeon{index}.png").convert_alpha()
PIGEON_IMG = pygame.transform.flip(PIGEON_IMG, True, False)

class Pigeon:
    def __init__(self):
        self.x = GAME_WIDTH / 8
        self.y = GAME_HEIGHT / 2
        pigeon_width = 30
        pigeon_height = 20
        self.rect = pygame.Rect(self.x, self.y, pigeon_width, pigeon_height)
        self.img = self.img


# inicia o pygame e configura a janela do jogo
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(FPS)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = -5