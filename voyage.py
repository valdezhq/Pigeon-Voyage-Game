import pygame
from sys import exit
import random

# configs do jogo
GAME_WIDTH = 388
GAME_HEIGHT = 689
FPS = 60
TITLE = "Pigeon Voyage"
index = 1

# classe do pombo
class Pigeon:
    def __init__(self):
        self.x = GAME_WIDTH / 8
        self.y = GAME_HEIGHT / 2
        pigeon_width = 30
        pigeon_height = 20
        self.rect = pygame.Rect(self.x, self.y, pigeon_width, pigeon_height)
        self.img = self.img

# classe dos prédios
class Building(pygame.Rect):
    def __init__(self):
        self.x = GAME_WIDTH
        self.y = 0
        building_width = 64
        building_height = 512
        self.rect = pygame.Rect(self.x, self.y, building_width, building_height)
        self.img = self.img

# imagens do jogo
background_img = pygame.image.load("assets/images/background.png")
pigeon_img = pygame.image.load(f"assets/images/pigeon{index}.png")
pigeon_img = pygame.transform.scale(pigeon_img, (pigeon_width, pigeon_height))
top_building_img = pygame.image.load("assets/images/top_building.png")
top_building_img = pygame.transform.scale(top_building_img, (top_building_width, top_building_height))
bottom_building_img = pygame.image.load("assets/images/bottom_building.png")
bottom_building_img = pygame.transform.scale(bottom_building_img, (bottom_building_width, bottom_building_height))

def draw():
    window.blit(background_img, (0, 0))
    window.blit(pigeon_img, pigeon)

    for building in buildings:
        window.blit(building.img, building)

    text_font = pygame.font.SysFont("Courier", 40)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))

def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    pigeon.y += velocity_y
    pigeon.y = max(pigeon.y, 0)

    if pigeon.y > GAME_HEIGHT:
        game_over = True
        return

    for building in buildings:
        building.x -= velocity_x

        if not building.passed and pigeon.x > building.x + building.width:
            score += 1
            building.passed = True

        # game over caso o player (pombo) colidir com o prédio
        if pigeon.colliderect(building):
            game_over = True
            return
        
    while len(buildings) > 0 and buildings[0].x < -building_width:
        buildings.pop(0) # remove os prédios que saíram da tela (tirando do final da lista)

def create_buildings():
    random_building_y = building_y - building_height/4 - random.random()*(building_height/2)
    opening = GAME_HEIGHT/4

    top_building = Building(top_building_img)
    top_building.y = random_building_y
    buildings.append(top_building)

    bottom_building = Building(bottom_building_img)
    bottom_building.y = top_building.y + top_building.height + opening
    buildings.append(bottom_building)

    print(len(buildings))

# inicia o pygame e configura a janela do jogo
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

create_buildings_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_buildings_timer, 1500) # cria um prédio a cada 1.5 segundos

# loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity_y = -5

                if game_over:
                    pigeon.y = pigeon_y
                    buildings.clear()
                    score = 0
                    game_over = False

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(FPS)