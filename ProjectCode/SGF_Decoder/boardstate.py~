import os
import numpy as np
from pysgf import SGF
import nth_move

def play_move(player, nthmove_coordinates):
    moves = {
            "B" : play_B,
            "W" : play_W
        }
    moves[player](nthmove_coordinates)

def play_B(coords):
    update_groups_B(coords)

def play_W(coords):
    return

def is_adjacent_black(coords): #figure out if the adjacent coordinate belongs to an existing group
    for key, group in groups_dict_B.items():
        if coords in group:
            return key
    return

def update_groups_B(coords):
    global groupid_B
    adjacent_coords = {
            (coords[0],max(coords[1]-1,0)),
            (coords[0],min(coords[1]+1,18)),
            (max(coords[0]-1,0),coords[1]),
            (min(coords[0]+1,18),coords[1])
            }
    adjacent_coords.discard((coords[0],coords[1])) #make set of all tuples of adjacent coordinates
    
    placeholder_group = {tuple(coords)} #this will be a new group created by the current move
    old_id_list = [] #these are old groups that get merged with the new group (could be empty)
    for adj_coords in adjacent_coords:
        key = is_adjacent_black(adj_coords)
        if key != None:
            old_id_list.append(key)
            placeholder_group = placeholder_group.union(groups_dict_B[key])
    for key in old_id_list:
        del groups_dict_B[key]
    groups_dict_B[groupid_B] = placeholder_group
    groupid_B += 1
    
#initializing
move_count = 1
groupid_B = 1 #increment this every time a new black group forms, ensuring a unique id
groupid_W = 1 #same as above, for white
groups_dict_B = {} #dictionary of black groups, e.g. {1:{(15,3)}, ...}
groups_dict_w = {}
board_state = np.zeros((19,19))

#load and parse data
file = os.path.join(os.path.dirname(__file__), "../data/Ke_Jie-Shin_Jinseo.sgf")
parsed_sgf = SGF.parse_file(file)

while move_count < 20:
    #extract nth move
    [player, nthmove_coordinates] = nth_move.Nthmove_coordinates(move_count, parsed_sgf)

    #play nth move
    play_move(player, nthmove_coordinates)
    print(groups_dict_B)

    move_count += 1
