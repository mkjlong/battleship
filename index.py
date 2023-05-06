###################################################
#                                                 #
#                  BATTLESHIP GAME                #
# ----------------------------------------------- #
#                                                 #
#                        BY:                      #
#              Markus , Sarah , Max               #
#                                                 #
#                                                 #
#   Started On:                       Ended On:   #
#   Apr 17 2023                      May 2 2023   #
#                                                 #
#                                                 #
###################################################




# ----------------------SETTINGS-------------------#

# if we have to put our boats in the other player's game, set this value to true

SHOW_BOATS_IN_CONSOLE = False


# toggle max's weird things
DO_EASTER_BUNNY = False

DO_TRAP_CARD = False

TOURNAMENT_MODE = False


# -----------------------IMPORTS-------------------#

import sys
import pygame
from random import randint
from random import choice
from pygame.locals import QUIT
from math import floor
from datetime import datetime


# -------------------------------------------------#

# --------------------CONSTANTS--------------------#


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 60

# colours
WHITE = (255, 255, 255)
RED = (250, 10, 11)
BLACK = (0, 0, 0)
AQUA = (0, 255, 255)



#timer
start_time = datetime.now()

# images
cat = pygame.image.load("cat.png")
cardBack = pygame.image.load("Yu-Gi-Oh Card Back.png")
trapHole = pygame.image.load("Trap Hole.png")

#gifs
title_images = []


for i in range(84):
    img = pygame.image.load(f"title_background/{i}.png")
    title_images.append(img)

game_images = []

for i in range(8):
    img = pygame.image.load(f"game_background/{i}.png")
    game_images.append(img)

end_images = []

for i in range(40):
    img = pygame.image.load(f"end_background/{i}.png")
    end_images.append(img)

# -------------------------------------------------#

# ---------------PYGAME INTIALIZATION--------------#

pygame.init()

gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Battleship Game')
grid_font = pygame.font.Font("fonts/hagne.ttf", 25)
title_font = pygame.font.Font("fonts/carbon.ttf", 150)
header_font = pygame.font.Font("fonts/hagne.ttf", 70)
header_2_font = pygame.font.Font("fonts/hagne.ttf", 25)
header_3_font = pygame.font.Font("fonts/hagne.ttf", 30)
text_font_1 = pygame.font.Font("fonts/hagne.ttf", 10)

small_font = pygame.font.SysFont("Roboto", 25)


# -------------------------------------------------#

# --------------------VARIABLES--------------------#

# all default starting variable values

pygame_input = "playerSelection"
# input is for when asking for who goes first, asking for if the ai hit a boat, and for what type

starting_player = "Player"
trapcard = True

playerShotsMade = 0  # how many shots have been taken
playerNumHit = 0  # how many shots have hit
playerNumMiss = 0  # how many shots have missed

# ai statistics
aiShotsMade = 0
aiNumHit = 0
aiNumMiss = 0

# All valid coords that the AI hasn't shot yet
remainingCoords = [
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10",
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10",
    "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10",
    "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10",
    "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10",
    "J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9", "J10"]


# temporary variable for testing
# all previous AI hits
# ai_choices = []


# stores all AI boat coordinates
all_ai_boat_coords = []


player_grid = []
# example
# [("A1","battleship"),("A2","battleship"),("F6","destroyer"), ("B1","miss")]
# ((coord), (miss|boattype))

ai_grid_full = []
# has the location of all the boat coords.
# [(["A1","B1","C1","D1","E1"],"carrier")]
# has a different format than player_grid and ai_grid_display, since all the information is already avaliable here, and doesn't need to display missed shots.

# same as player_grid, only has the information avaliable to the opponent
ai_grid = []


# the ai's choice
ai_move = "A1"


# either player, or ai
turn = "player"



#text animation (when the player clicks a tile, an animation will appear of what boat you clicked)
animation_time = 0
doTextAnimation = False
text_anmiation_content = "miss!"
# the main while loop stops when this value is set to true
gameOver = False


# -------------------------------------------------#

# ----------------PYGAME FUNCTIONS-----------------#


# draws a text, and centers it horizontally and vertically
def centerText(text, x, y, center_x=True, center_y=True):
    if (center_x):
        x = x - text.get_width()/2
    if (center_y):
        y = y - text.get_height()/2
    gameWindow.blit(text, (x, y))


