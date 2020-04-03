from toybox.interventions.amidar import *
from toybox.interventions.breakout import *
from toybox.interventions.base import *
from toybox.interventions.core import * 
from toybox import Toybox, Input

import numpy as np
import math
from matplotlib.pyplot import imshow, subplots, tight_layout, show
import random



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
      
    
    try:
        tile = intervention.get_tile_by_pos(x + 1, y) #Can't move right...
        possible_actions[3] = False if tile.tag == "Empty" else True
    except:
        possible_actions[3] = False
    
    try: 
        tile = intervention.get_tile_by_pos(x - 1, y) #Can't move left...
        possible_actions[2] = False if tile.tag == "Empty" else True
    except:
        possible_actions[2] = False

    try: 
        tile = intervention.get_tile_by_pos(x, y - 1) #Can't move down...
        possible_actions[1] = False if tile.tag == "Empty" else True
    except:
        possible_actions[1] = False
        
    try: 
        tile = intervention.get_tile_by_pos(x, y + 1) #Can't move up...
        possible_actions[0] = False if tile.tag == "Empty" else True
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


# In[7]:


move = Input()
move.up = True
direction = "up"
last_move = direction



frames = []
move_changed = []
direction_hist = []
direction_hist.append(direction)
move_changed.append(0)
fired = False

with Toybox('amidar') as tb:


    for i in range(900):


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

                if i == 0:
                    starting_pos = player_pos ##takes in the starting position

                if player_pos == starting_pos: ##Checking if the agent died, if so, reset everything to go up (this will probably be changed to down as the loop goes further in the body since gen_adj_move is made that way)
                    move = Input()
                    move.up = True
                    direction = "up"
                    last_move = direction
                    print(move)


                #Array that measures the manhattan distance of the player to the enemies

                vals = [calc_distance(player_pos, enemy_pos_0), calc_distance(player_pos, enemy_pos_1), 
                        calc_distance(player_pos, enemy_pos_2), calc_distance(player_pos, enemy_pos_3)]
                #Returns the Manhattan distance of the closest enemy to the agent
                enemy_idx, closest_dist = min(enumerate(vals), key = lambda p: p[1])


                if closest_dist <= 5 and not fired:
                    move.button1 = True
                    fired = True


                available = available_moves(player_pos, intervention)
                generated = gen_adj_move(direction,move, available)

                if len(move_changed) <= 2:
                        move = generated[0]
                        direction = generated[1]
                        move_changed.append(0)
                        direction_hist.append(direction)

                else:

                        if generated[1] != direction_hist[-1]: #sample_direction has changed
                            if sum(move_changed[-2:]) == 2: #the last two moves were a change in direction -> don't change direction
                                move_changed.append(0)
                                direction_hist.append(direction)

                            else: #otherwise, the last two moves were the same or not consecutive changes -> change direction normally.
                                move = generated[0]
                                direction = generated[1]
                                direction_hist.append(direction)
                                move_changed.append(1)





                print("{}.".format(i/15), direction)


                
                frames.append(tb.get_rgb_frame())



        
subplots(figsize=(20, 10))
imshow(np.hstack(frames))
show()
tight_layout() # makes it a little bigger.


# In[ ]:




