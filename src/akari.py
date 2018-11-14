
from constraint import *


''' Couple of helpful functions '''
def var_to_coord(var, board_size=7):
    return int(var/board_size), var%board_size

def coord_to_var(coord, board_size=7):
    return coord[0]*board_size + coord[1]


class Cell:
    '''
    White & black squares.
    Holds two variable:
    - Color
    - hint (only for blacks, otherwise None)
    '''
    def __init__(self, color=1, hint=None):
        self.color = color # true(1) for white, false for black(0)
        self.hint = hint


def black_box_adjacent(akari, index):
    '''
    Find and check adjacent cells of the black box.
    Return array of white cells (indices) adjacent to it.
    Arguments:
        akari {[type]} -- [description]
        index {[type]} -- [description]
    '''
    board_size = len(akari)
    x,y = var_to_coord(index, board_size)
    adjacents = []
    # north
    n = coord_to_var((x-1,y),board_size)
    if x-1 >= 0 and akari[x-1][y].color:
        adjacents.append(n)

    # south
    s = coord_to_var((x+1,y), board_size)
    if x+1 < board_size and akari[x+1][y].color:
        adjacents.append(s)

    # west
    w = coord_to_var((x,y-1),board_size)
    if y-1 >= 0 and akari[x][y-1].color:
        adjacents.append(w)

    # east
    e = coord_to_var((x,y+1),board_size)
    if y+1 < board_size and akari[x][y+1].color:
        adjacents.append(e)

    return adjacents

def whiteCell_corridor(akari, whiteCell, horizontal = False, vertical = False):
    '''
    Returns the list of white cells which is visible from the given input cell excluding itself.
    Arguments:
        akari {matrix} -- board
        whiteCell {int} -- index of the white cell on board.

    Returns:
        list -- list of whites visible to the given white cell. No black cell interupts.
    '''

    corridorList = []
    board_size = len(akari)

    # Explore north
    x,y = var_to_coord(whiteCell, board_size)
    x = x-1
    while x >= 0 and akari[x][y].color and not horizontal:
        corridorList.append(coord_to_var((x,y), board_size))
        x = x-1
    
    # Explore South
    x,y = var_to_coord(whiteCell, board_size)
    x = x+1
    while x < board_size and akari[x][y].color and not horizontal:
        corridorList.append(coord_to_var((x,y), board_size))
        x = x+1
    
    # Explore west
    x,y = var_to_coord(whiteCell, board_size)
    y = y-1
    while y >= 0 and akari[x][y].color and not vertical:
        corridorList.append(coord_to_var((x,y), board_size))
        y = y-1
    
    # Explore east
    x,y = var_to_coord(whiteCell, board_size)
    y = y+1
    while y < board_size and akari[x][y].color and not vertical:
        corridorList.append(coord_to_var((x,y), board_size))
        y = y+1

    return corridorList
    