def drawCounters(turn):
    # draws a counter on top of the grid that was hit
    if (turn == "player"):
        grid = player_grid
    else:
        grid = ai_grid
    for boat in grid:
        coord = boat[0]
        boat_type = boat[1]

        x = 100 + int(getX(coord))*60
        y = 100 + int(LetterToNum(getY(coord)))*60

        if (boat_type == "miss") or TOURNAMENT_MODE == True:
            pygame.draw.circle(gameWindow, (32,32,150), (x, y), 25)

        else:  # boat hit
            if((turn == "ai" and getAiBoatHitsRemaining(boat_type)==0) or (turn == "player" and getPlayerBoatHitsRemaining(boat_type)==0)):
                #boat sunk
                pygame.draw.circle(gameWindow, (64,64,64), (x, y), 25)
            else:
                #boat hit (not sunk)
                pygame.draw.circle(gameWindow, (128,0,0), (x, y), 25)

# draws the grid


def drawGrid():

    for i in range(1, 11):
        # horzontal lines
        pygame.draw.line(gameWindow, (100,100,125), (i*GRID_SIZE+70, 0+70), (i*GRID_SIZE+70, GRID_SIZE*11+70), 2)

        # render the text as graphics
        turn_number = grid_font.render(str(i), 1, (255,255,255))
        centerText(turn_number, i*GRID_SIZE+100, 105)

        # vertical lines
        pygame.draw.line(gameWindow, (100,100,125), (70, i*GRID_SIZE+70), (GRID_SIZE*11+70, i*GRID_SIZE+70), 2)

        # render the text as graphics
        turn_letter = grid_font.render(NumToLetter(i), 1, (255,255,255))
        centerText(turn_letter, 100, i*GRID_SIZE+100)

    # draws the borders (grid borders aren't being blitted in the for loop)
    pygame.draw.rect(gameWindow, (100,100,130), (70, 70, GRID_SIZE*11, GRID_SIZE*11), 5)


# displays statistics of game
def drawStats():
    playerShot = str(getPlayerShots())
    aiShot = str(getAIShots())

    playerHit = str(getPlayerHits())
    aiHit = str(getAIHits())

    playerMiss = str(getPlayerMisses())
    aiMiss = str(getAIMisses())

    playerBoats = str(getPlayerBoatsRemaining())
    aiBoats = str(getAiBoatsRemaining())

    pygame.draw.line(gameWindow, WHITE, (267, 200), (267, 800), 6)
    pygame.draw.line(gameWindow, WHITE, (533, 200), (533, 800), 6)
    pygame.draw.line(gameWindow, WHITE, (0, 250), (800, 250), 6)

    ai_text = header_2_font.render("AI", True, WHITE)
    centerText(ai_text,400,230)

    player_text = header_2_font.render("PLAYER", True, WHITE)
    centerText(player_text,667,230)


    if(time_since_game_end > 6):
        shots_fired = header_2_font.render("SHOTS FIRED", True, WHITE)
        centerText(shots_fired,133,290)

        player_shots_fired = header_3_font.render(playerShot, True, WHITE)
        centerText(player_shots_fired,400,290)

        ai_shots_fired = header_3_font.render(aiShot, True, WHITE)
        centerText(ai_shots_fired,667,290)
    if(time_since_game_end > 7):
        shots_hit = header_2_font.render("SHOTS HIT", True, WHITE)
        centerText(shots_hit,133,330)

        player_shots_hit = header_3_font.render(playerHit, True, WHITE)
        centerText(player_shots_hit,400,330)

        ai_shots_hit = header_3_font.render(aiHit, True, WHITE)
        centerText(ai_shots_hit,667,330)
    if(time_since_game_end > 8):
        shots_missed = header_2_font.render("SHOTS MISSED", True, WHITE)
        centerText(shots_missed,133,370)

        player_shots_miss = header_3_font.render(playerMiss, True, WHITE)
        centerText(player_shots_miss,400,370)

        ai_shots_miss = header_3_font.render(aiMiss, True, WHITE)
        centerText(ai_shots_miss,667,370)
    if(time_since_game_end > 9.5):
        boats_left = header_2_font.render("BOATS LEFT", True, WHITE)
        centerText(boats_left,133,450)

        player_boats_left = header_3_font.render(aiBoats, True, WHITE)
        centerText(player_boats_left,400,450)

        ai_boats_left = header_3_font.render(playerBoats, True, WHITE)
        centerText(ai_boats_left,667,450)




