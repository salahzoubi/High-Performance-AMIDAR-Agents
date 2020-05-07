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


def calc_distance(one, two):

    return sqrt((abs(one.tx -  two.tx)**2) + (abs(one.ty - two.ty)**2))

def calc_distance1(x1,y1,x2,y2):
    return sqrt( (abs(x1 - x2)**2) + (abs(y1 - y2)**2))

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
        possible_actions[2] = False if (tile.tag == "Empty" or x <= 1) else True
    except:
        possible_actions[2] = False

    try:
        tile = intervention.get_tile_by_pos(x, y - 1) #Can't move down...
        possible_actions[1] = False if (tile.tag == "Empty" or y >= 30) else True
    except:
        possible_actions[1] = False

    try:
        tile = intervention.get_tile_by_pos(x, y + 1) #Can't move up...
        possible_actions[0] = False if (tile.tag == "Empty" or y <= 1 ) else True
    except:
        possible_actions[0] = False


    return possible_actions #retur

def get_enemy_dir(enemy_hist, enemy_pos): #returns the direction the enemy is moving in given the enemy's history of moves

    x = enemy_pos.tx
    y = enemy_pos.ty

    prev = enemy_hist[-1] if len(enemy_hist) > 0 else 0

    prev_x = prev[0]
    prev_y = prev[1]

    diff_x = x - prev_x
    diff_y = y - prev_y

    if diff_x != 0 and diff_y != 0:
        print("both directions x,y have somehow changed... and the enemies pos was {} now it is {}".format((prev_x,prev_y), (x,y) ))

    if diff_x > 0:
        return "right"
    elif diff_x < 0:
        return "left"
    elif diff_y < 0:
        return "up"
    elif diff_y > 0:
        return "down"
    elif diff_x == 0 and diff_y == 0:
        return "hasn't moved"

def dir_max(pos, enemy_pos, enemy_direction, available): #returns direction that maximizes distance between agent and enemy

    x = pos.tx
    y = pos.ty

    enemy_x = enemy_pos.tx
    enemy_y = enemy_pos.ty

    direction = "none"

    right = (calc_distance1(x+1,y,enemy_x, enemy_y), "right")
    left = (calc_distance1(x-1,y, enemy_x, enemy_y), "left")
    up = (calc_distance1(x, y-1, enemy_x, enemy_y), "up")
    down = (calc_distance1(x, y+1, enemy_x, enemy_y), "down")

    possible_moves = []

    if available[0]:
        possible_moves.append(up)
    if available[1]:
        possible_moves.append(down)
    if available[2]:
        possible_moves.append(left)
    if available[3]:
        possible_moves.append(right)

    print(max(possible_moves, key = itemgetter(0))[0], max(possible_moves, key = itemgetter(0))[1])
    direction = max(possible_moves, key = itemgetter(0))[1]

    return direction

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

def find_dir_length(possible, pos, intervention): #given the possible moves at the position given, returns the (direction, length of segment in that direction)


    x = pos.tx
    y = pos.ty

    possible = possible_moves(available)
    segments = []


    if len(possible) > 0:

        length = 0

        for i in possible: #Check how much "length" going in each move yields over the board, return (direction, length)
            if i == "up":
                length = 0
                y_up = y

                for i in range(32): #Keep going up, if the nex tile is unpainted then add 1 to the score, else break
                    if  y_up - 1 >= 0 and intervention.get_tile_by_pos(x, y_up - 1).tag != "Empty":
                        length += 1
                        y_up -= 1 #update y position to move one up
                    else:
                        # print("up score: {}".format(score))
                        break
                segments.append(("up", length))
            if i == "down":
                length = 0
                y_down = y

                for i in range(32): #Keep going up, if the nex tile is unpainted then add 1 to the score, else break
                    if  y_down + 1 <= 30 and intervention.get_tile_by_pos(x, y_down + 1).tag != "Empty":
                        length += 1
                        y_down += 1 #update y position to move one up
                    else:
                        # print("up score: {}".format(score))
                        break
                segments.append(("down", length))

            if i == "left":
                length = 0
                x_left = x

                for i in range(32): #Keep going up, if the nex tile is unpainted then add 1 to the score, else break
                    if  x_left - 1 >= 0 and intervention.get_tile_by_pos(x_left - 1, y).tag != "Empty":
                        length += 1
                        x_left -= 1 #update y position to move one up
                    else:
                        # print("up score: {}".format(score))
                        break
                segments.append(("left", length))

            if i == "right":
                length = 0
                x_right = x

                for i in range(32): #Keep going up, if the nex tile is unpainted then add 1 to the score, else break
                    if  x_right + 1 <= 31 and intervention.get_tile_by_pos(x_right + 1, y).tag != "Empty":
                        length += 1
                        x_right += 1 #update y position to move one up
                    else:
                        # print("up score: {}".format(score))
                        break
                segments.append(("right", length))
    print(segments)
    return segments

