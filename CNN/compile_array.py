import numpy as np
import os

def simul_shuffle(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def reshape_go(array):
    array = np.reshape(array, (-1,19,19))
    array = np.delete(array, 0, axis=0)
    return array

def process_directory(directory_path, array):
    """Function to iterate through files in a directory"""
    total = len(os.listdir(directory_path))
    progress = 0
    percentage = 0
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            newitem = np.load(os.path.join(os.path.dirname(__file__), filepath))
            array = np.append(newitem,array)
        progress += 1
        if (progress*100)/total >= percentage+1:
            print(str(percentage) + "% progress")
            percentage += 1
    return array

X_train_B = np.zeros((19,19))
X_train_W = np.zeros((19,19))
X_dev_B = np.zeros((19,19))
X_dev_W = np.zeros((19,19))
print("X sets initialized")

X_train_B = process_directory(os.path.join(os.getcwd(), 'Train_B_endgame'), X_train_B)
print("X train B loaded")
X_train_B = reshape_go(X_train_B)
print("X train B reshaped")
X_train_W = process_directory(os.path.join(os.getcwd(), 'Train_W_endgame'), X_train_W)
print("X train W loaded")
X_train_W = reshape_go(X_train_W)
print("X train W reshaped")
X_dev_B = process_directory(os.path.join(os.getcwd(), 'Dev_B_endgame'), X_dev_B)
X_dev_B = reshape_go(X_dev_B)
X_dev_W = process_directory(os.path.join(os.getcwd(), 'Dev_W_endgame'), X_dev_W)
X_dev_W = reshape_go(X_dev_W)
print("Dev B and W loaded and reshaped")

Y_train_B = np.array([1.0]*len(X_train_B))
Y_train_W = np.array([0.0]*len(X_train_W))
Y_dev_B = np.array([1.0]*len(X_dev_B))
Y_dev_W = np.array([0.0]*len(X_dev_W))
print("Y sets initialized")

X_train = np.concatenate((X_train_B, X_train_W),axis=0)
Y_train = np.concatenate((Y_train_B, Y_train_W))
print("Train sets concatenated")
X_dev = np.concatenate((X_dev_B, X_dev_W),axis=0)
Y_dev = np.concatenate((Y_dev_B, Y_dev_W))
print("Dev sets concatenated")

X_train, Y_train = simul_shuffle(X_train, Y_train)
print("Train sets shuffled")
X_train = X_train.reshape((-1,19,19,1))
Y_train = Y_train.reshape((-1,1))
print("Train sets reshaped")
X_dev, Y_dev = simul_shuffle(X_dev, Y_dev)
X_dev = X_dev.reshape((-1,19,19,1))
Y_dev = Y_dev.reshape((-1,1))
print("Dev sets shuffled and reshaped")

np.save('X_train_endgame.npy',X_train)
np.save('Y_train_endgame.npy',Y_train)
np.save('X_dev_endgame.npy',X_dev)
np.save('Y_dev_endgame.npy',Y_dev)
print("all arrays saved")