# draws the header text
def drawHeader():
    if (turn == "player"):
        text_content = "ATTACK"
        color = (255,32,32)
    else:
        text_content = "DEFEND"
        color = (32,32,255)
    text = header_3_font.render(text_content, 1, color)
    #pygame.draw.rect(gameWindow, (255, 255, 255), (340, 5, 120, 60), 7, 10)
    centerText(text,400,35)


def drawTextAnimation():
    global animation_time, doTextAnimation, turn
    text = small_font.render(text_anmiation_content,True, (255,255,255))
    x = text_animation_location[0]
    y = text_animation_location[1] -50  - 50*  (animation_time)**3
    opacity = max(255 - 100*(animation_time)**3,0)
    text.set_alpha(opacity)
    centerText(text,x,y)


    animation_time+=0.002

    if(animation_time>=1.5):
        doTextAnimation = False
        turn = "ai"

def trapcard():
    if (not DO_TRAP_CARD):
        return
    gameWindow.blit(cardBack, (250, 200))
    pygame.display.update()
    pygame.time.delay(1500)
    trap = header_font.render("I activate my", 1, WHITE)
    card = header_font.render("TRAP CARD: TRAP HOLE!", 1, WHITE)
    gameWindow.blit(trap, (150, 300))
    gameWindow.blit(card, (100, 350))
    pygame.display.update()
    pygame.time.delay(1500)
    gameWindow.blit(trapHole, (250, 200))
    pygame.display.update()
    pygame.time.delay(3500)


# -------------------------------------------------#

# ---------------------FUNCTIONS-------------------#


# How many AI boats remain
def getAiBoatsRemaining():
    boats = 5
    if TOURNAMENT_MODE == True:
        boats = 100
    for type in ["destroyer", "cruiser", "submarine", "battleship", "carrier"]:
        if (getAiBoatHitsRemaining(type) == 0):
            boats -= 1
    if secrets.upper() == "ICBM" and turn == "ai":
        boats = 0
    return boats


# moves the coordinate by a certain amount
def shiftCoordinate(coordinate, direction, amount):  # shiftCoordinate("A4","up",3) => A1
    shiftX = 0
    shiftY = 0
    if (direction == "up"):
        shiftY = -1
    elif (direction == "down"):
        shiftY = 1
    elif (direction == "left"):
        shiftX = -1
    elif (direction == "right"):
        shiftX = 1

    coordX = int(getX(coordinate))
    coordY = getY(coordinate)

    coordX += shiftX

    coordY = incrementLetter(coordY, shiftY)

    return coordY + str(coordX)


# --------------------STATS FUNCTIONS--------------------#


def getPlayerShots():
    return len(player_grid)


def getAIShots():
    return len(ai_grid)


def getPlayerHits():
    hits = 0
    for boat in player_grid:
        if (boat[1] != "miss"):
            hits += 1
    return hits


def getAIHits():
    hits = 0
    for boat in ai_grid:
        if (boat[1] != "miss"):
            hits += 1
    return hits


def getPlayerMisses():
    misses = 0
    for boat in player_grid:
        if (boat[1] == "miss"):
            misses += 1
    return misses


def getAIMisses():
    misses = 0
    for boat in ai_grid:
        if (boat[1] == "miss"):
            misses += 1
    return misses


# Gets the amount of boats the player still has
def getPlayerBoatsRemaining():
    boats = 5
    for type in ["battleship", "cruiser", "submarine", "destroyer", "carrier"]:
        if (getPlayerBoatHitsRemaining(type) == 0):
            boats -= 1
    return boats


# example: if the carrier has been hit once, it will return 4 (need to hit the carrier 4 more times to sink)
def getPlayerBoatHitsRemaining(boat_type):
    boatCount = getBoatLength(boat_type)
    for boat in player_grid:
        if (boat[1] != boat_type):
            continue
        else:
            boatCount -= 1
    return boatCount


# Gets the amount of boats the AI still has
def getAiBoatHitsRemaining(boat_type):
    boats_left = getBoatLength(boat_type)

    for boat in ai_grid:
        # ai_grid_display = [("A1", "carrier"),("A2","carrier"),("A3","carrier","A4","carrier","A5","carrier")]
        if (boat[1] == boat_type):
            boats_left -= 1
    return boats_left


