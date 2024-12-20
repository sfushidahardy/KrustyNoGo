import os
import numpy as np
from pysgf import SGF
import nth_move
import render_board

def other_player(player):
    if player == "W":
        return "B"
    else:
        return "W"

def add_coord_as_liberty(player, coords):
    adjacent_coords = {
            (coords[0],max(coords[1]-1,0)),
            (coords[0],min(coords[1]+1,18)),
            (max(coords[0]-1,0),coords[1]),
            (min(coords[0]+1,18),coords[1])
            }
    adjacent_coords.discard((coords[0],coords[1])) #make set of all tuples of adjacent coordinates
    for adj_coords in adjacent_coords:
        key = is_adjacent(player, adj_coords) #update depending on adjacency with other stones of same colour
        if key != None:
            liberties_dict[player][key].add(coords)

def capture(player, key):
    player2 = other_player(player)
    for coord in groups_dict[player2][key]:
        add_coord_as_liberty(player, coord)
    del liberties_dict[player2][key]
    del groups_dict[player2][key]

def play_move(player, nthmove_coordinates):
    update_groups_liberties_p1(player, nthmove_coordinates)
    player2 = other_player(player)
    update_liberties_p2(player2, nthmove_coordinates)
    liberties_copy = liberties_dict[player2].copy()
    for key, libgrp in liberties_copy.items():
        if libgrp == set():
            capture(player, key)
            #global move_count
            #print(player2 + " captured at move " + str(move_count))

def is_adjacent(player, coords): #figure out if the adjacent coordinate belongs to an existing group
    for key, group in groups_dict[player].items():
        if coords in group:
            return key
    return

def update_groups_liberties_p1(player, coords):
    global groupid
    adjacent_coords = {
            (coords[0],max(coords[1]-1,0)),
            (coords[0],min(coords[1]+1,18)),
            (max(coords[0]-1,0),coords[1]),
            (min(coords[0]+1,18),coords[1])
            }
    adjacent_coords.discard((coords[0],coords[1])) #make set of all tuples of adjacent coordinates
    
    placeholder_group = {tuple(coords)} #this will be a new group created by the current move
    placeholder_liberties = adjacent_coords.copy() #this will be a new liberty-group created by curr move
    old_id_set = set() #these are old groups that get merged with the new group (could be empty)
    for adj_coords in adjacent_coords:
        key = is_adjacent(player, adj_coords) #update depending on adjacency with other stones of same colour
        if key != None:
            old_id_set.add(key)
            placeholder_group = placeholder_group.union(groups_dict[player][key])
            placeholder_liberties = placeholder_liberties.union(liberties_dict[player][key])
            placeholder_liberties.remove(adj_coords)
            placeholder_liberties.remove(tuple(coords))
        else: 
            player2 = other_player(player)
            key2 = is_adjacent(player2,adj_coords) #update depending on adjacency with opposite colour
            if key2 != None:
                placeholder_liberties.remove(adj_coords) 
    for key in old_id_set:
        del groups_dict[player][key]
        del liberties_dict[player][key]
    groups_dict[player][groupid] = placeholder_group
    liberties_dict[player][groupid] = placeholder_liberties
    groupid += 1

def update_liberties_p2(player2, coords):
    for key, lib_group in liberties_dict[player2].items():
        lib_group.discard(tuple(coords))

#initializing
move_count = 1
groupid = 1 #increment this every time a new group forms, ensuring a unique id
groups_dict = {"B" : {}, "W" : {}} #e.g. B is dictionary of black groups, e.g. {1:{(15,3)}, ...}
liberties_dict = {"B" : {}, "W" : {}} #e.g. B is a dictionary of liberties for every B group 

#load and parse data
file = os.path.join(os.path.dirname(__file__), "../data/test2.sgf")
parsed_sgf = SGF.parse_file(file)

while move_count < 120:
    #extract nth move
    [player, nthmove_coordinates] = nth_move.Nthmove_coordinates(move_count, parsed_sgf)

    #play nth move
    play_move(player, nthmove_coordinates) 
    move_count += 1

render_board.generate(groups_dict, liberties_dict)


