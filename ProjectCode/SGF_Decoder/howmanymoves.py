
def totalmoves(sgf_file):
    total_moves = 0
    current_node = sgf_file
    while current_node.children != []:
        current_node = current_node.children[0]
        total_moves += 1
    return total_moves