# Checks for duplicate coordinates
def checkDupeBoatCoords(boatcoords):
    if (len(boatcoords) == 0):
        return True
    dupe = False
    for coord in boatcoords:
        if (boatcoords.count(coord) > 1):
            dupe = True
    return dupe


# get the length of a boat type
def getBoatLength(boat_type):
    if (boat_type == "carrier"):
        return 5
    elif (boat_type == "battleship"):
        return 4
    elif (boat_type == "cruiser"):
        return 3
    elif (boat_type == "submarine"):
        return 3
    elif (boat_type == "destroyer"):
        return 2


# 1 => A, 2=> B, 3=> C etc...
def NumToLetter(num):
    return chr(64 + num)


# A => 1, B=> 2, C=> 3 etc...
def LetterToNum(chr):
    return ord(chr) - 64


# add function but for letters
def incrementLetter(char, n):
    return chr(ord(char) + n)


# gets the X value of a coordinate
def getX(location):  # getX("A1") => 1
    if (type(location) == str):  # location = A1
        return location[1:]
    else:  # location==("A","1")
        return location[1]


# gets the Y value of a coordinate
def getY(location):  # getY("A1") => A
    return location[0]


# generates the AI boats (randomly)
def generateBoat(boat_type):
    length = getBoatLength(boat_type)
    startingX = randint(1, 11 - length)
    startingY = NumToLetter(randint(1, 11 - length))  # random between A and J
    boatDirection = choice(["vertical", "horizontal"])
    boatpositions = []

    # duplicate = True
    # while duplicate==True:
    for i in range(length):
        if (boatDirection == "vertical"):
            coord = (incrementLetter(startingY, i)+str(startingX))
        elif (boatDirection == "horizontal"):
            coord = (startingY + str(startingX + i))
        boatpositions.append(coord)
        all_ai_boat_coords.append(coord)

    return (boatpositions, boat_type)


# finds the coordinate of the mouse click in reference to the grid
def getMouseCoords():
    # 60-120 = 1, 120-180=2  etc..
    pos = pygame.mouse.get_pos()
    x = pos[0]-70
    y = pos[1]-70
    y = NumToLetter(min(max(floor(y/60), 1), 10))
    x = str(min(max(floor(x/60), 1), 10))
    return (y, x)


# orders each grid of the boat inputted
def sortBoats(boat):
    return boat[0]


# the ai fires in a checkboard pattern, and this function juts checks which ones to fire at random
def checkIfCoordIsOdd(coord):
    x = int(getX(coord))
    y = int(LetterToNum(getY(coord)))
    return ((x+y) % 2 == 0)

# -------------------- AI --------------------#

# chooses a (not very) optional location for computer to shoot at


def AIChoice():
    player_grid.sort(key=sortBoats)

    # sorts the boats in order of gruid (A1, A2, A3, A4, etc...)
    targets = []

    ai_choice = "A1"  # temp
    targetBoat = ""

    # check if we have to still try to hunt for the boat anymore
    for boat in player_grid:
        boatType = boat[1]
        if (boatType == "miss"):
            continue

        if (getPlayerBoatHitsRemaining(boatType) == getBoatLength(boatType)):
            continue

        if (getPlayerBoatHitsRemaining(boatType) <= 0):
            # print("it sunk")
            continue

        targetBoat = boatType

    if (targetBoat == ""):
        # no boats have been found (that hasnt been sunk)
        targets.append(choice(list(filter(checkIfCoordIsOdd, remainingCoords))))

    else:
        # hit a boat that hasnt been sunk, now hunting to kill the boat
        hitboats = []
        for boat in player_grid:
            if (boat[1] == targetBoat):
                hitboats.append(boat)
        if (len(hitboats) >= 2):
            # we know the direction of the boat
            # get the common coordionate (get the direction of the boat)
            direction = ""

            firstBoatLocation = hitboats[0][0]
            # hitboats[-1] is the same as hitboats[len(hitboats)-1]
            lastBoatLocation = hitboats[-1][0]

            if (getX(firstBoatLocation) != getX(lastBoatLocation)):
                direction = "horizontal"
            else:
                direction = "vertical"
            # print("boat direction is " + direction)
            if (direction == "horizontal"):
                target1 = shiftCoordinate(firstBoatLocation, "left", 1)
                target2 = shiftCoordinate(lastBoatLocation, "right", 1)
                targets.append(target1)
                targets.append(target2)
            else:
                target1 = shiftCoordinate(firstBoatLocation, "up", 1)
                target2 = shiftCoordinate(lastBoatLocation, "down", 1)
                targets.append(target1)
                targets.append(target2)
        else:  # we have already hit one location, but we cant find direction of boat
            boatlocation = hitboats[0][0]
            target1 = shiftCoordinate(boatlocation, "left", 1)
            target2 = shiftCoordinate(boatlocation, "right", 1)
            target3 = shiftCoordinate(boatlocation, "up", 1)
            target4 = shiftCoordinate(boatlocation, "down", 1)

            targets.append(target1)
            targets.append(target2)
            targets.append(target3)
            targets.append(target4)

    # remove illegal and already hit location
    for coord in targets[:]:
        if (coord not in remainingCoords):
            targets.remove(coord)
    if (len(targets) != 0):
        ai_choice = choice(targets)
        remainingCoords.remove(ai_choice)
        return ai_choice
    else:
        print("opponent resigns because they inputted incorrectly :)")
        return "nothing"

        # sometimes doesn't work when user inputs incorrectly (illegally). pls dont :D



