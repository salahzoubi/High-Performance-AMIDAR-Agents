from toybox.interventions.amidar import *
from toybox.interventions.breakout import *
from toybox.interventions.base import *
from toybox.interventions.core import * 
from toybox import Toybox, Input

import numpy as np
import math
from matplotlib.animation import ArtistAnimation
from matplotlib.pyplot import imshow, subplots, tight_layout, show, figure, pause
import random
import cv2


def calc_distance(one, two):
    
    return abs(one.tx -  two.tx) + abs(one.ty - two.ty)





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
    

    return possible_actions 


def gen_adj_move(direction, move,  moves):
    #generates a move that is adjacent to the current one (i.e: not opposite direction)
    
    mover = move
    direct = direction
    
    if direction == "up" or direction == "down":  
        if moves[2]:
            setattr(mover, 'left', True)
            setattr(mover, direction, False)
            direct = 'left'
        elif moves[3]:
            setattr(mover, 'right', True)
            setattr(mover, direction, False)
            direct = 'right'
    if direction == "left" or direction == "right":
        if moves[0]:
            setattr(mover, 'up', True)
            setattr(mover, direction, False)
            direct = 'up'
        elif moves[1]:
            setattr(mover, 'down', True)
            setattr(mover, direction, False)
            direct = 'down'
    
    return (mover, direct)


def visited_before(direction, pos, pos_history): #checks whether the moving in the given direction ends the agent in a position that has been visited before...

    x = pos.tx
    y = pos.ty
    visited = False

    if direction == "up":
        if (x, y-1) in pos_history:
            visited = True
    elif direction == "down":
        if (x, y+1) in pos_history:
            visited = True
    elif direction == "left":
        if (x-1, y) in pos_history:
            visited = True
    else:
        if (x+1, y) in pos_history:
            visited = True

    return visited


def gen_direction(direction, direction_hist, available_moves, pos, pos_history): #enemy spotted, direction must be changed to an adjacent one...


        dir = direction
        if len(direction_hist) >= 3 and direction == (direction_hist[-1] and direction_hist[-2] and direction_hist[-3]): #atleast 4 moves have been made and direction has not been changed for two moves...

            possible_directions = []

            if available_moves[0]: possible_directions.append("up")
            if available_moves[1]: possible_directions.append("down")
            if available_moves[2]: possible_directions.append("left")
            if available_moves[3]: possible_directions.append("right")


            if direction == "up" or direction == "down": #do some checks
                if "left" in possible_directions and "right" in possible_directions:
                    if visited_before("left", pos, pos_history):
                        dir = "right"
                    elif visited_before("right", pos, pos_history):
                        dir = "left"
                    else:
                        dir = "left"

                elif "left" in possible_directions and not "right" in possible_directions:
                    if not visited_before("left", pos, pos_history):
                        dir = "left"

                elif  "right" in possible_directions and not "left" in possible_directions:
                   if not visited_before("right", pos, pos_history):
                       dir = "right"


            elif direction == "left" or direction == "right":

                if "up" in possible_directions and "down" in possible_directions:
                    if visited_before("up", pos, pos_history):
                        dir = "down"
                    elif visited_before("down", pos, pos_history):
                        dir = "up"
                    else:
                        dir = "up"
                elif "up" in possible_directions and not "down" in possible_directions:
                    if not visited_before("up", pos,pos_history):
                        dir = "up"
                elif "down" in possible_directions and not "up" in possible_directions:
                    if not visited_before("down", pos, pos_history):
                        dir = "down"



        return dir




def check_next_move (pos, direction, position_history): #Checks whether the agent is back tracking or not... returns true if position has been taken before

    x = pos.tx
    y = pos.ty

    if direction == "left":
        return (x-1, y) in position_history
    elif direction == "right":
        return (x+1, y) in position_history
    elif direction == "up":
        return (x, y+1) in position_history
    elif direction == "down":
        return (x, y-1) in position_history

def opposite_dir(direction): #returns an input object with the opposite direction

    if direction == "up":
        return "down"
    elif direction == "down":
        return "up"
    elif direction == "right":
        return "left"
    elif direction == "left":
        return "right"

    return
