##########################
## INITIALIZING PLAYERS ##
##########################

import random
import time
from math import log

# import bots
from samplebots import helterskelter
from samplebots import foursquare
from samplebots import samthesnake
from samplebots import denseblock

names = [None]*30

names[0] = 'Helter Skelter'
names[1] = 'Four Square'
names[2] = 'Sam the Snake'
names[3] = 'Dense Block'

def controller(num,state,turns_left,last_move):
    if num == 0:
        return helterskelter(state,turns_left,last_move)
    elif num == 1:
        return foursquare(state,turns_left,last_move)
    elif num == 2:
        return samthesnake(state,turns_left,last_move)
    elif num == 3:
        return denseblock(state,turns_left,last_move)

# Helper function: calculates (in percent) the probability of a square decaying
# Decay list: punish the perimeter; changes over the course of the game
# With no decay multiplier, a 10x10 square will hold up until the end of the game
def prob_decay(gamestate, pos, decay_list):
    x = pos[0]
    y = pos[1]
    adj_same = 0
    for dx in [-1, 1]:
        if 0 <= x+dx < 20:
            adj_same += (gamestate[x+dx][y] == gamestate[x][y])
    for dy in [-1, 1]:
        if 0 <= y+dy < 20:
            adj_same += (gamestate[x][y+dy] == gamestate[x][y])
    return decay_list[adj_same]

# Helper function: calculates the scores of each player
def scores(gamestate):
    total = [1 for i in range(4)]
    checked = [[0 for j in range(len(gamestate[0]))] for i in range(len(gamestate))]
    adj_dir = [[0,1], [0,-1], [1,0], [-1,0]]
    for st_x in range(len(gamestate)):
        for st_y in range(len(gamestate[0])):
            if not checked[st_x][st_y] and gamestate[st_x][st_y] != 0:
                Q = [[st_x, st_y]]
                checked[st_x][st_y] = 1
                color = gamestate[st_x][st_y]
                count = 1
                while len(Q) > 0:
                    cur = Q.pop(0)
                    x = cur[0]
                    y = cur[1]
                    for d in adj_dir:
                        if 0 <= x+d[0] < len(gamestate) and 0 <= y+d[1] < len(gamestate[0]):
                            if gamestate[x+d[0]][y+d[1]] == color and not checked[x+d[0]][y+d[1]]:
                                Q.append([x+d[0], y+d[1]])
                                checked[x+d[0]][y+d[1]] = 1
                                count += 1
                total[color-1] *= count
    return total

# Helper function: converts the gamestate to fit the perspective of a given player (their pieces are "1")
def convert_board(gamestate, player_num):
    player_board = [[0 for i in range(20)] for j in range(20)]
    index_map = [i for i in range(5)]
    index_map[1] = player_num
    index_map[player_num] = 1
    for i in range(20):
        for j in range(20):
            player_board[i][j] = index_map[gamestate[i][j]]
    return player_board

player1 = int(input("Enter the number corresponding to player 1: "))
player2 = int(input("Enter the number corresponding to player 2: "))
player3 = int(input("Enter the number corresponding to player 3: "))
player4 = int(input("Enter the number corresponding to player 4: "))

gamestate = [[0 for i in range(20)] for j in range(20)]
last_moves = [(0,0) for i in range(4)]
decay_multiplier = 4 # factor by which decay is slowed

#########################
## INITIALIZING SCREEN ##
#########################

import pygame
import pygame.gfxdraw
pygame.init()
screen = pygame.display.set_mode((1000,640))
background = pygame.Surface((1000,640))
smallfont = pygame.font.SysFont('arial', 30)
medfont = pygame.font.SysFont('copperplate', 40)
largefont = pygame.font.SysFont('georgia', 60)

colors = [(0,0,0),(250,125,0),(50,50,200),(50,200,50),(200,50,200)]