# -------------------------------------------------#

# -------------------MAIN PROGRAM------------------#

# generates all 5 boats of ai




while checkDupeBoatCoords(all_ai_boat_coords):
    all_ai_boat_coords = []
    ai_grid_full = []

    for boat_type in ["carrier", "battleship", "cruiser", "submarine", "destroyer"]:
        ai_grid_full.append(generateBoat(boat_type))


if (SHOW_BOATS_IN_CONSOLE):
    for boat in ai_grid_full:
        print(boat[0] + " is at " + ", ".join(boat[1]))


# -----VIRUS INJECTED BY THE EASTER BUNNY-------#
if (DO_EASTER_BUNNY):
    secrets = input("")
    if secrets.upper() == "CLASH ROYALE":
        TOURNAMENT_MODE = True
else:
    secrets = ""
# -------------------- GAME --------------------#



text_animation_location = pygame.mouse.get_pos()
while gameOver != True:





    gameWindow.fill("#FFFFFF")
    # all images & grid
    frame = floor(( (datetime.now() - start_time).total_seconds() * 50) % 7)
    gameWindow.blit(game_images[frame], (0,0))
    gameWindow.blit(cat, (71, 70))
    drawGrid()

    
    # if it is the players turn
        


    if (pygame_input == "playerSelection"):
        # -------------------- TITLE SCREEN --------------------#
        frame = floor(( (datetime.now() - start_time).total_seconds() * 10 ) % 83)
        #gets the frame to display on the gif, where 10 is the amount of delay (1/10 of a second), and 83 is the length of the gif
        
        
        gameWindow.blit(title_images[frame], (0,0))
        title_text = title_font.render("BATTLESHIP",True,(100,100,100))
        title_text.set_alpha(150)

        centerText(title_text,400,200)

        
        player_hitbox = pygame.draw.rect(gameWindow,(32,32,32),(150,350,200,100),3,5)
        ai_hitbox = pygame.draw.rect(gameWindow,(32,32,32),(450,350,200,100),3,5)

        player_text = header_2_font.render("Player", True, (255,255,255))
        player_text.set_alpha(200)
        ai_text = header_2_font.render("Computer", True, (255,255,255))
        ai_text.set_alpha(200)

        centerText(player_text,250,400)
        centerText(ai_text,550,400)


        if(player_hitbox.collidepoint(pygame.mouse.get_pos())):
            player_hitbox = pygame.draw.rect(gameWindow,(255,255,255),(150,350,200,100),5,5)
            player_text.set_alpha(255)
            centerText(player_text,250,400)
            
            if(pygame.mouse.get_pressed()[0]):
                #clicked player
                pygame_input=""
                turn = "player"
                pygame.time.delay(150)
        elif(ai_hitbox.collidepoint(pygame.mouse.get_pos())):
            ai_hitbox = pygame.draw.rect(gameWindow,(255,255,255),(450,350,200,100),5,5)
            ai_text.set_alpha(255)
            centerText(ai_text,550,400)
            
            if(pygame.mouse.get_pressed()[0]):
                #clicked player
                pygame_input=""
                turn = "ai"
                pygame.time.delay(150)
        

        pygame.display.update()


    # -------------------- HITBOAT --------------------#

    # if button clicked is a hitbox for boat
    elif(pygame_input == "hitboat"):
        drawCounters("player")
        if (doTextAnimation):
            drawTextAnimation()
            if(animation_time>1.5):
                doTextAnimation=False
                pygame_input=""
                turn="player"
        else:
            animation_time=0
            drawHeader()
            if(ai_move!="nothing"):
                pygame.draw.circle(gameWindow,(100,100,100),(100 + int(getX(ai_move))*60,100 + int(LetterToNum(getY(ai_move)))*60),25)
            #^ draws a gray circle in the ai_move location, indicating we dont know the state of that tile yet

            invisible_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            invisible_rect.set_alpha(100)
            invisible_rect.fill((0, 0, 0))
            gameWindow.blit(invisible_rect, (0, 0))

            # -------------------- AI'S MOVE --------------------#

            # displays where the ai hits
            prompt = header_2_font.render("AI HITS", 1, (255, 255, 255))
            centerText(prompt,400,240)

            prompt2 = header_font.render(str(ai_move), 1, (255,255,255))
            centerText(prompt2,400,300)

            pygame.draw.rect(gameWindow,(255,255,255),((250,200,300,300)),7,20)


            if(ai_move != "nothing"):
                # draws buttons for hitting or missing
                button_hit = pygame.draw.rect(
                    gameWindow, (32, 255, 32), (300, 400, 80, 50), 3, 5)
                button_miss = pygame.draw.rect(
                    gameWindow, (255, 32, 32), (420, 400, 80, 50), 3, 5)

                text_hit = grid_font.render("HIT", 1, (255, 255, 255))
                text_miss = grid_font.render("MISS", 1, (255, 255, 255))

                gameWindow.blit(text_hit, (340-(text_hit.get_width()/2),
                                425-(text_hit.get_height()/2)))
                gameWindow.blit(text_miss, (460-(text_miss.get_width()/2),
                                425-(text_miss.get_height()/2)))

                # if player selected hit or miss buttons
                for event in pygame.event.get():
                    if (event.type == pygame.MOUSEBUTTONUP):
                        if (button_hit.collidepoint(pygame.mouse.get_pos())):
                            pygame_input = "hitwhat"
                        elif (button_miss.collidepoint(pygame.mouse.get_pos())):
                            hitboat = (ai_move, "miss")
                            player_grid.append(hitboat)

                            # changes who's turn it is
                            doTextAnimation = True
                            text_anmiation_content = "miss"
                            text_animation_location = (100 + int(getX(ai_move))*60, 100 + int(LetterToNum(getY(ai_move)))*60)

                        pygame.event.clear()

                pygame.display.update()
        

    elif (pygame_input == "hitwhat"):  # if the ai hit a player's boat
        drawCounters("player")
        if (doTextAnimation):
            drawTextAnimation()
            if(animation_time>1.5):
                doTextAnimation=False
                pygame_input=""
                turn="player"
        else:
            pygame.draw.circle(gameWindow,(100,100,100),(100 + int(getX(ai_move))*60,100 + int(LetterToNum(getY(ai_move)))*60),25)
            
            invisible_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            invisible_rect.set_alpha(100)
            invisible_rect.fill((0, 0, 0))
            gameWindow.blit(invisible_rect, (0, 0))
            pygame.draw.rect(gameWindow, (255, 255, 255), (100, 250, 600, 300), 5, 50)
            prompt = header_3_font.render("What did the AI hit", 1, (255, 255, 255))
            centerText(prompt,400,310)

            # all temporary, draws a rectangle outside the border so it doesnt display, gets updated after
            button_carrier = pygame.draw.rect(gameWindow, (0, 0, 0), (1, 1, 1, 1))
            button_battleship = pygame.draw.rect(
                gameWindow, (0, 0, 0), (1, 1, 1, 1))
            button_cruiser = pygame.draw.rect(gameWindow, (0, 0, 0), (1, 1, 1, 1))
            button_submarine = pygame.draw.rect(
                gameWindow, (0, 0, 0), (1, 1, 1, 1))
            button_destroyer = pygame.draw.rect(
                gameWindow, (0, 0, 0), (1, 1, 1, 1))

            text_carrier = text_font_1.render("", 1, (255, 255, 255))
            text_battleship = text_font_1.render("", 1, (255, 255, 255))
            text_cruiser = text_font_1.render("", 1, (255, 255, 255))
            text_submarine = text_font_1.render("", 1, (255, 255, 255))
            text_destroyer = text_font_1.render("", 1, (255, 255, 255))

            # if carrier still exists, displays carrier button
            if (getPlayerBoatHitsRemaining("carrier") >= 1):
                button_carrier = pygame.draw.rect(
                    gameWindow, (255,255,255), (120, 400, 80, 50), 3, 5)
                text_carrier = text_font_1.render("carrier", 1, (255, 255, 255))
            if (getPlayerBoatHitsRemaining("battleship") >= 1):
                # if battleship still exists, displays battleship button
                button_battleship = pygame.draw.rect(
                    gameWindow, (255,255,255), (240, 400, 80, 50), 3, 5)
                text_battleship = text_font_1.render("battleship", 1, (255, 255, 255))
            if (getPlayerBoatHitsRemaining("cruiser") >= 1):
                # if cruiser still exists, displays cruiser button
                button_cruiser = pygame.draw.rect(
                    gameWindow, (255,255,255), (360, 400, 80, 50), 3, 5)
                text_cruiser = text_font_1.render("cruiser", 1, (255, 255, 255))
            if (getPlayerBoatHitsRemaining("submarine") >= 1):
                # if submarine still exists, displays submarine button
                button_submarine = pygame.draw.rect(
                    gameWindow, (255,255,255), (480, 400, 80, 50), 3, 5)
                text_submarine = text_font_1.render("submarine", 1, (255, 255, 255))
            if (getPlayerBoatHitsRemaining("destroyer") >= 1):
                # if destroyer still exists, displays destroyer button
                button_destroyer = pygame.draw.rect(
                    gameWindow, (255,255,255), (600, 400, 80, 50), 3, 5)
                text_destroyer = text_font_1.render("destroyer", 1, (255, 255, 255))

            gameWindow.blit(text_carrier, (160-(text_carrier.get_width()/2),
                            425-(text_carrier.get_height()/2)))
            gameWindow.blit(text_battleship, (280-(text_battleship.get_width()/2),
                            425-(text_battleship.get_height()/2)))
            gameWindow.blit(text_cruiser, (400-(text_cruiser.get_width()/2),
                            425-(text_cruiser.get_height()/2)))
            gameWindow.blit(text_submarine, (520-(text_submarine.get_width()/2),
                            425-(text_submarine.get_height()/2)))
            gameWindow.blit(text_destroyer, (640-(text_destroyer.get_width()/2),
                            425-(text_destroyer.get_height()/2)))

            for event in pygame.event.get():
                # When mouse click has been released
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if (button_carrier.collidepoint(pygame.mouse.get_pos())):
                        hitboat_type = "carrier"
                    elif (button_battleship.collidepoint(pygame.mouse.get_pos())):
                        hitboat_type = "battleship"
                    elif (button_cruiser.collidepoint(pygame.mouse.get_pos())):
                        hitboat_type = "cruiser"
                    elif (button_submarine.collidepoint(pygame.mouse.get_pos())):
                        hitboat_type = "submarine"
                    elif (button_destroyer.collidepoint(pygame.mouse.get_pos())):
                        hitboat_type = "destroyer"
                    else:
                        continue
                    hitboat = (ai_move, hitboat_type)
                    player_grid.append(hitboat)
                    doTextAnimation = True
                    if (getPlayerBoatHitsRemaining(hitboat_type) == 0):
                        text_anmiation_content = hitboat_type + " sunk"
                    else:
                        text_anmiation_content = f"hit {hitboat_type} ({getBoatLength(hitboat_type) - getPlayerBoatHitsRemaining(hitboat_type)}/{getBoatLength(hitboat_type)})"
                    text_animation_location = (100 + int(getX(ai_move))*60, 100 + int(LetterToNum(getY(ai_move)))*60)
                    

            pygame.display.update()
            continue
    else:
        drawHeader()

        # -------------------- PLAYER'S TURN --------------------#

        if turn == "player":
            drawCounters("ai")
            if (doTextAnimation):
                drawTextAnimation()
                if(animation_time>1.5):
                    doTextAnimation=False
                    turn="ai"
            else:
                animation_time=0
            for event in pygame.event.get():
                # detect a click
                if event.type == pygame.MOUSEBUTTONDOWN and not doTextAnimation:
                    coord = "".join(getMouseCoords())
                    hitboat = ()
                    for boat in ai_grid_full:
                        boat_type = boat[1]
                        if (coord in boat[0]):
                            hitboat = (coord, boat_type)

                            # check if the player has already hit
                            if (hitboat not in ai_grid):
                                ai_grid.append(hitboat)
                                if (getAiBoatHitsRemaining(boat_type) == 0) and TOURNAMENT_MODE == False:
                                    doTextAnimation = True
                                    text_anmiation_content = boat_type + " sunk"
                                    text_animation_location = (100 + int(getX(coord))*60, 100 + int(LetterToNum(getY(coord)))*60)
                                    if(DO_TRAP_CARD):
                                        trapcard()
                                else:
                                    doTextAnimation = True
                                    text_anmiation_content = f"hit {boat_type} ({getBoatLength(boat_type) - getAiBoatHitsRemaining(boat_type)}/{getBoatLength(boat_type)})"
                                    text_animation_location = (100 + int(getX(coord))*60, 100 + int(LetterToNum(getY(coord)))*60)
                            else:
                                # they hit there already, the boat is already exploded so they missed
                                doTextAnimation = True
                                text_anmiation_content = "miss"
                                text_animation_location = (100 + int(getX(coord))*60, 100 + int(LetterToNum(getY(coord)))*60)

                    # if the player has not hit a boat
                    if (hitboat == ()) or TOURNAMENT_MODE == True:
                        doTextAnimation = True
                        text_anmiation_content = "miss"
                        text_animation_location = (100 + int(getX(coord))*60, 100 + int(LetterToNum(getY(coord)))*60)

                        ai_grid.append((coord, "miss"))

                    # draws counter at each grid shot atv
                    drawCounters("ai")
                    pygame.display.update()
                    #turn = "ai"
                    #pygame.time.delay(1000)

        # -------------------- AI'S TURN --------------------#

        elif turn == "ai":
            # do something
            ai_move = AIChoice()
            pygame_input = "hitboat"

        # When one sides has no boats remaining
    
    if (getAiBoatsRemaining() == 0 or getPlayerBoatsRemaining() == 0) and doTextAnimation == False: #if the player or ai lost, this runs after the animation.
        gameOver = True
    
    

    
    
    
    
    
    
    
    pygame.display.update()
    # When player clicks the X button at top right
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


