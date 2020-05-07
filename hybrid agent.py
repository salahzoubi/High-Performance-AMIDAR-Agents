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

def gen_board(intervention):

    board = {}

    for x in range(32):
        for y in range(31):
            tag = intervention.get_tile_by_pos(x,y).tag
            if tag != "Empty":
                board[(x,y)] = tag

    return board

def update_board_tag(intervention, board):

    for i in board.keys():
        x,y = i[0], i[1]
        tag = intervention.get_tile_by_pos(x,y).tag
        if tag != "Empty":
            board[i] = tag

    return board

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
                    if  y_down + 1 <= 30 and intervention.get_tile_by_pos(x, y_down + 1).tag == "Unpainted":
                        score += (1/(i+1))
                        y_down += 1
                    elif  y_down + 1 <= 30 and intervention.get_tile_by_pos(x, y_down + 1).tag == "Painted":
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
                    if  x_right+1 <= 31 and intervention.get_tile_by_pos(x_right+1, y).tag == "Unpainted":
                        score += (1/(i+1))
                        x_right += 1
                    elif  x_right+1 <= 31 and intervention.get_tile_by_pos(x_right+1, y).tag == "Painted":
                        x_right += 1
                    else:
                        # print("right score: {}".format(score))
                        break
                if score >= max_score:
                    max_score = score
                    dir = "right"

    return (dir,max_score)

def closest_unpainted_point(board, pos): #Returns the closest unpainted points to a players position


    pos_x = pos.tx
    pos_y = pos.ty


    unpainted_points = [x for x,y in board.items() if y == "Unpainted"]
    distance_pos = [(calc_distance1(pos_x, pos_y, x, y), (x,y)) for (x,y) in unpainted_points if calc_distance1(pos_x, pos_y, x, y) != 0]

    if len(distance_pos) <= 0:
        return None
    closest_point = min(distance_pos)
    closest_points = [x for x in distance_pos if x[0] == closest_point[0]]


    return [x[1] for x in closest_points]

def get_to_point(player_pos, point, intervention): #Generates a sequence of valid directions to reach from player position to point on a amap

    sequence = [] #sequence of directions to reach point

    x = player_pos.tx
    y = player_pos.ty
    point_x = point[0]
    point_y = point[1]

    diff_x = x - point_x
    diff_y = y - point_y
    diff_hist = []

    while(diff_x != 0 or diff_y != 0):

        player = intervention.tile_to_tilepoint(intervention.get_tile_by_pos(x,y))
        available = available_moves(player, intervention)
        possible = possible_moves(available)


        diff_x = x - point_x
        diff_y = y - point_y


        if  len(diff_hist) > 0 and (diff_x, diff_y) == diff_hist[-1]:
            return [-1]
        else:
            if diff_x != 0:
                if diff_x < 0: #need to go right
                    if "right" in possible:
                        sequence.append("right")
                        x += 1
                        continue
                elif diff_x > 0: #need to go left
                    if "left" in possible:
                        sequence.append("left")
                        x -= 1
                        continue
            if diff_y !=0:
                if diff_y < 0: #need to go down
                    if "down" in possible:
                        sequence.append("down")
                        y += 1
                        continue
                elif diff_y > 0: #need to go up
                    if "up" in possible:
                        sequence.append("up")
                        y -= 1
                        continue
        diff_hist.append((diff_x, diff_y))




    return sequence

def agent_stuck(pos, pos_history):

    if len(pos_history) > 4:
        if pos == pos_history[-1] and pos == pos_history[-2] and pos == pos_history[-3] and pos == pos_history[-4] :
            return True
    else:
        return False

def get_opposite_direction(direction):

    if direction == "up": return "down"
    elif direction == "down": return "up"
    elif direction == "left" : return "right"
    elif direction == "right": return "left"

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

    return segments

def project_length(pos, direction, length): #returns an updated position tuple of player position+length in desired direction


    x = pos.tx
    y = pos.ty

    if direction == "up": return (x, y - length)
    elif direction == "down": return(x, y+length)
    elif direction == "left": return(x-length, y)
    elif direction == "right": return(x+length, y)



keys = range(5,25,2)

avg_scores = {k: [] for k in keys}



