from toybox.interventions.amidar import *
from toybox.interventions.breakout import *
from toybox.interventions.base import *
from toybox.interventions.core import *
from toybox import Toybox, Input

import numpy as np
from math import sqrt
from matplotlib.animation import ArtistAnimation
from matplotlib.pyplot import imshow, subplots, tight_layout, show, figure, pause
import random
import cv2
from operator import itemgetter

def available_moves(pos, intervention): #returns a list of available "legal" moves in the format
    #[up, down, left, right] given the current position of the agent

    possible_actions = [True] * 4


    x = pos.tx
    y = pos.ty

    # if (x,y) == (0,0): #Edge cases, to deal with whether the agent is at a corner or not...
    #     return[False, True, False, True]


    try:
        tile = intervention.get_tile_by_pos(x + 1, y) #Can't move right...
        possible_actions[3] = False if (tile.tag == "Empty" or x >= 31) else True
    except:
        possible_actions[3] = False

    try:
        tile = intervention.get_tile_by_pos(x - 1, y) #Can't move left...
        possible_actions[2] = False if (tile.tag == "Empty" or x <= 0) else True
    except:
        possible_actions[2] = False

    try:
        tile = intervention.get_tile_by_pos(x, y + 1) #Can't move down...
        possible_actions[1] = False if (tile.tag == "Empty" or y >= 30) else True
    except:
        possible_actions[1] = False

    try:
        tile = intervention.get_tile_by_pos(x, y - 1) #Can't move up...
        possible_actions[0] = False if (tile.tag == "Empty" or y <= 0 ) else True
    except:
        possible_actions[0] = False


    return possible_actions #retur

def possible_moves(available): #returns an array with the available moves in the form of strings

    possible_moves = []

    if available[0]:
        possible_moves.append("up")
    if available[1]:
        possible_moves.append("down")
    if available[2]:
        possible_moves.append("left")
    if available[3]:
        possible_moves.append("right")

    return possible_moves

def get_opposite_direction(direction):

    if direction == "up": return "down"
    elif direction == "down": return "up"
    elif direction == "left" : return "right"
    elif direction == "right": return "left"

def agent_stuck(pos, pos_history):

    if len(pos_history) > 4:
        if pos == pos_history[-1] and pos == pos_history[-2] and pos == pos_history[-3] and pos == pos_history[-4] :
            return True
    else:
        return False

def check_score_dir(direction, pos, available, intervention):


    x = pos.tx
    y = pos.ty

    possible = possible_moves(available)
    dir = direction

    max_score = 0

    if len(possible) > 0:

        max_score, direction = 0, direction

        for i in possible: #Check how much "score" going in each move yields over the board, return direction that gives max direction

            if i == "up":
                score = 0
                y_up = y

                for i in range(32): #Keep going up, if the nex tile is unpainted then add 1 to the score, else break
                    if  y_up - 1 >= 0 and intervention.get_tile_by_pos(x, y_up - 1).tag == "Unpainted":
                        score += (1/(i+1))
                        y_up -= 1 #update y position to move one up
                    elif  y_up - 1 >= 0 and intervention.get_tile_by_pos(x, y_up - 1).tag == "Painted":
                        y_up -= 1
                    else:
                        # print("up score: {}".format(score))
                        break
                if score > max_score: #if this moves yields better score than previous max_score, udpdate direction and max_score
                    max_score = score
                    dir = "up"
            if i == "down":


                score = 0
                y_down = y


                for i in range(32):
                    if  y_down + 1 <= 29 and intervention.get_tile_by_pos(x, y_down + 1).tag == "Unpainted":
                        score += (1/(i+1))
                        y_down += 1
                    elif  y_down + 1 <= 29 and intervention.get_tile_by_pos(x, y_down + 1).tag == "Painted":
                        y_down +=1
                    else:
                        # print("down score: {}".format(score))
                        break
                if score >= max_score:
                    max_score = score
                    dir = "down"
            if i == "left":
                score = 0
                x_left= x

                for i in range(32):
                    if  x_left - 1 >= 0 and intervention.get_tile_by_pos(x_left - 1, y).tag == "Unpainted":
                        score += (1/(i+1))
                        x_left -= 1
                    elif x_left - 1 >= 0 and intervention.get_tile_by_pos(x_left - 1, y).tag == "Painted":
                        x_left -=1
                    else:
                        # print("left score: {}".format(score))
                        break
                if score >= max_score:
                    max_score = score
                    dir = "left"
            if i == "right":
                score = 0
                x_right = x
                for i in range(32):
                    if  x_right+1 <= 30 and intervention.get_tile_by_pos(x_right+1, y).tag == "Unpainted":
                        score += (1/(i+1))
                        x_right += 1
                    elif  x_right+1 <= 30 and intervention.get_tile_by_pos(x_right+1, y).tag == "Painted":
                        x_right += 1
                    else:
                        # print("right score: {}".format(score))
                        break
                if score >= max_score:
                    max_score = score
                    dir = "right"

    # print("Max Score: {}; and direction given is: {}".format(max_score, dir))

    return (dir,max_score)

def update_dir(direction, move, fired):
    #takes in a direction, returns a move corresponding to that direction (fired is a boolean indicating whether the fire button should be activated)



    move = Input()
    if fired:
        move.button1 = True

    if direction == "right":
        move.right = True
    elif direction == "left":
        move.left = True
    elif direction == "down":
        move.down = True
    else:
        move.up = True
    return move


move = Input()
move.up = True
direction = None

frames = []
last_dir = None
move_to_take = []
past_points = []
last_pos = []

with Toybox('amidar') as tb:

    for i in range(700):
        tb.apply_action(move)


        if i % 3 == 0:
            with AmidarIntervention(tb) as intervention:

                game = intervention.game
                enemies = game.enemies

                if i == 0:
                    for j in range(5):
                        enemies.remove(enemies[0])
                    game.player.position = intervention.get_random_track_position()

                player_pos = intervention.worldpoint_to_tilepoint(game.player.position)

                available = available_moves(player_pos, intervention)
                possible = possible_moves(available)


                player_pos = intervention.worldpoint_to_tilepoint(game.player.position)


                if check_score_dir(direction, player_pos, available, intervention)[0] != get_opposite_direction(last_dir) and not agent_stuck((player_pos.tx, player_pos.ty), last_pos):
                    direction = check_score_dir(direction, player_pos, available, intervention)[0]

                elif agent_stuck((player_pos.tx, player_pos.ty), last_pos):
                        direction = check_score_dir(direction, player_pos, available, intervention)[0]

                else:
                    direction = last_dir


                move = update_dir(direction, move, False)

                print("ok")


                last_pos.append((player_pos.tx, player_pos.ty))
                last_dir = direction
                frames.append(tb.get_rgb_frame())




for i in frames:
    imshow(i)
    pause(.01)
show()