# -------------------------------------------------#



# ------------------- GAME OVER ------------------#

game_end_time = datetime.now()
while True:
    time_since_game_end = (datetime.now()-game_end_time).total_seconds()
    
    frame = floor((time_since_game_end * 10) % 39)
    
    gameWindow.blit(end_images[frame], (0,0))
    # Player losing screen
    if getPlayerBoatsRemaining() == 0  or ai_move == "nothing":
        game_over_text_content = "AI WON"
    # Player winning screen
    elif getAiBoatsRemaining() == 0:
        game_over_text_content = "PLAYER WON"
    # Max's secret lmfao
    elif secrets.upper() == "ICBM":
        game_over_text_content = "NUKE WON"
    else:
        game_over_text_content = "NOBODY WON"#should never happen (using for tests)
    
    if(time_since_game_end<5):#draw only within the first 5 seconds
        game_over_text = title_font.render(game_over_text_content, 1, WHITE)
        game_over_text.set_alpha(200)
        centerText(game_over_text,400,100)

        fake_loading_screen_text = header_2_font.render("Fetching statistics",True,WHITE)
        centerText(fake_loading_screen_text,400,400)

        pygame.draw.rect(gameWindow,WHITE,(300,450,200 * min((time_since_game_end/4),1),25), 0 ,25)
        pygame.draw.rect(gameWindow,WHITE,(300,450,200,25), 2, 25)

    # -------------------- STATISTICS  --------------------#

    if(time_since_game_end>5):
        statistics = title_font.render("STATISTICS", 1, WHITE)
        statistics.set_alpha(200)
        centerText(statistics, 400, 100)
        drawStats()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # -------------------------------------------------#
