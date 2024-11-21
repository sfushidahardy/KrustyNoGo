import os
import numpy as np
from pysgf import SGF
import nth_move
import random
import render_board

#initializing global variables
move_count = 1
groupid = 1 #increment this every time a new group forms, ensuring a unique id
groups_dict = {"B" : {}, "W" : {}} #e.g. B is dictionary of black groups, e.g. {1:{(15,3)}, ...}
liberties_dict = {"B" : {}, "W" : {}} #e.g. B is a dictionary of liberties for every B group


def other_player(player):
    if player == "W":
        return "B"
    else:
        return "W"

def add_coord_as_liberty(player, coords, groups_dict, liberties_dict):
    adjacent_coords = {
            (coords[0],max(coords[1]-1,0)),
            (coords[0],min(coords[1]+1,18)),
            (max(coords[0]-1,0),coords[1]),
            (min(coords[0]+1,18),coords[1])
            }
    adjacent_coords.discard((coords[0],coords[1])) #make set of all tuples of adjacent coordinates
    for adj_coords in adjacent_coords:
        key = is_adjacent(player, adj_coords, groups_dict) #update depending on adjacency with other stones of same colour
        if key != None:
            liberties_dict[player][key].add(coords)
    return liberties_dict

def capture(player, key, groups_dict, liberties_dict):
    player2 = other_player(player)
    for coord in groups_dict[player2][key]:
        liberties_dict = add_coord_as_liberty(player, coord, groups_dict, liberties_dict)
    del liberties_dict[player2][key]
    del groups_dict[player2][key]
    return groups_dict, liberties_dict

def play_move(player, nthmove_coordinates, groupid, groups_dict, liberties_dict):
    groupid, groups_dict, liberties_dict = update_groups_liberties_p1(player, nthmove_coordinates, groupid, groups_dict, liberties_dict)
    player2 = other_player(player)
    liberties_dict = update_liberties_p2(player2, nthmove_coordinates, liberties_dict)
    liberties_copy = liberties_dict[player2].copy()
    for key, libgrp in liberties_copy.items():
        if libgrp == set():
            groups_dict, liberties_dict = capture(player, key, groups_dict, liberties_dict)
            #global move_count
            #print(player2 + " captured at move " + str(move_count))
    return groupid, groups_dict, liberties_dict

def is_adjacent(player, coords, groups_dict): #figure out if the adjacent coordinate belongs to an existing group

    for key, group in groups_dict[player].items():
        if coords in group:
            return key
    return

def update_groups_liberties_p1(player, coords, groupid, groups_dict, liberties_dict):
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
        key = is_adjacent(player, adj_coords, groups_dict) #update depending on adjacency with other stones of same colour
        if key != None:
            old_id_set.add(key)
            placeholder_group = placeholder_group.union(groups_dict[player][key])
            placeholder_liberties = placeholder_liberties.union(liberties_dict[player][key])
            placeholder_liberties.remove(adj_coords)
            placeholder_liberties.remove(tuple(coords))
        else: 
            player2 = other_player(player)
            key2 = is_adjacent(player2,adj_coords, groups_dict) #update depending on adjacency with opposite colour
            if key2 != None:
                placeholder_liberties.remove(adj_coords) 
    for key in old_id_set:
        del groups_dict[player][key]
        del liberties_dict[player][key]
    groups_dict[player][groupid] = placeholder_group
    liberties_dict[player][groupid] = placeholder_liberties
    groupid += 1
    return groupid, groups_dict, liberties_dict

def update_liberties_p2(player2, coords, liberties_dict):
    for key, lib_group in liberties_dict[player2].items():
        lib_group.discard(tuple(coords))
    return liberties_dict

def process(parsed_sgf, totalmoves):
    move_count = 1
    groupid = 1 #increment this every time a new group forms, ensuring a unique id
    groups_dict = {"B" : {}, "W" : {}} #e.g. B is dictionary of black groups, e.g. {1:{(15,3)}, ...}
    liberties_dict = {"B" : {}, "W" : {}} #e.g. B is a dictionary of liberties for every B group

    move_limit = random.randint(30, totalmoves)
    
    while move_count <= move_limit:
        #extract nth move
        [player, nthmove_coordinates] = nth_move.Nthmove_coordinates(move_count, parsed_sgf)

        #play nth move
        groupid, groups_dict, liberties_dict = play_move(player, nthmove_coordinates, groupid, groups_dict, liberties_dict)
        move_count += 1

    img_data = render_board.generate(groups_dict, liberties_dict)
    return img_data