def solve(akari):
    # Variables are from 0 to board_size^2-1. It is like id (index) of the cell.
    # Ex. 7*7 --> [0..48]
    problem = Problem()
    board_size = len(akari)
    cells = list(range(board_size**2)) # Variables
    domain = [0,1] # on/off
    black_cells = []
    white_cells = []

    for i in range(board_size**2):
        x,y = var_to_coord(i,board_size)
        if akari[x][y].color:
            white_cells.append(i)
        else:
            black_cells.append(i)
    
    print(white_cells)
    print(black_cells)
    # Add variables
    problem.addVariables(cells, domain)
    
    ''' Add constraints '''

    # Black box cannot contain lightbulb
    for i in black_cells:
        problem.addConstraint(lambda bc: bc != 1, [i])


    # Hint of the black cells checked
    for i in black_cells:
        adjList = black_box_adjacent(akari, i)
        x,y = var_to_coord(i,board_size) # coord of the black box
        
        adjConstraint = akari[x][y].hint
        print("adjConst: ", x, y,  adjConstraint)
        # No bulb
        if adjConstraint == 0:
            for white in adjList:
                problem.addConstraint(lambda w: w != 1, [white],)
        # only 1 has bulb
        elif adjConstraint == 1:
            problem.addConstraint(
                lambda w1=None,w2=None,w3=None,w4=None: 
                (w1 == 1 and all(w == 0 or w == None for w in [w2,w3,w4])) or 
                (w2 == 1 and all(w == 0 or w == None for w in [w1,w3,w4])) or
                (w3 == 1 and all(w == 0 or w == None for w in [w1,w2,w4])) or
                (w4 == 1 and all(w == 0 or w == None for w in [w1,w2,w3]))
                ,adjList,
            )
        # only 2 has bulb
        elif adjConstraint == 2:
            problem.addConstraint(
                lambda w1=None,w2=None,w3=None,w4=None:
                (w1 == 1 and w2 == 1 and all(w == 0 or w == None for w in [w3,w4])) or 
                (w1 == 1 and w3 == 1 and all(w == 0 or w == None for w in [w2,w4])) or
                (w1 == 1 and w4 == 1 and all(w == 0 or w == None for w in [w2,w3])) or
                (w2 == 1 and w3 == 1 and all(w == 0 or w == None for w in [w1,w4])) or
                (w2 == 1 and w4 == 1 and all(w == 0 or w == None for w in [w1,w3])) or
                (w3 == 1 and w4 == 1 and all(w == 0 or w == None for w in [w1,w2]))
                ,adjList,
            )
        # only 3 has bulb
        elif adjConstraint == 3:
            problem.addConstraint(
                lambda w1=None,w2=None,w3=None,w4=None:
                (w1 == 1 and w2 == 1 and w3 == 1 and (w4 == 0 or w4 == None)) or 
                (w1 == 1 and w2 == 1 and w4 == 1 and (w3 == 0 or w3 == None)) or
                (w1 == 1 and w4 == 1 and w3 == 1 and (w2 == 0 or w2 == None)) or
                (w4 == 1 and w2 == 1 and w3 == 1 and (w1 == 0 or w1 == None))
                ,adjList,
            )
        # all 4 has bulbs.
        elif adjConstraint == 4:
            problem.addConstraint(
                lambda w1=None,w2=None,w3=None,w4=None:
                w1 == 1 and w2 == 1 and w3 == 1 and w4 == 1
                ,adjList, 
            )

    # Each white is illumunated
    for i in white_cells:
        corridor = whiteCell_corridor(akari, i) # get the list of corridor.
        corridor.append(i) # add itself to the list. 
        # Check if  the corridor list has at least 1 light bulb.
        problem.addConstraint(SomeInSetConstraint([1]),corridor)
    
    # No light bulb illuminate each other.
    # There is exactly one light bulb in vertical and  in horizontal corridors.
    # This light bulb 
    for i in white_cells:
        horizontal = whiteCell_corridor(akari, i, horizontal=True)
        vertical = whiteCell_corridor(akari, i, vertical=True)
        horizontal.append(i)
        vertical.append(i)
        # if sum of corridor elements is larger than 1 it means there is 2 light bulb on that corriodor
        # however it is ok to sum to 0.
        problem.addConstraint(MaxSumConstraint(1), horizontal)
        problem.addConstraint(MaxSumConstraint(1), vertical)




    solutions = problem.getSolutions()
    return solutions


