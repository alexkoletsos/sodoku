#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import numpy as np
import time

ROW = "ABCDEFGHI"
COL = "123456789"
FULL_DOMAIN = [1,2,3,4,5,6,7,8,9]

#dict mapping squares to tiles 
squares = {1:['A1','A2','A3','B1','B2','B3','C1','C2','C3'],
           2:['A4','A5','A6','B4','B5','B6','C4','C5','C6'],
           3:['A7','A8','A9','B7','B8','B9','C7','C8','C9'],
           4:['D1','D2','D3','E1','E2','E3','F1','F2','F3'],
           5:['D4','D5','D6','E4','E5','E6','F4','F5','F6'],
           6:['D7','D8','D9','E7','E8','E9','F7','F8','F9'],
           7:['G1','G2','G3','H1','H2','H3','I1','I2','I3'],
           8:['G4','G5','G6','H4','H5','H6','I4','I5','I6'],
           9:['G7','G8','G9','H7','H8','H9','I7','I8','I9']}


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def modify_board(board):
    # if value of key is 0, modify value to be elements 1-9, add to unassigned vars
    for k in board.keys():
        if board[k] == 0:
            board[k] = FULL_DOMAIN.copy()

    #now, removes items that are already on board from domains
    new_board = reduce_domain(board)
    return new_board


def is_complete(board):
    for k in board.keys():
        if 'list' in str(type(board[k])):
            return False
    return True

def mrv(board):
    #return list of vars with least remaining legal values
    least = 10
    var = ''

    for k in board.keys():
        if 'int' in str(type(board[k])):
            continue
        if len(board[k]) < least:
            least = len(board[k])
            var = k

    return var

def is_consistent(var,val,board):
    #check if value in var is consistent with assigned vars (not in same row, column, square)   

    #same square
    if var[0] in ['A','B','C']:
            r_val = 0
    elif var[0] in ['D','E','F']:
            r_val = 3
    elif var[0] in ['G','H','I']:
            r_val = 6
    box_num = r_val + -(-int(var[1])//3)

    for tile in squares[box_num]:
        if 'list' in str(type(board[tile])):
            continue
        if tile != var and board[tile] == val:
            return False

    row = var[0]
    col = var[1]

    #same row
    for i in range(1,10):
        r_tile = row + str(i)
        if 'list' in str(type(board[r_tile])):
            continue
        if r_tile != var and board[r_tile] == val:
            return False
    
    #same column
    for j in ROW:
         c_tile = j + col
         if 'list' in str(type(board[c_tile])):
            continue
         if c_tile != var and board[c_tile] == val:
            return False
        
    return True

def forward_check(var,val,board):
    #forward checks domains given assignment, reduces runtime

    #same square
    if var[0] in ['A','B','C']:
            r_val = 0
    elif var[0] in ['D','E','F']:
            r_val = 3
    elif var[0] in ['G','H','I']:
            r_val = 6
    box_num = r_val + -(-int(var[1])//3)

    for tile in squares[box_num]:
        if 'int' in str(type(board[tile])):
            continue
        if tile != var and val in board[tile]:
            board[tile].remove(val)
            if len(board[tile]) == 0:
                return False

    row = var[0]
    col = var[1]

    #same row
    for i in range(1,10):
        r_tile = row + str(i)
        if 'int' in str(type(board[r_tile])):
            continue
        if r_tile != var and val in board[r_tile]:
            board[r_tile].remove(val)
            if len(board[r_tile]) == 0:
                return False
    
    #same column
    for j in ROW:
         c_tile = j + col
         if 'int' in str(type(board[c_tile])):
            continue
         if c_tile != var and val in board[c_tile]:
            board[c_tile].remove(val)
            if len(board[c_tile]) == 0:
                return False

    return True

def reduce_domain(board): 
    #forward checks domains before running algo

    #same square
    for var in board.keys():
        if 'list' in str(type(board[var])):
            continue
         
        val = board[var]


        if var[0] in ['A','B','C']:
                r_val = 0
        elif var[0] in ['D','E','F']:
                r_val = 3
        elif var[0] in ['G','H','I']:
                r_val = 6
        box_num = r_val + -(-int(var[1])//3)

        for tile in squares[box_num]:
            if 'int' in str(type(board[tile])):
                continue
            if tile != var and val in board[tile]:
                board[tile].remove(val)
                if len(board[tile]) == 1:
                    board[tile] = board[tile][0]

        row = var[0]
        col = var[1]

        #same row
        for i in range(1,10):
            r_tile = row + str(i)
            if 'int' in str(type(board[r_tile])):
                continue
            if r_tile != var and val in board[r_tile]:
                board[r_tile].remove(val)
                if len(board[r_tile]) == 1:
                    board[r_tile] = board[r_tile][0]
        
        #same column
        for j in ROW:
            c_tile = j + col
            if 'int' in str(type(board[c_tile])):
                continue
            if c_tile != var and val in board[c_tile]:
                board[c_tile].remove(val)
                if len(board[c_tile]) == 1:
                    board[c_tile] = board[c_tile][0]

    return board

def deep_copy(board):
    copy = { }
    for key,value in board.items():
        if 'int' in str(type(value)):
            copy[key] = value
        else:
            copy[key] = value.copy()
    return copy

def backtracking(board):
    #modifies unassigned variables (forward checks)
    assigned = modify_board(board)
    #recursively calls backtracking
    return backtracking_search(assigned)

def backtracking_search(board):
    """Takes a board and returns solved board."""
    #check if assignment is complete
    if is_complete(board):
        return board
    #MRV function
    var = mrv(board)
    #now, iterate through domain
    for val in board[var]:
        if is_consistent(var,val,board):
            temp = deep_copy(board)
            temp[var] = val
            if forward_check(var,val,temp):
                result = backtracking_search(dict(temp))
                if result:
                    return result
    return 


if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        counter = 0

        list_time = []

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            st = time.time()

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)
            et = time.time()
            elapsed = round(et - st, 8)

            counter += 1
            #print(counter)

            # Print solved board. TODO: Comment this out when timing runs.
            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
            list_time.append(elapsed)

        f_rm = open('README.txt', "w")
        f_rm.write(f'Puzzles Solved: {counter}\n')
        f_rm.write(f'Minimum Running Time: {min(list_time)}\n')
        f_rm.write(f'Maximum Running Time: {max(list_time)}\n')
        f_rm.write(f'Average Running Time: {round(np.mean(list_time),8)}\n')
        f_rm.write(f'Standard Deviation: {round(np.std(list_time),8)}\n')

        print("Finishing all boards in file.")