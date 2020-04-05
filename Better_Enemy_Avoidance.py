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



def get_walls(tiles):
    
    walls = []
    
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j] == 'Empty':
                coord = (i,j)
                walls.append(coord)
    return walls
    



def available_moves(pos, intervention): #returns a list of available "legal" moves in the format 
    #[up, down, left, right] given the current position of the agent
    
    possible_actions = [True] * 4
    
    x = pos.tx
    y = pos.ty

    if (x,y) == (0,0): #Edge cases, to deal with whether the agent is at a corner or not...
        return[False, True, False, True]
    # elif (x,y) == (0, )
    
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
        tile = intervention.get_tile_by_pos(x, y - 1) #Can't move down...
        possible_actions[1] = False if (tile.tag == "Empty" or y >= 31) else True
    except:
        possible_actions[1] = False
        
    try: 
        tile = intervention.get_tile_by_pos(x, y + 1) #Can't move up...
        possible_actions[0] = False if (tile.tag == "Empty" or y <= 0 ) else True
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


def opposite_dir(move, direction): #returns an input object with the opposite direction

    if move.up:
        move.up, move.down = False, True
        direction = "down"
    elif move.down:
        move.down, move.up = False, True
        direction = "up"
    elif move.right:
        move.right, move.left = False, True
        direction = "left"
    elif move.left:
        move.left, move.right = False, True
        direction = "right"

    return (move, direction)

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


# In[7]:


move = Input()
move.up = True
direction = "up"
last_move = direction



frames = []
move_changed = []
direction_hist = []
pos_history = []
direction_hist.append(direction)
move_changed.append(0)
fired = False
stuck_ct = 0

with Toybox('amidar') as tb:


    for i in range(2300):


        if i % 100 == 0:
            move.button1 = False

        tb.apply_action(move)

        if i % 15 == 0:

            
            with AmidarIntervention(tb) as intervention:


                game = intervention.game

                player_pos = intervention.worldpoint_to_tilepoint(game.player.position) 
                enemy_pos_0 = intervention.worldpoint_to_tilepoint(game.enemies[0].position)
                enemy_pos_1 = intervention.worldpoint_to_tilepoint(game.enemies[1].position) 
                enemy_pos_2 = intervention.worldpoint_to_tilepoint(game.enemies[2].position)  
                enemy_pos_3 = intervention.worldpoint_to_tilepoint(game.enemies[3].position)

                pos_history.append((player_pos.tx, player_pos.ty))


                if i == 0:
                    starting_pos = player_pos ##takes in the starting position

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


                if closest_dist <= 7:
                        fired = True



                available = available_moves(player_pos, intervention)
                generated = gen_adj_move(direction,move, available)



                if len(move_changed) <= 2 and not check_next_move(player_pos, generated[1], pos_history):
                                move = generated[0]
                                direction = generated[1]
                                move_changed.append(0)
                                direction_hist.append(direction)

                elif not check_next_move(player_pos, generated[1], pos_history):

                    if generated[1] != direction_hist[-1] and not check_next_move(player_pos, generated[1], pos_history): #sample_direction has changed
                        if sum(move_changed[-2:]) == 2: #the last two moves were a change in direction -> don't change direction
                                        move_changed.append(0)
                                        direction_hist.append(direction)

                        else: #otherwise, the last two moves were the same or not consecutive changes -> change direction normally.
                                        move = generated[0]
                                        direction = generated[1]
                                        direction_hist.append(direction)
                                        move_changed.append(1)
                elif stuck_ct >= 5 and check_next_move(player_pos, generated[1], pos_history):
                    dir = opposite_dir(move, direction)
                    move = dir[0]
                    direction = dir[1]
                    stuck_ct = 0
                else:
                    stuck_ct += 1

            move = update_dir(direction, move, fired)

            print( available, direction, check_next_move(player_pos, generated[1], pos_history), move, player_pos, stuck_ct)


                
            frames.append(tb.get_rgb_frame())


#
# out = cv2.VideoWriter('demo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 15, (10,10))
#
#
# for i in range(len(frames)):
#     out.write(frames[i])
# out.release()


# subplots(figsize=(20, 10))
# imshow(np.hstack(frames))

for i in frames:
    imshow(i)
    pause(.01)

show()

# tight_layout() # makes it a little bigger.


# In[ ]:




