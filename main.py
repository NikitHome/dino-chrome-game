import pygame
import pygame.freetype

import random

pygame.init()

screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Dino game')
clock = pygame.time.Clock()
font = pygame.freetype.Font(None, 40)

cactus_image = pygame.image.load('./sprites/plant.png')
cactus_image = pygame.transform.scale(cactus_image, (50, 80))
dino_image = pygame.image.load('./sprites/dino.png')
dino_image = pygame.transform.scale(dino_image, (100, 100))
ground_image = pygame.image.load('./sprites/bg.png')
ground_image = pygame.transform.scale(ground_image, (800, 142))

ground_group = pygame.sprite.Group()
cactus_group = pygame.sprite.Group()

ground_event = pygame.USEREVENT
cactus_event = pygame.USEREVENT + 1
pygame.time.set_timer(ground_event, 2000)
pygame.time.set_timer(cactus_event, 6000)


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()
            dino.score += 1
        if self.rect.colliderect(dino.rect):
            dino.game_status = 'Menu'


class Dino():
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.y = 0
        self.step = 6
        self.max_jump = 60
        self.in_jump = False
        self.score = 0
        self.game_status = 'Game'

    def jump(self):
        if self.in_jump:
            if self.y < self.max_jump:
                self.y += 1
                self.rect.y -= self.step
            elif self.y < self.max_jump * 2:
                self.y += 1
                self.rect.y += self.step
            else:
                self.in_jump = False
                self.y = False

    def draw(self):
        screen.blit(self.image, self.rect)


dino = Dino(dino_image, (100, 400))
g = Ground(ground_image, (300, 450))
ground_group.add(g)

g = Ground(ground_image, (900, 450))
ground_group.add(g)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            dino.in_jump = True
        if event.type == ground_event:
            g = Ground(ground_image, (900, 450))
            ground_group.add(g)
        if event.type == cactus_event:
            pygame.time.set_timer(cactus_event, random.randint(6000, 10000))
            c = Cactus(cactus_image, (910, 400))
            cactus_group.add(c)

    screen.fill((255, 255, 255))
    if dino.game_status == 'Game':
        ground_group.update()
        ground_group.draw(screen)
        cactus_group.update()
        cactus_group.draw(screen)
        dino.jump()
        dino.draw()
        font.render_to(screen, (850, 50), str(dino.score), (0, 0, 0))
    else:
        font.render_to(screen, (450, 200), 'Game over', (0, 0, 0))
    pygame.display.flip()
    clock.tick(60)