def update_dir(direction, move, fired):


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

def gen_normal_move(direction, available_moves, pos_history, pos):

    dir = direction

    possible_directions = []

    if available_moves[0]: possible_directions.append("up")
    if available_moves[1]: possible_directions.append("down")
    if available_moves[2]: possible_directions.append("left")
    if available_moves[3]: possible_directions.append("right")

    if direction in possible_directions and not visited_before(direction, pos, pos_history): # keep moving in same direction if it leads to a position that hasn't been visited before
        dir = direction

    elif direction in possible_directions and visited_before(direction, pos, pos_history):
        possible_directions = list(filter(lambda x: x != direction, possible_directions))
        if len(possible_directions) <= 0:
            dir = direction
        else:
            dir = random.choice(possible_directions)
    else:
        sample_directions = list(filter(lambda x: x != opposite_dir(direction), possible_directions))

        if len(sample_directions) > 0:
            dir = random.choice(sample_directions)
        else:
            dir = random.choice(possible_directions)

    return dir


def agent_stuck(pos, pos_history):

    x = pos.tx
    y = pos.ty

    if len(pos_history) >= 5:
        if (x,y) == pos_history[-1]:
            return True

    return False



# In[7]:


move = Input()
move.up = True
direction = "up"
last_move = direction



frames = []
move_changed = []
direction_hist = []
pos_history = []
move_changed.append(0)
enemy_hist = []
last_enemy_fired = -1
fired = False

with Toybox('amidar') as tb:


    for i in range(2000):

        tb.apply_action(move)


        if i % 10 == 0:

            
            with AmidarIntervention(tb) as intervention:


                game = intervention.game

                player_pos = intervention.worldpoint_to_tilepoint(game.player.position) 
                enemy_pos_0 = intervention.worldpoint_to_tilepoint(game.enemies[0].position)
                enemy_pos_1 = intervention.worldpoint_to_tilepoint(game.enemies[1].position) 
                enemy_pos_2 = intervention.worldpoint_to_tilepoint(game.enemies[2].position)  
                enemy_pos_3 = intervention.worldpoint_to_tilepoint(game.enemies[3].position)


                positions = [enemy_pos_0, enemy_pos_1, enemy_pos_2, enemy_pos_3]


                if i == 0:
                    starting_pos = player_pos ##takes in the starting position
                    print("we're back at square 1")

                if player_pos == starting_pos: ##Checking if the agent died, if so, reset everything to go up (this will probably be changed to down as the loop goes further in the body since gen_adj_move is made that way)
                    move = Input()
                    move.up = True
                    direction = "up"
                    last_move = direction


                #Array that measures the manhattan distance of the player to the enemies

                vals = [calc_distance(player_pos, enemy_pos_0), calc_distance(player_pos, enemy_pos_1), 
                        calc_distance(player_pos, enemy_pos_2), calc_distance(player_pos, enemy_pos_3)]
                #Returns the Manhattan distance of the closest enemy to the agent
                enemy_idx, closest_dist = min(enumerate(vals), key = lambda p: p[1])

                available = available_moves(player_pos, intervention)


                if agent_stuck(player_pos, pos_history):
                    print("I'm stuck")


                if closest_dist <= 3 and enemy_idx is not last_enemy_fired:
                        last_enemy_fired = enemy_idx
                        fired = True
                        print("jumped")
                else:
                        fired = False

                enemy_hist.append(enemy_idx)


                direction = gen_direction(direction, direction_hist, available, player_pos, pos_history)



                print("changing dir to: {}".format(direction))


            # else:
            #
            #         direction = gen_normal_move(direction, available, pos_history, player_pos)



                move = update_dir(direction, move, fired)
                print("{}. {}; {}; {}; {}".format(i/10, available, direction, move, player_pos))


                pos_history.append((player_pos.tx, player_pos.ty))
                direction_hist.append(direction)

                frames.append(tb.get_rgb_frame())






# subplots(figsize=(20, 10))
# imshow(np.hstack(frames))

for i in frames:
    imshow(i)
    pause(.01)

show()

# tight_layout() # makes it a little bigger.






