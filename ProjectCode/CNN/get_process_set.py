import os 
import boardstate
from pysgf import SGF
import howmanymoves
import numpy as np

def save_processed_data(result, board):
    global success
    success += 1
    if result == 0:
        np.save(os.path.join('Test_W_endgame', str(success)+'.npy'), board)
    else:
        np.save(os.path.join('Test_B_endgame', str(success)+'.npy'), board)
    return

def determine_boardstate(parsed_sgf, result, movecount):
    global fail
    global boardstate_error
    try:
        board = boardstate.process(parsed_sgf, movecount)
    except:
        fail += 1
        boardstate_error += 1
    else:
        save_processed_data(result, board)

def move_count(parsed_sgf, result):
    global fail
    global movecount_error
     #does the file have enough moves? (how many moves does it have?)
    try:
        movecount = howmanymoves.totalmoves(parsed_sgf)
    except:
        fail += 1
        movecount_error += 1
    else:
        determine_boardstate(parsed_sgf, result, movecount) 

def winner(parsed_sgf):
    #does the file have a winner?
    global fail
    global indeterminate
    try:
        raw_result = parsed_sgf.get_property("RE")[0]
        result = 0
        if raw_result == "B":
            result = 1
        elif raw_result == "W":
            result == 0
    except:
        fail += 1
        indeterminate += 1
    else:
        move_count(parsed_sgf, result)

def process_file(filepath):
    """Function to process each file"""
    #is the file actually a valid SGF?
    global fail
    global corrupt_file
    try:
        file = os.path.join(os.path.dirname(__file__), filepath)
        parsed_sgf = SGF.parse_file(file)
    except:
        fail += 1
        corrupt_file += 1
    else: 
        winner(parsed_sgf) 
       
def process_directory(directory_path):
    """Function to iterate through files in a directory"""
    global progress
    global percentage
    global total
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            process_file(filepath)
        progress += 1
        if (progress*100)/total >= percentage + 1:
            print(str(percentage) + "% progress")
            percentage += 1

def process_directory_five_times(directory_path):
    """Function to iterate through files in a directory"""
    global progress
    global percentage
    global total
    iterations = 1
    while iterations <= 5:
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath):
                process_file(filepath)
            progress += 1
            if (progress*100)/total >= percentage + 1:
                print(str(percentage) + "% progress")
                percentage += 1
        progress = 0
        percentage = 0
        print("iteration: "+ str(iterations))
        iterations += 1

#initialize metadata
success = 0
fail = 0
corrupt_file = 0
indeterminate = 0
movecount_error = 0
boardstate_error = 0
progress = 0
percentage = 0
total = len(os.listdir('./Test_Raw'))

# Get the directory path
cwd = os.getcwd()
directory_path = os.path.join(cwd, "Test_Raw")

# Process the files in the directory
process_directory(directory_path)

print("success: " + str(success))
print("fail: " + str(fail))
print("fail - corrupt file: " + str(corrupt_file))
print("fail - indeterminate game: " + str(indeterminate))
print("fail - too few moves: " + str(movecount_error))
print("fail - boardstate error: " + str(boardstate_error))