def main():
    '''
    board_size = 7
    akari = [[Cell() for j in range(board_size)] for i in range(board_size)]

    # manually construct akari board
    akari[0][3].color = 0
    akari[0][5].color = 0
    akari[0][5].hint = 3
    akari[1][0].color = 0
    akari[1][2].color = 0
    akari[1][2].hint = 0
    akari[2][5].color = 0
    akari[3][0].color = 0
    akari[3][0].hint = 0
    akari[3][6].color = 0
    akari[3][6].hint = 0
    akari[4][1].color = 0
    akari[4][1].hint = 0
    akari[5][4].color = 0
    akari[5][5].hint = 1
    akari[5][6].color = 0
    akari[6][1].color = 0
    akari[6][1].hint = 0
    akari[6][3].color = 0
    akari[6][3].hint = 0
    '''

    # second akari puzzle
    board_size = 10
    akari = [[Cell() for j in range(board_size)] for i in range(board_size)]

    # manually construct akari board
    akari[0][5].color = 0
    akari[0][6].color = 0
    akari[0][6].hint = 1
    akari[1][4].color = 0
    akari[0][6].hint = 0
    akari[2][3].color = 0
    akari[3][0].color = 0
    akari[3][0].hint = 1
    akari[3][7].color = 0
    akari[3][7].hint = 2
    akari[4][0].color = 0
    akari[4][0].hint = 1
    akari[4][4].color = 0
    akari[4][4].hint = 2
    akari[4][5].color = 0
    akari[4][8].color = 0
    akari[5][1].color = 0
    akari[5][1].hint = 2
    akari[5][4].color = 0
    akari[5][5].color = 0
    akari[5][5].hint = 1
    akari[5][9].color = 0
    akari[5][9].hint = 0
    akari[6][2].color = 0
    akari[6][2].hint = 2
    akari[6][9].color = 0
    akari[6][9].hint = 2
    akari[7][6].color = 0
    akari[8][5].color = 0
    akari[8][5].hint = 2
    akari[9][3].color = 0
    akari[9][4].color = 0
    



    for i in range(board_size):
        for j in range(board_size):
            print(akari[i][j].color, end=" ")
        print()
    #print(isinstance(akari[6][3], Black))

    solutions = solve(akari)
    print("Found %d solutions " % len(solutions))

    # Print first 4 solutions
    for i in range(len(solutions)):
        print(solutions[i])
        solution_board = [[Cell() for j in range(board_size)] for i in range(board_size)]
        '''
        # First table

        solution_board[0][3].color = 0
        solution_board[0][5].color = 0
        solution_board[1][0].color = 0
        solution_board[1][2].color = 0
        solution_board[2][5].color = 0
        solution_board[3][0].color = 0
        solution_board[3][6].color = 0
        solution_board[4][1].color = 0
        solution_board[5][4].color = 0
        solution_board[5][6].color = 0
        solution_board[6][1].color = 0
        solution_board[6][3].color = 0
        '''

        solution_board[0][5].color = 0
        solution_board[0][6].color = 0
        solution_board[0][6].hint = 1
        solution_board[1][4].color = 0
        solution_board[0][6].hint = 0
        solution_board[2][3].color = 0
        solution_board[3][0].color = 0
        solution_board[3][0].hint = 1
        solution_board[3][7].color = 0
        solution_board[3][7].hint = 2
        solution_board[4][0].color = 0
        solution_board[4][0].hint = 1
        solution_board[4][4].color = 0
        solution_board[4][4].hint = 2
        solution_board[4][5].color = 0
        solution_board[4][8].color = 0
        solution_board[5][1].color = 0
        solution_board[5][1].hint = 2
        solution_board[5][4].color = 0
        solution_board[5][5].color = 0
        solution_board[5][5].hint = 1
        solution_board[5][9].color = 0
        solution_board[5][9].hint = 0
        solution_board[6][2].color = 0
        solution_board[6][2].hint = 2
        solution_board[6][9].color = 0
        solution_board[6][9].hint = 2
        solution_board[7][6].color = 0
        solution_board[8][5].color = 0
        solution_board[8][5].hint = 2
        solution_board[9][3].color = 0
        solution_board[9][4].color = 0

        for key, value in solutions[0].items():
            x,y = var_to_coord(key, board_size)
            if value == 1:
                solution_board[x][y].color = 8
        
        for i in range(board_size):
            for j in range(board_size):
                if solution_board[i][j].color == 1:
                    print('O', end=" ")
                elif solution_board[i][j].color == 0:
                    if solution_board[i][j].hint != None:
                        print(solution_board[i][j].hint, end=" ")
                    else:
                        print("X", end=" ")
                elif solution_board[i][j].color == 8:
                    print("B", end=" ")
            print()

if __name__ == "__main__":
    main()






