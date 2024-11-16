import numpy as np


#initializing
board_state = np.zeros((19,19)) #will be the board state at each move n.
black_groups = [] #keep track of groups at move n. The "right way" to do this should be: for each black stone, assign a number which indexes the group it belongs to. (Maybe a dictionary?)
black_liberties = [] #keep track of liberties for each group
white_groups = []
white_liberties = []

#functions

#place_black
#place_white
#for each N, call the Nth move. This takes the form Move = [player, coordinates], so Move[0] determines whether to use "place_black" or "place_white".
#next, the second entry contains the coordinates of the move.
#update the board position *and* the black_groups. (black_groups update is slightly tricky because of possible unions of groups)
#update the liberties for the black groups. This consists of:
# 1. removing the given move coordinate from any liberties of black groups.
# 2. checking and adding any of the four adjacent coordinates of the given move as liberties.

#after calling "place_black" for example, we call "check_liberties_white".
#this consists of checking the four cells adjacent to the coordinates of "place_black". First, see if any of them belong to a white group. If so, for each group, remove the coordinates of the new black move from the "liberties" list corresponding to the white groups.
#for each group, check whether or not the liberties list becomes empty. If so, call the "capture" function.
#if not, the turn is over.

#capture_black
#capture_white
#the capture function takes, as input, the white or black group being captured.
#this consists of a group of coordinates all belonging to one colour, which will be removed.
#remove stones one at a time.
# 1. For each e.g. white stone being removed, check if any of the four adjacent cells is black. If so, add the coordinates to the liberties of those black groups.
# 2. For each white stone being removed, remove the coordinate from the general board position.

