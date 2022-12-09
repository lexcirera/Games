'''
console pacman
'''

import random

# define the board here
board = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3]
]

# define the position of pacman
pacman_row = 1
pacman_col = 1

# define the symbols
SYMBOL_PACMAN = 'P'
SYMBOL_WALL = '#'
SYMBOL_FOOD = '.'

# define the score of game
score = 0

# print the board
def print_board():
    for row in board:
        for col in row:
            if pacman_row == row and pacman_col == col:
                print(SYMBOL_PACMAN, end = " ")
            elif col == SYMBOL_WALL:
                print(SYMBOL_WALL, end = " ")
            elif col == SYMBOL_FOOD:
                print(SYMBOL_FOOD, end = " ")
            else:
                print(' ', end = " ")
        print()

# place the food on board
def place_food():
    food_row = random.randint(0,2)
    food_col = random.randint(0,2)

    board[food_row][food_col] = SYMBOL_FOOD

# move the pacman
def move_pacman(direction):
    global pacman_row
    global pacman_col
    global score

    if direction == 'U':
        if pacman_row == 0:
            pacman_row = 2
        else:
            pacman_row = pacman_row - 1
    elif direction == 'D':
        if pacman_row == 2:
            pacman_row = 0
        else:
            pacman_row = pacman_row + 1
    elif direction == 'L':
        if pacman_col == 0:
            pacman_col = 2
        else:
            pacman_col = pacman_col - 1
    elif direction == 'R':
        if pacman_col == 2:
            pacman_col = 0
        else:
            pacman_col = pacman_col + 1

    # check if pacman eats food
    if board[pacman_row][pacman_col] == SYMBOL_FOOD:
        score += 1
        board[pacman_row][pacman_col] = 0
        place_food()

# main loop of the game
print("Welcome to the Pacman game!")

place_food()

while True:
    print_board()
    print("Score: " + str(score))
    direction = input("Enter direction (U/D/L/R): ").upper()

    move_pacman(direction)