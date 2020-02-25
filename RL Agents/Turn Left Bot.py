#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ctoybox import Toybox, Input, State
import numpy as np
import json

from matplotlib.pyplot import imshow, subplots, tight_layout


# In[3]:


move = Input()
move.up = True
fire = Input()

frames = []

with Toybox('amidar') as tb:     
    

    
    for i in range(300):
        
        tb.apply_action(move)
        
        pos = tb.state_to_json()['player']['position'] #player position             

        if i % 25 == 0 and i >0 :
            frames.append(tb.get_rgb_frame())
            if pos == prev_pos:
                move.up, move.left, fire.button1 = False, True, True
                tb.apply_action(fire)
                

                
        prev_pos = pos #player position             

            
# render the images we collected horizontally:
subplots(figsize=(len(frames)*3, 4))
imshow(np.hstack(frames))
tight_layout() # makes it a little bigger.


# In[ ]:




