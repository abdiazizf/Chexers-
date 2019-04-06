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

GOAL = {'R': [(3, -3), (3,-2) , (3,-1) , (3, 0)] , 'B':[(0, -3), (-1,-2) , (-2,-1) , (-3, 0)] , 'G' :[(-3, 3), (-2, 3) , (-1, 3) , (0, 3)]}
axial_directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
axial_jump = [(2, 0), (2, -2), (0, -2), (-2, 0), (-2, 2), (0, 2)]
def main():


    with open(sys.argv[1]) as file:
        data = json.load(file)

    board_dict = convert_json_to_board_dict(data)
    # TODO: Search for and output winning sequence of moves
    # ...
    print_board(board_dict)
    initial_state = Board(board_dict)

    a = search(initial_state)
    print(a)
    print_board(board_dict)
class Board:
    # With hex based the board_state dict will contain a dictionary of hexes
    # coordinates will still be key, hex is now value
    # Dictionary: tuples (board coordinates) as key, current piece status as value
    board_state = {}

    pieces = []

    target = []


    def __init__(self, state, goal_state ,parent = None):
        self.state = state
        self.goal_state = goal_state

        tuples = [(x, y) for x in range(-3,4) for y in range(-3,4)]
        for entry in tuples:
            self.board_state[entry] = GameHex(False, False)
        for entry in initial_board:
            if initial_board[entry] in GOAL:
                self.pieces.append(entry)
                self.target = GOAL[initial_board[entry]]
                self.board_state[entry].is_occupied = True
                self.board_state[entry].occupied_by = initial_board[entry]
            elif initial_board[entry] != '-':
                self.board_state[entry].is_occupied = True
                self.board_state[entry].occupied_by = initial_board[entry]


    def successor_board_states(self):
        potential_moves = []
        potential_jump = []
        legal_moves = []
        legal_jumps =[]
        successor_states = []
        for i in axial_directions:
            potential_moves.append((self.pieces[0][0]+i[0], self.pieces[0][1]+i[1]))
        for i in axial_jump :
            potential_jump.append((self.pieces[0][0] + i[0], self.pieces[0][1] + i[1]))
        for i in potential_moves :
            if i[0] not  in range(-3,4) or  i[1] not in range(-3,4):
               continue
            elif self.board_state[i].is_occupied :
                continue
            legal_moves.append(i)
        for i in potential_jump:
            if i[0] not in range(-3, 4) or i[1] not in range(-3, 4):
                continue
            elif self.board_state[i].is_occupied :
                continue
            elif self.board_state[(i[0] // 2, i[1] // 2)].is_occupied :
                legal_moves.append(i)
            else:
                continue

      #   for each in legal_moves:
      #      state = copy.deepcopy(self)
      #      swap_position(state.state, state.pieces[0], each)
      #      state.board_state.
      #      successor_states.append(state)



        return state



def swap_position(state,move_from, move_to):
    temp = state[move_from]
    state[move_from] = state[move_to]
    state[move_to] = temp
    return state


def same_sign(x , y) :
    if x < 0 and y < 0 :
        return 1
    elif x>=0 and y>= 0 :
        return 1
    else :
        return 0

def heuristic(target, source):

  # if board_state.board_state[goal].is_occupied:
  #     heuristic_list.append(9999)
  ##     continue
    distance_x = target[0] - source[0]
    distance_y = target[1] - source[1]
    if same_sign(distance_x, distance_y):
        heuristic_list = abs(distance_x + distance_y)
    else:
        heuristic_list = max(abs(distance_x), abs(distance_y))
    return heuristic_list

def search(initial_board) :

    queue = Q.PriorityQueue()
    queue.put(initial_board.pieces[0], 0)
    cost_so_far = {}
    cost_so_far[initial_board.pieces[0]] = 0
    came_from = {}
    came_from[initial_board.pieces[0]] = None

    while not queue.empty():
        current_state = queue.get()
        if current_state in initial_board.target :
            break
        for successor in initial_board.successor_board_states() :
            new_cost = cost_so_far[current_state] + 1
            if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                cost_so_far[successor] = new_cost
                priority = new_cost + heuristic(initial_board.target[0] , successor)
                queue.put(successor, priority)
                came_from[successor] = current_state

    return came_from


def convert_json_to_board_dict(file):
    # Reads colour from the JSON, compares it to a dictionary of values and
    # sets the correct symbol
    tuples = [(x, y) for x in range(-3, 4) for y in range(-3, 4)]
    colour_dict = {'red' : 'R','blue': 'B','green':'G'}
    player_colour = colour_dict[file['colour']]
    # Creates an empty dict and constructs an entry for each tuple in JSON, using
    # predetermined player colour for player pieces and a block otherwise
    board_dict = {}
    for coordinate in file['pieces']:
        board_dict[tuple(coordinate)] = player_colour
    for coordinate in file['blocks']:
        board_dict[tuple(coordinate)] = 'BLK'
    # return dict

    for pair in tuples :
        if pair not in board_dict :
            board_dict[pair] = '-'
    return board_dict





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
class GameHex:

    # Could possibly define a game board as a collection of hexes.
    # Each hex has a co-ordinate


    def __init__(self,is_occupied,occupied_by):
        self.is_occupied = is_occupied
        self.occupied_by = occupied_by


    def __str__(self):
        return "S({}, {})".format(self.is_occupied, self.occupied_by)



if __name__ == '__main__':
    main()