import random

# ----------------------------------------- #
#             FUNCTION DETAILS              #
# ----------------------------------------- #
#
# INPUT: state - the current board (20 by 20). [20 by 20 array of integers from 0 to 4]
#        * 0 = empty
#        * 1 = your bot's square
#        * 2 to 4 = other bots' squares
#
#        turns_left - number of turns left. [positive integer from 1 to 260]
#        * 260 to 201 = setup phase
#        * 200 to 1 = attack/decay phase
#
#        last_move - coordinates of your last move. [Tuple of 2 integers from 0 to 19]
#        * Tip: Use this information to plan your next move!
#
# OUTPUT: your move - coordinates of the square you want to color. [Tuple of 2 integers from 0 to 19]
#        * If out of range, defaults to (0,0)
#        * Does not handle invalid types - make sure to abide by the specifications!
#
# ----------------------------------------- #

# NAME: helterskelter
# Randomly picks a square to claim
def helterskelter(state, turns_left, last_move): 
    return (random.randint(0, 19), random.randint(0, 19))

# ----------------------------------------- #

# NAME: foursquare
# Builds 2 by 2 squares randomly
def foursquare(state, turns_left, last_move): 
    step = (last_move[0]%2)+2*(last_move[1]%2)
    if step == 0:
        return (last_move[0]+1, last_move[1])
    if step == 1:
        return (last_move[0]-1, last_move[1]+1)
    if step == 2:
        return (last_move[0]+1, last_move[1])
    if step == 3:
        return (2*random.randint(0, 9), 2*random.randint(0, 9))
    
# ----------------------------------------- #

# NAME: samthesnake
# Makes a random continuous snake w/o bumping into itself
# (If it must crash into walls or itself, game over! Starts anew)
def samthesnake(state, turns_left, last_move): 
    if turns_left >= 260:
        return [random.randint(7, 12), random.randint(7, 12)]
    else:
        for i in range(40): # tries 40 times
            directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
            chosen_direction = directions[random.randint(0, 3)]
            new_x = last_move[0] + chosen_direction[0]
            new_y = last_move[1] + chosen_direction[1]
            if 0 <= new_x < 20 and 0 <= new_y < 20:
                if state[new_x][new_y] != 1:
                    return (new_x, new_y)
        return [random.randint(4, 17), random.randint(4, 17)]

# ----------------------------------------- #

# NAME: denseblock
# Makes a dense 10 by n block in the upper left corner
def denseblock(state, turns_left, last_move):
    for i in range(20):
        for j in range(10):
            if (state[i][j] == 0) or (state[i][j] != 1 and turns_left <= 200):
                return (i, j)
    return (random.randint(0, 19), random.randint(0, 19))

