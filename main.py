import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COIN_YELLOW_COLOR = (255, 255, 224)
FPS = 60


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(
            "./assets/player_dragon_sprite.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Particle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((5, 5))
        self.surf.fill((100, 100, 100))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(10, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(
            "./assets/misc_coin_sprite.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(0, 0)

    def destruct(self):
        self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("./assets/pngegg (1).png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                -100,
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 10)
        self.move_direction = 0

    def update(self):
        if (player.rect[1] > self.rect[1]):
            self.move_direction = 1
        else:
            self.move_direction = -1

        self.rect.move_ip(self.speed, self.move_direction)
        if (self.rect.left > SCREEN_WIDTH):
            self.kill()


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

ADDPARTICLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPARTICLE, 250)
ADDCOIN = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCOIN, 1500)
ADDENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY, 750)

player = Player()

font = pygame.font.Font('freesansbold.ttf', 16)
score = 0
text = font.render('Coins: ' + str(score), True, COIN_YELLOW_COLOR)
textRect = text.get_rect()
textRect.center = (50, 40)

particles = pygame.sprite.Group()
coins = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        if event.type == ADDPARTICLE:
            new_particle = Particle()
            particles.add(new_particle)
            all_sprites.add(new_particle)
        if event.type == ADDCOIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
        if event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.fill((30, 30, 30))

    pressed_keys = pygame.key.get_pressed()

    for coin in coins:
        if player.rect.colliderect(coin.rect):
            coin.destruct()
            score += 1
            text = font.render('Coins: ' + str(score), True, COIN_YELLOW_COLOR)
            textRect = text.get_rect()
            textRect.center = (50, 40)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    screen.blit(text, textRect)

    particles.update()
    enemies.update()
    player.update(pressed_keys)

    pygame.display.flip()

pygame.quit()
