#import os
#import howmanymoves
#from pysgf import SGF

#file = os.path.join(os.path.dirname(__file__), "../data/Ke_Jie-Shin_Jinseo.sgf")
#parsed_sgf = SGF.parse_file(file)

#totalmoves = howmanymoves.totalmoves(parsed_sgf)
#print(totalmoves)

#N = 100

Players = ["W","B"]

def sgf_to_coords(string):
    return [ord(char) - 97 for char in string.lower()]

def Nthmove_sgf(N, parsed_sgf):
    for _ in range(N):
        parsed_sgf = parsed_sgf.children[0]
    return parsed_sgf

def Nthmove_coordinates(N, parsed_sgf):
    player = Players[N % 2]
    nthmove = Nthmove_sgf(N, parsed_sgf).get_property(player)
    return [player, sgf_to_coords(nthmove)]


