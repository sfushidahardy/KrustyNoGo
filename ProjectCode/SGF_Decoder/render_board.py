import numpy as np

np.set_printoptions(linewidth=np.inf)
def generate(groups, liberties):
    img_data = [" "]*19*19
    for key, grps in groups["B"].items():
        for coord in grps:
            img_data[coord[1]*19+ coord[0]] = "B"
    for key, grps in groups["W"].items():
        for coord in grps:
            img_data[coord[1]*19+ coord[0]] = "W"
    #for key, grps in liberties["B"].items():
    #    for coord in grps:
    #        img_data[coord[1]*19+ coord[0]] = "b"
    #for key, grps in liberties["W"].items():
    #    for coord in grps:
    #        img_data[coord[1]*19+ coord[0]] = "w"
    img_data = np.array(img_data).reshape((19,19))
    print(img_data)
