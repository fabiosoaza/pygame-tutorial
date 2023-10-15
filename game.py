import pygame, sys
import random, time
import math


pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 6
SCORE = 0

#Creating colors
# Predefined some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

IMAGES_PATH = "assets/images/"
SOUNDS_PATH = "assets/sounds/"

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(IMAGES_PATH+"AnimatedStreet.png")
bg_height = background.get_height()
bg_rect = background.get_rect()

#define game variables
scroll = 0
tiles = math.ceil(SCREEN_HEIGHT  / bg_height) + 1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill(WHITE)
pygame.display.set_caption("Game")

run = True

FPS = 60
fps = pygame.time.Clock()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(IMAGES_PATH+"Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(IMAGES_PATH+"Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:
        # self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        # self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)



P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

MAX_SCROLL_SPEED=14


pygame.mixer.music.load(SOUNDS_PATH+'background.wav')
pygame.mixer.music.play(-1)

while run:

    # Desenhe o plano de fundo rolante
    for i in range(0, tiles):
        screen.blit(background, (0, -i * bg_height + scroll))

    #scroll speed 20% slower than speed
    speed_decrease = SPEED * 0.2
    scroll_speed = MAX_SCROLL_SPEED if SPEED - speed_decrease > MAX_SCROLL_SPEED else SPEED - speed_decrease
    scroll += scroll_speed

    # Redefina o scroll
    if scroll >= bg_height:
        scroll = 0

    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
            run = False
            pygame.mixer.music.stop()


    scores = font_small.render(str(SCORE), True, BLACK)
    screen.blit(scores, (10, 10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

        #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(SOUNDS_PATH+'crash.wav').play()
        time.sleep(0.5)
        pygame.mixer.music.stop()
        screen.fill(RED)
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        run = False

    pygame.display.update()
    fps.tick(FPS)

time.sleep(0.2)
pygame.quit()