def project_length(pos, direction, length): #returns an updated position tuple of player position+length in desired direction


    x = pos.tx
    y = pos.ty

    if direction == "up": return (x, y - length)
    elif direction == "down": return(x, y+length)
    elif direction == "left": return(x-length, y)
    elif direction == "right": return(x+length, y)

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



frames = []

enemy_hist = {"enemy_0": [], "enemy_1": [], "enemy_2": [], "enemy_3": []}


move = Input()
move.up = True
direction = "up"
fired = False


with Toybox('amidar') as tb:



    for i in range(2000):
        tb.apply_action(move)


        if i % 3 == 0:

            with AmidarIntervention(tb) as intervention:



                game = intervention.game



                player_pos = intervention.worldpoint_to_tilepoint(game.player.position)
                enemy_0 = intervention.worldpoint_to_tilepoint(game.enemies[0].position)
                enemy_1 = intervention.worldpoint_to_tilepoint(game.enemies[1].position)
                enemy_2 = intervention.worldpoint_to_tilepoint(game.enemies[2].position)
                enemy_3 = intervention.worldpoint_to_tilepoint(game.enemies[3].position)
                enemy_4 = intervention.worldpoint_to_tilepoint(game.enemies[4].position)

                available = available_moves(player_pos, intervention)
                possible = possible_moves(available)

                enemies = [(enemy_0.tx, enemy_0.ty), (enemy_1.tx,enemy_1.ty), (enemy_2.tx, enemy_2.ty), (enemy_3.tx, enemy_3.ty), (enemy_4.tx, enemy_4.ty)]



                vals = [calc_distance(player_pos, enemy_0), calc_distance(player_pos, enemy_1),
                calc_distance(player_pos, enemy_2), calc_distance(player_pos, enemy_3), calc_distance(player_pos, enemy_4)]
                #Returns the Manhattan distance of the closest enemy to the agent
                enemy_idx, closest_dist = min(enumerate(vals), key = lambda p: p[1])





                if i > 0 and closest_dist <= 17:

                    max_dist = -1
                    dir = None

                    if closest_dist <= 4:
                        fired = True
                    else:
                        fired = False

                    for dir,length in find_dir_length(possible, player_pos, intervention):
                        projected = project_length(player_pos, dir, length)

                        if calc_distance1(projected[0], projected[1],enemies[enemy_idx][0],  enemies[enemy_idx][1]) > max_dist:
                            max_dist = calc_distance1(projected[0], projected[1],enemies[enemy_idx][0],  enemies[enemy_idx][1])
                            direction = dir
                    # print('{}. {}, pos: {}'.format(i, dir, player_pos))

                enemy_hist['enemy_0'].append( (enemy_0.tx, enemy_0.ty))
                enemy_hist['enemy_1'].append((enemy_1.tx, enemy_1.ty))
                enemy_hist['enemy_2'].append( (enemy_2.tx, enemy_2.ty))
                enemy_hist['enemy_3'].append((enemy_3.tx, enemy_3.ty))

                move = update_dir(direction, move, fired)

                last_dir = direction


                frames.append(tb.get_rgb_frame())



for i in frames:
    imshow(i)
    pause(.00001)

show()