title = pygame.image.load("title.png").convert_alpha()
background.blit(title,(670,45))
border = pygame.image.load("frame.png").convert_alpha()
background.blit(border,(13,12))
for j in range(0,21):
    pygame.draw.line(background,(80,80,80),(68,62+26*j),(588,62+26*j),1)
    pygame.draw.line(background,(80,80,80),(68+26*j,582),(68+26*j,62),1)

text = medfont.render('Players',1,(255,255,255),(0,0,0))
background.blit(text,(680,170))
text = medfont.render('Scores',1,(255,255,255),(0,0,0))
background.blit(text,(680,400))
for j in range(0,4):
    pygame.gfxdraw.aacircle(background,700,240+40*j,15,colors[j+1])
    pygame.gfxdraw.filled_circle(background,700,240+40*j,15,colors[j+1])
    pygame.gfxdraw.aacircle(background,700,470+40*j,15,colors[j+1])
    pygame.gfxdraw.filled_circle(background,700,470+40*j,15,colors[j+1])
text = smallfont.render(names[player1],1,(255,255,255),(0,0,0))
background.blit(text,(725,223))
text = smallfont.render(names[player2],1,(255,255,255),(0,0,0))
background.blit(text,(725,263))
text = smallfont.render(names[player3],1,(255,255,255),(0,0,0))
background.blit(text,(725,303))
text = smallfont.render(names[player4],1,(255,255,255),(0,0,0))
background.blit(text,(725,343))

def display(gamestate):
    screen.blit(background, (0,0))
    for j in range(20):
        for k in range(20):
            if gamestate[j][k] != 0:
                pygame.gfxdraw.aacircle(screen,81+26*j,75+26*k,10,colors[gamestate[j][k]])
                pygame.gfxdraw.filled_circle(screen,81+26*j,75+26*k,10,colors[gamestate[j][k]])
    for j in range(19):
        for k in range(20):
            occ1 = gamestate[j][k]
            occ2 = gamestate[j+1][k]
            if occ1 == occ2 and occ1:
                pygame.draw.rect(screen,colors[occ1],(81+26*j,65+26*k,26,21))
    for j in range(20):
        for k in range(19):
            occ1 = gamestate[j][k]
            occ2 = gamestate[j][k+1]
            if occ1 == occ2 and occ1:
                pygame.draw.rect(screen,colors[occ1],(71+26*j,75+26*k,21,26))
    for j in range(19):
        for k in range(19):
            occ1 = gamestate[j][k]
            occ2 = gamestate[j][k+1]
            occ3 = gamestate[j+1][k]
            occ4 = gamestate[j+1][k+1]
            if occ1 == occ2 == occ3 == occ4 and occ1:
                pygame.draw.rect(screen,colors[occ1],(81+26*j,75+26*k,26,26))
    scrnums = scores(gamestate)
    for j in range(0,4):
        text = smallfont.render(str(scrnums[j]),1,(255,255,255),(0,0,0))
        width = text.get_width()
        screen.blit(text,(900-width,453+40*j))

    pygame.display.flip()


#################################################
## PLAYERS POPULATE THE GAME BOARD WITH PIECES ##
#################################################

for j in range(0,60):
    (ra,pa) = controller(player1,convert_board(gamestate, 1),260-j,last_moves[0])
    (rb,pb) = controller(player2,convert_board(gamestate, 2),260-j,last_moves[1])
    (rc,pc) = controller(player3,convert_board(gamestate, 3),260-j,last_moves[2])
    (rd,pd) = controller(player4,convert_board(gamestate, 4),260-j,last_moves[3])

    # Place the pieces at positions unclaimed
    # queries with the same position are equally likely to get it
    queries = [(ra,pa), (rb,pb), (rc,pc), (rd,pd)]
    for k in range(len(queries)):
        if not (0 <= queries[k][0] < 20 and 0 <= queries[k][1] < 20):
            queries[k] = (0,0)
    last_moves = queries
    queries_dict = {}
    for k in range(0,4):
        if queries[k] in queries_dict.keys():
            queries_dict[queries[k]].append(k+1)
        else:
            queries_dict[queries[k]] = [k+1]
    for pos in queries_dict.keys():
        if gamestate[pos[0]][pos[1]] == 0:
            piece = random.randint(0, len(queries_dict[pos])-1)
            gamestate[pos[0]][pos[1]] = queries_dict[pos][piece]

