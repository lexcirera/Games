import pygame
import random

# screen size
WIDTH = 600
HEIGHT = 600

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game objects
player = None
enemies = []
bullets = []

def init():
    global player
    player = Player()

def create_enemies():
    global enemies
    for i in range(5):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        enemies.append(Enemy(x, y))

def draw():
    screen.fill(BLACK)

    # draw player
    player.draw()

    # draw enemies
    for enemy in enemies:
        enemy.draw()

    # draw bullets
    for bullet in bullets:
        bullet.draw()

    # update screen
    pygame.display.flip()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    return True

class Player:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 5
        self.size = (20, 20)

    def draw(self):
        rect = (self.x, self.y, self.size[0], self.size[1])
        pygame.draw.rect(screen, WHITE, rect)

    def shoot(self):
        global bullets
        x = self.x + self.size[0] / 2
        y = self.y
        bullets.append(Bullet(x, y))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.size = (20, 20)

    def draw(self):
        rect = (self.x, self.y, self.size[0], self.size[1])
        pygame.draw.rect(screen, WHITE, rect)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.size = (10, 10)

    def draw(self):
        rect = (self.x, self.y, self.size[0], self.size[1])
        pygame.draw.rect(screen, WHITE, rect)
##
# initialize game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()
##
# game loop
init()
create_enemies()
a=input()
while True:
    if handle_events() == False:
        break

    draw()