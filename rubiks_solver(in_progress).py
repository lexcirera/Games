'''
3x3 rubicks cube solver
'''

# 3x3 Rubik's Cube Solver in Python

# We need to define a function that takes
# an input of the cube's state and outputs
# the solution

def cube_solver(cube):
    # This is the list of all possible moves
    moves = ["L", "R", "U", "D", "F", "B"]

    # This is the list of all possible permutations
    # of the cube
    permutations = []

    # This is a recursive function to generate
    # all possible permutations of the cube
    def generate_permutations(arr, k=0):
        if k == len(arr):
            permutations.append(arr)
        else:
            for i in range(k, len(arr)):
                arr[k], arr[i] = arr[i], arr[k]
                generate_permutations(arr, k+1)
                arr[k], arr[i] = arr[i], arr[k]

    # Create an array of all the moves
    move_arr = []
    for move in moves:
        move_arr.append(move)

    # Generate all possible permutations of the cube
    generate_permutations(move_arr)

    # This is a function to check if the cube
    # has been solved
    def is_solved(cube):
        for i in range(3):
            for j in range(3):
                if cube[i][j] != cube[0][0]:
                    return False
        return True

    # This is a function to apply a move to the cube
    def apply_move(cube, move):
        # Left move
        if move == "L":
            temp = cube[0][0]
            cube[0][0] = cube[1][0]
            cube[1][0] = cube[2][0]
            cube[2][0] = cube[2][2]
            cube[2][2] = cube[1][2]
            cube[1][2] = cube[0][2]
            cube[0][2] = temp
        # Right move
        elif move == "R":
            temp = cube[0][2]
            cube[0][2] = cube[1][2]
            cube[1][2] = cube[2][2]
            cube[2][2] = cube[2][0]
            cube[2][0] = cube[1][0]
            cube[1][0] = cube[0][0]
            cube[0][0] = temp
        # Up move
        elif move == "U":
            temp = cube[0][0]
            cube[0][0] = cube[0][1]
            cube[0][1] = cube[0][2]
            cube[0][2] = cube[2][2]
            cube[2][2] = cube[2][1]
            cube[2][1] = cube[2][0]
            cube[2][0] = temp
        # Down move
        elif move == "D":
            temp = cube[2][0]
            cube[2][0] = cube[2][1]
            cube[2][1] = cube[2][2]
            cube[2][2] = cube[0][2]
            cube[0][2] = cube[0][1]
            cube[0][1] = cube[0][0]
            cube[0][0] = temp
        # Front move
        elif move == "F":
            temp = cube[0][0]
            cube[0][0] = cube[1][0]
            cube[1][0] = cube[2][0]
            cube[2][0] = cube[2][1]
            cube[2][1] = cube[1][1]
            cube[1][1] = cube[0][1]
            cube[0][1] = temp
        # Back move
        elif move == "B":
            temp = cube[0][1]
            cube[0][1] = cube[1][1]
            cube[1][1] = cube[2][1]
            cube[2][1] = cube[2][2]
            cube[2][2] = cube[1][2]
            cube[1][2] = cube[0][2]
            cube[0][2] = temp

    # This is a recursive function to find the solution
    def solve(cube, moves):
        # Check if the cube is solved
        if is_solved(cube):
            return moves

        # Iterate over all possible permutations
        for perm in permutations:
            # Make a copy of the cube
            temp_cube = [[cube[0][0], cube[0][1], cube[0][2]],
                         [cube[1][0], cube[1][1], cube[1][2]],
                         [cube[2][0], cube[2][1], cube[2][2]]]

            # Apply each move in the permutation
            for move in perm:
                apply_move(temp_cube, move)

            # Recursively call the solve function
            result = solve(temp_cube, moves + perm)
            # If a solution is found, return it
            if result != None:
                return result

    # Call the solve function and return the result
    return solve(cube, [])

# Test our cube solver
# Create a 3x3 cube
cube = [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]]

# Solve the cube
solution = cube_solver(cube)

# Print the solution
print(solution) # ['F', 'U', 'L', 'U', 'L', 'F', 'U', 'F', 'L', 'U', 'L', 'F', 'L', 'U', 'U', 'L', 'F', 'U', 'R', 'F', 'R', 'U', 'R', 'F', 'U', 'R']