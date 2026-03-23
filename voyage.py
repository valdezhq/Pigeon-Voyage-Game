import pygame
from sys import exit
import random

# configs do jogo
GAME_WIDTH = 400
GAME_HEIGHT = 600
FPS = 60
TITLE = "Pigeon Voyage"

# instruções iniciais
INSTRUCTIONS = [
    "How to Play:",
    "SPACE - Fly",
    "R - Restart",
    "ESC - Quit",
]

# animação do pombo
pigeon_index = 0
animation_timer = 0
animation_speed = 5

# classe do pombo
pigeon_x = GAME_WIDTH / 8
pigeon_y = GAME_HEIGHT / 2
pigeon_width = 30
pigeon_height = 20

class Pigeon(pygame.Rect):
    def __init__(self, img): 
        pygame.Rect.__init__(self, pigeon_x, pigeon_y, pigeon_width, pigeon_height)
        self.img = img

# classe dos prédios
building_x = GAME_WIDTH
building_y = 0
building_width = 64
building_height = 512

class Building(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, building_x, building_y, building_width, building_height)
        self.img = img
        self.passed = False # checa se player passou pelo prédio ou não

# imagens do jogo
background_img = pygame.image.load("assets/images/background.png")
background_img = pygame.transform.scale(background_img, (GAME_WIDTH, GAME_HEIGHT))

pigeon_images = []
for i in range(1, 4):
    img = pygame.image.load(f"assets/images/pigeon{i}.png")
    img = pygame.transform.scale(img, (pigeon_width, pigeon_height))
    pigeon_images.append(img)

top_building_img = pygame.image.load("assets/images/topbuilding.png")
top_building_img = pygame.transform.scale(top_building_img, (building_width, building_height))

bottom_building_img = pygame.image.load("assets/images/bottombuilding.png")
bottom_building_img = pygame.transform.scale(bottom_building_img, (building_width, building_height))

# áudios do jogo
pygame.mixer.init()
collision_sound = pygame.mixer.Sound("assets/sounds/collision.ogg")
game_music = "assets/sounds/game-music.mp3"
menu_music = "assets/sounds/menu-music.wav"

# variáveis do jogo
pigeon = Pigeon(pigeon_images[0])
buildings = []
velocity_x = -4
velocity_y = 0
gravity = 0.2
score = 0
game_over = False
in_menu = True

def draw_overlay():
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # cor preta com transparência
    window.blit(overlay, (0, 0))

def draw():
    window.blit(background_img, (0, 0))
    window.blit(pigeon.img, pigeon)

    for building in buildings:
        window.blit(building.img, building)

    text_str = str(int(score))
    if game_over:
        draw_overlay()
        text_str = "Game Over! Score: " + text_str
        pygame.mixer.music.stop()

    text_font = pygame.font.SysFont("Courier", 30, bold=True)
    text_render = text_font.render(text_str, True, "white")
    text_rect = text_render.get_rect(center=(GAME_WIDTH/2, 50))
    window.blit(text_render, text_rect)

def draw_menu():
    window.blit(background_img, (0, 0))
    draw_overlay()

    # título do jogo
    title_font = pygame.font.SysFont("Courier", 40, bold=True)
    title_render = title_font.render(TITLE, True, "white")
    title_rect = title_render.get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2 - 80))
    window.blit(title_render, title_rect)

    # instruções do menu
    text_font = pygame.font.SysFont("Courier", 25, bold=True)
    for i, line in enumerate(INSTRUCTIONS):
        text_render = text_font.render(line, True, "white")
        text_rect = text_render.get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2 + i*50))
        window.blit(text_render, text_rect)

def move():
    global velocity_y, score, game_over

    if game_over:
        return

    velocity_y += gravity
    pigeon.y += velocity_y
    pigeon.y = max(pigeon.y, 0) # para o pombo não passar do topo da tela

    if pigeon.y > GAME_HEIGHT:
        if not game_over:
            game_over = True
            collision_sound.play()
        return

    for building in buildings:
        building.x += velocity_x

        if not building.passed and pigeon.x > building.x + building.width:
            score += 0.5 # 0.5 porque tem dois prédios
            building.passed = True

        # game over caso o player (pombo) colidir com o prédio
        if pigeon.colliderect(building):
            if not game_over:
                game_over = True
                collision_sound.play()
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

pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1) # toca a música do menu em loop

# loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_buildings_timer and not game_over and not in_menu:
            create_buildings()

        if not in_menu and not game_over:
            animation_timer += 1
        if animation_timer >= animation_speed:
            animation_timer = 0
            pigeon_index = (pigeon_index + 1) % len(pigeon_images)
            pigeon.img = pigeon_images[pigeon_index]

        # eventos de teclado para controle do jogo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if in_menu:
                    pygame.quit()
                    exit()
                else:
                    in_menu = True
                    game_over = False
                    velocity_y = 0
                    buildings.clear()
                    pigeon.y = pigeon_y
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)
                continue

            if event.key == pygame.K_SPACE:
                if in_menu:
                    in_menu = False
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play(-1)
                elif not game_over:
                    velocity_y = -5

            elif event.key == pygame.K_r and game_over:
                pigeon.y = pigeon_y
                buildings.clear()
                score = 0
                game_over = False
                velocity_y = 0
                in_menu = False
                pygame.mixer.music.load(game_music)
                pygame.mixer.music.play(-1)

    if in_menu:
        draw_menu()
    else:
        move()
        draw()

    pygame.display.update()
    clock.tick(FPS)