'''
program of a tetris game with gravity rotation and collision detection
'''

#import pygame modules
import pygame
import random

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((600, 600))

#title and icon
pygame.display.set_caption("Tetris")
#icon = pygame.image.load('tetris.png')
#pygame.display.set_icon(icon)

#define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#shapes
shapes = [
    [[1, 1, 1],
    [0, 1, 0]],

    [[2, 2, 2, 2]],

    [[3, 3],
    [3, 3]],

    [[0, 4, 4],
    [4, 4, 0]],

    [[5, 5, 0],
    [0, 5, 5]],

    [[6, 6, 6],
    [0, 0, 6]],

    [[7, 7, 7],
    [7, 0, 0]]
]

#rotate shape
def rotate_shape(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]

#function to check if shape is inside the grid
def check_collision(shape, grid):
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x] != 0:
                if y + pos_y > len(grid) - 1:
                    return True
                if x + pos_x > len(grid[y]) - 1:
                    return True
                if grid[y + pos_y][x + pos_x] != 0:
                    return True
    return False

#create a grid with 10x20
grid = [ [ 0 for x in range(10) ] for y in range(20) ]

#define current_shape and color
current_shape = random.choice(shapes)
current_color = random.choice([red, green, blue])

#define rotation and position
rotation = 0
pos_x = 5
pos_y = 0

#game loop
running = True
while running:
    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pos_x -= 1
                if check_collision(current_shape, grid):
                    pos_x += 1
            if event.key == pygame.K_RIGHT:
                pos_x += 1
                if check_collision(current_shape, grid):
                    pos_x -= 1
            if event.key == pygame.K_DOWN:
                pos_y += 1
                if check_collision(current_shape, grid):
                    pos_y -= 1
            if event.key == pygame.K_UP:
                current_shape = rotate_shape(current_shape)
                if check_collision(current_shape, grid):
                    current_shape = rotate_shape(current_shape)
                    current_shape = rotate_shape(current_shape)
                    current_shape = rotate_shape(current_shape)
    #gravity
    pos_y += 1
    if check_collision(current_shape, grid):
        pos_y -= 1
        for y in range(len(current_shape)):
            for x in range(len(current_shape[y])):
                if current_shape[y][x] != 0:
                    grid[y + pos_y][x + pos_x] = current_shape[y][x]
        current_shape = random.choice(shapes)
        current_color = random.choice([red, green, blue])
        pos_x = 5
        pos_y = 0
    #fill the screen
    screen.fill(black)
    #draw the grid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != 0:
                pygame.draw.rect(screen, white, (x * 30, y * 30, 30, 30), 0)
    #draw the current shape
    for y in range(len(current_shape)):
        for x in range(len(current_shape[y])):
            if current_shape[y][x] != 0:
                pygame.draw.rect(screen, current_color, (x * 30 + pos_x * 30, y * 30 + pos_y * 30, 30, 30), 0)
    pygame.display.update()