##    # text graphics
##    string_print = ""
##    string_print += "------------------------------------------ \n"
##    for k in range(20):
##        string_print += str(gamestate[k]) + "\n"
##    print(string_print)

    # update graphics screen
    display(gamestate)
    
    # delay
    time.sleep(0.05)

# big print and delay (for testing/aesthetic purposes)
print("Decay is now active")
time.sleep(2)

##############################################################
## PLAYERS CONTINUE TO POPULATE GAME BOARD; DECAY IS ACTIVE ##
##############################################################

for j in range(0,200):
    (ra,pa) = controller(player1,convert_board(gamestate, 1),200-j,last_moves[0])
    (rb,pb) = controller(player2,convert_board(gamestate, 2),200-j,last_moves[1])
    (rc,pc) = controller(player3,convert_board(gamestate, 3),200-j,last_moves[2])
    (rd,pd) = controller(player4,convert_board(gamestate, 4),200-j,last_moves[3])

    # Place the pieces at positions (any)
    # queries with the same position are equally likely to get it
    queries = [(ra,pa), (rb,pb), (rc,pc), (rd,pd)]
    for k in range(len(queries)):
        if not (0 <= queries[k][0] < 20 and 0 <= queries[k][1] < 20):
            queries[k] = (0,0)
    last_moves = queries
    queries_dict = {}
    for k in range(0,4):
        if queries[k] in queries_dict.keys():
            queries_dict[queries[k]].append(k+1)
        else:
            queries_dict[queries[k]] = [k+1]

    for pos in queries_dict.keys():

        # if blank, then automatic claim
        if gamestate[pos[0]][pos[1]] == 0:
            N = 100

        # if occupied, every player contesting the square adds 40 percent probability of claiming it
        else:
            N = 40*len(queries_dict[pos])

        # if decay is successful, a random contesting player gets it
        # if the player owning the square "claims" it, then square is decayed
        if random.randint(0,99) < N:
            piece = random.randint(0, len(queries_dict[pos])-1)
            if gamestate[pos[0]][pos[1]] == queries_dict[pos][piece]:
                gamestate[pos[0]][pos[1]] = 0
            else:
                gamestate[pos[0]][pos[1]] = queries_dict[pos][piece]

    # Decay squares

    num_pieces = sum([sum([gamestate[a][b] > 0 for b in range(20)]) for a in range(20)])
    decay_multiplier = (1100 / (num_pieces + 100)) # ranges from 2.2 to 11; expect around 4
    decay_list = (([5,4,2,1,0] if j < 80 else [8,6,4,3,1]) if j < 195 else [10,8,12,8,3])
    # Different phases for decay_list for a given number of moves done (j):
    # 0-79 = [5,4,2,1,0], 80-194 = [8,6,4,3,1], 195-199 = [10,8,12,8,3]
    new_gamestate = [[0 for i in range(20)] for j in range(20)]
    for x in range(0,20):
        for y in range(0,20):
            if not (random.randint(0,int(decay_multiplier*100-1)) < prob_decay(gamestate, [x,y], decay_list)): # decay multiplier used here
                 new_gamestate[x][y] = gamestate[x][y]
    gamestate = new_gamestate

##    # text graphics
##    string_print = ""
##    string_print += "------------------------------------------ \n"
##    for k in range(20):
##        string_print += str(gamestate[k]) + "\n"
##    print(string_print)

    # update graphics screen
    display(gamestate)
    
    # delay
    time.sleep(0.05)
    
# display log_2 of final scores, for overall tournament standings
j = 0
for num in scores(gamestate):
    print("Player",j,"log score is",round(log(num,2),2))
    j += 1


################################################
## USER WILL PRESS ESC TO CLOSE PYGAME WINDOW ##
################################################

mainloop = True
while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
pygame.quit()

