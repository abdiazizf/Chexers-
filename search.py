
"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching
Authors: Abdiaziz Farah, Jordan Puckridge
HEX BASED IMPLEMENTATION
"""

import sys
import json
import copy
import queue as Q

# TODO: Implement a move function for board to check for a valid move and then swap pieces
# Also needs to print the specified output according to the project spec

# TODO: Implement a distance function to calculate how far it is from a hex to
# the nearest goal space, to use in a heuristic evaluation

# TODO: Implement search algorithm that finds optimal solution and records
# the sequence of moves

#possible moves
axial_directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
#possible jumos
axial_jump = [(2, 0), (2, -2), (0, -2), (-2, 0), (-2, 2), (0, 2)]
#goal for each colour
goal = {'R': [(3, -3), (3,-2) , (3,-1) , (3, 0)] , 'B':[(0, -3), (-1,-2) , (-2,-1) , (-3, 0)] , 'G' :[(-3, 3), (-2, 3) , (-1, 3) , (0, 3)]}
# off board co-ordinates for generating valid exit moves  
exit_hexes = {'R': [(4, -3),(4,-2),(4,-1)] , 'B':[(-3,-1),(-2,-2),(-1,-3)] , 'G' :[(-3,4),(-2,4),(-1,4)]}

def main():


    with open(sys.argv[1]) as file:
        data = json.load(file)
        
    #converts board to dict
    board_dict = convert_json_to_board_dict(data)
    pieces, target = create_piece_and_target_list(board_dict)
    
    print_board(board_dict,debug=True)
    
    #returns state of last piece
    a = search(board_dict,pieces,target)
    path = []
    while a :
        path.insert(0 ,a.pieces[0])
        a=a.parent
    print(path)
    
    
#Class for every node state
class State :
    def __init__(self,state,pieces,parent,cost,target):
        self.state = state
        self.pieces = pieces
        self.parent = parent
        self.cost = cost
        self.target = target
        self.cost


    #prints object as a board and not memory location of object
    def __str__(self):
        return str(self.parent.action)
    def __hash__(self):
        my_tuple = self.state
        return hash(my_tuple)

    def __eq__(self, other):
        return (self.state, self.pieces, self.parent) == (other.state, other.pieces, other.parent)
    def __lt__(self,other):
        return self.cost < other.cost

    def successor_board_states(self):
        legal_moves = []
        successor_states = []
        exit_moves = []
        for piece in self.pieces:
            for i in axial_directions:
                potential_moves = (piece[0]+i[0], piece[1]+i[1])
                
                # Add EXIT check here 
                if potential_moves in exit_hexes:
                    exit_moves.append(potential_moves)
                    
                if potential_moves not in self.state or self.state[potential_moves] is not None:
                    continue
                legal_moves.append(potential_moves)
                
    
            for i in axial_jump :
                potential_jump = (piece[0] + i[0], piece[1] + i[1])
                if potential_jump not in self.state or self.state[potential_jump] is not None:
                    continue
                elif self.state[(potential_jump[0] - (i[0]/2), potential_jump[1] - (i[1] / 2))] is not None:
                    legal_moves.append(potential_jump)
                else:
                    continue
            
         

        #CREATE NEW STATE FOR EVERY POSSIBLE MOVE Ill maybe create a new method for this
        for each in legal_moves:
            for piece in self.pieces:
                if valid_move_for_piece(piece, each): 
                    # Create state from move for desire piece
                    index = self.pieces.index(piece)
            index = 0       
            new_state = copy.deepcopy(self.state)
            new_piece = copy.deepcopy(self.pieces)
            temp = new_state[each]
            new_state[each]= new_state[new_piece[index]]
            new_state[new_piece[index]] = temp
            new_piece[index] = each
            state = State(new_state,new_piece,self,self.cost + 1 ,self.target)
            successor_states.append(state)


        return successor_states

def valid_move_for_piece(piece,move):
    
    for direction in axial_directions:
        new_move = piece[0]+direction[0], piece[1]+direction[1]
        if new_move == move:
            return True
    return False

def swap_pieces_in_state(move,new_state,piece):
    return True

# prints output for current move
def print_move(origin, goal, move):
    if move == "JUMP":
        print("JUMP from ,",origin," to ",goal,".")
    elif move == "MOVE":
        print("MOVE from ,",origin," to ",goal,".")
    elif move == "EXIT":
        print("EXIT from ,",origin,".")


def same_sign(q , r) :
    return (q < 0 and r < 0)or (q>=0 and r>= 0)

# returns the distance between two axial hex coordinates
def hex_distance(origin, goal):
    
    distance_x = goal[0] - origin[0]
    distance_y = goal[1] - origin[1]
    if same_sign(distance_x, distance_y):
        return abs(distance_x + distance_y)
    else:
        return max(abs(distance_x), abs(distance_y))
    
    return 

#returns minimum distance to any target
def heuristic(target, source):
    heuristic = 0
    for piece in source :
        heuristic_list = []
        for goal in target:
            heuristic_list.append(hex_distance(piece, goal))
        heuristic += min(heuristic_list)

    return  heuristic


def search(initial_state, pieces , target) :
    initial_state = State(initial_state,pieces,None,0,target)  #initialise first state
    queue = Q.PriorityQueue()                                       #create Priority queue
    queue.put(initial_state, initial_state.cost)                    #put initial state in queue
    vistited_states = {}                                            #create empty dictionary for visited_nodes
    vistited_states[tuple(initial_state.state.items())] = initial_state.cost #create dictionary

    while not queue.empty():
        current_node = queue.get()
        # this                 |  is why it only works for one piece 
        #                      |
        # goal check           v
        if current_node.pieces[0] in current_node.target:
            break
        
        # define goal state as a board with no pieces on it
        # if current_node == goal_state:
        #   break
        
        #if not current_node.pieces:
        #    break
        
        # generate successor states of current node 
        for successor in current_node.successor_board_states():
            new_cost = successor.cost
            
            if tuple(successor.state.items()) not in vistited_states:
                priority = new_cost + heuristic(initial_state.target, successor.pieces)
                queue.put(successor, priority)

    # TODO: print output of final moves 
    return current_node


def convert_json_to_board_dict(file):
    # Reads colour from the JSON, compares it to a dictionary of values and
    # sets the correct symbol
    colour_dict = {'red' : 'R','blue': 'B','green':'G'}
    player_colour = colour_dict[file['colour']]
    coordinates = [(q, r) for q in range(-3, 4) for r in range(-3, 4) if -q - r in range(-3, 4)]
    # Creates an empty dict and constructs an entry for each tuple in JSON, using
    # predetermined player colour for player pieces and a block otherwise
    board_dict = {}

    for coordinate in file['pieces']:
        board_dict[tuple(coordinate)] = player_colour
    for coordinate in file['blocks']:
        board_dict[tuple(coordinate)] = 'BLK'
    for coordinate in coordinates :
        if coordinate not in board_dict:
            board_dict[coordinate]= None

    # return dict

    return board_dict

#creates a list of all the pieces
#creates a list of all the possible target nodes (ie theres a block on one target so we cant use it

def create_piece_and_target_list(board_dict):
    pieces = []
    for entry in board_dict:
        if board_dict[entry] in goal:
            pieces.append(entry)
            targets = goal[board_dict[entry]]
    for i in targets:
        if board_dict[i] == 'BLK':
            targets.remove(i)
        return pieces, targets


def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.
    Arguments:
    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.
    Keyword arguments:
    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3 + 1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:


if __name__ == '__main__':
    main()