for k in keys:
    for j in range(10):

        frames = []
        move = Input()
        direction = None

        move_to_take = []
        past_points = []
        last_pos = []
        last_dir = None
        last_score = []
        fired = False
        y = 0

        if j >0 and j % 2 == 0:
            y += 5

        print("{}. for key: {}".format(j, k))

        with Toybox('amidar') as tb:

            tb.new_game()


            for i in range(10000):

                if(tb.game_over()) or i >= 9999:
                    avg_scores[k].append(tb.get_score())
                    print(tb.get_score())
                    break



                if len(move_to_take) <= 1:
                    while len(move_to_take) >0:
                            move = update_dir(move_to_take.pop(), move, fired)
                            tb.apply_action(move)
                            tb.apply_action(move)
                            tb.apply_action(move)
                            tb.apply_action(move)
                else:

                    while len(move_to_take)> 0:

                        desired_move = move_to_take.pop(0)
                        move = update_dir(desired_move, move, fired)
                        tb.apply_action(move)
                        tb.apply_action(move)
                        tb.apply_action(move)
                        tb.apply_action(move)
                        tb.apply_action(move)


                if i % 3 == 0:

                    with AmidarIntervention(tb) as intervention:

                        game = intervention.game
                        enemy_removal = game.enemies

                        if i == 0:
                            # for j in range(1):
                            #     enemy_removal.remove(enemy_removal[0])
                            game.player.position = intervention.tile_to_worldpoint(intervention.get_tile_by_pos(31,y))


                        enemy_0 = intervention.worldpoint_to_tilepoint(game.enemies[0].position)
                        enemy_1 = intervention.worldpoint_to_tilepoint(game.enemies[1].position)
                        enemy_2 = intervention.worldpoint_to_tilepoint(game.enemies[2].position)
                        enemy_3 = intervention.worldpoint_to_tilepoint(game.enemies[3].position)
                        enemy_4 = intervention.worldpoint_to_tilepoint(game.enemies[3].position)



                        enemies = [(enemy_0.tx, enemy_0.ty), (enemy_1.tx, enemy_1.ty), (enemy_2.tx, enemy_2.ty), (enemy_3.tx, enemy_3.ty), (enemy_4.tx, enemy_4.ty)] #, (enemy_1.tx, enemy_1.ty)


                        player_pos = intervention.worldpoint_to_tilepoint(game.player.position)

                        available = available_moves(player_pos, intervention)
                        # enemy_0 = intervention.worldpoint_to_tilepoint(game.enemies[0].position)
                        possible = possible_moves(available)

                        vals = [calc_distance(player_pos, enemy_0), calc_distance(player_pos, enemy_1), calc_distance(player_pos, enemy_2), calc_distance(player_pos, enemy_3), calc_distance(player_pos, enemy_4)] #, calc_distance(player_pos, enemy_1), calc_distance(player_pos, enemy_2)
                        #Returns the Manhattan distance of the closest enemy to the agent
                        enemy_idx, closest_dist = min(enumerate(vals), key = lambda p: p[1])

                        if i > 0 and closest_dist <= k:

                            max_dist = -1
                            dir = None

                            if closest_dist <= 5:
                                fired = True
                            else:
                                fired = False

                            for dir,length in find_dir_length(possible, player_pos, intervention):
                                projected = project_length(player_pos, dir, length)

                                if calc_distance1(projected[0], projected[1], enemies[enemy_idx][0],  enemies[enemy_idx][1]) > max_dist:
                                    max_dist = calc_distance1(projected[0], projected[1],enemies[enemy_idx][0],  enemies[enemy_idx][1])
                                    direction = dir

                                else:
                                    direction = last_dir

                                move_to_take.append(direction)

                        else:

                            checked = check_score_dir(direction, player_pos, available, intervention) #returns (direction, score) that maximizes score



                            if checked[1] == 0: #that is, the agent can't see anywhere
                                points = gen_board(intervention)
                                closest_points = closest_unpainted_point(points,player_pos)

                                closest_points = [x for x in closest_points if get_to_point(player_pos, x, intervention) != [-1] and x not in past_points] if closest_points is not None else [(0,0)]
                                if len(closest_points) > 0:
                                        get = get_to_point(player_pos, closest_points[0], intervention)
                                        move_to_take.extend(get)

                                else:

                                    moves_but_opposite = [x for x in possible if x != get_opposite_direction(last_dir)]
                                    move_to_take.append(random.choice(moves_but_opposite))



                            elif checked[0] != get_opposite_direction(last_dir) and not agent_stuck((player_pos.tx, player_pos.ty), last_pos):
                                direction = checked[0]
                                move_to_take.append(direction)


                            elif agent_stuck((player_pos.tx, player_pos.ty), last_pos):
                                direction = checked[0]
                                move_to_take.append(direction)


                            else:
                                direction = last_dir
                                move_to_take.append(direction)



                        last_pos.append((player_pos.tx, player_pos.ty))
                        last_dir = move_to_take[len(move_to_take)-1]

                        frames.append(tb.get_rgb_frame())

print(avg_scores)
# for i in frames:
#     imshow(i)
#     pause(.000001)
# show()
