import sys
from itertools import groupby
import os
import ctypes
from copy import deepcopy


# pos = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
default_pos = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

class Board:
    turn = 'X'
    winner = False
    # pos = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    valid_moves = []
    # pos = []
    def __init__(self, positions = default_pos, turn = 'X', row_move = '', col_move = ''):
        self.pos = positions
        self.turn = turn
        self.row_move = row_move
        self.col_move = col_move
        self.getavailablemoves()
        if row_move != '' and col_move != '':
             self.update_pos(self.row_move, self.col_move)
        self.getavailablemoves()

    def draw_board(self):
        # clears the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        # line numbers
        print('player ' + self.turn + "'s turn")
        print(' ' * 3 + '1' + ' ' * 7 + '2' + ' ' * 7 + '3')
        # board
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('1' + ' ' * 2 + self.pos[0][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[0][1] + ' ' * 3 + '|' + ' ' * 3 +
              self.pos[0][2] +
              ' ' * 3)
        print('_' * 7 + '|' + '_' * 7 + '|' + '_' * 7)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('2' + ' ' * 2 + self.pos[1][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[1][1] + ' ' * 3 + '|' + ' ' * 3 +
              self.pos[1][
                  2] + ' ' * 3)
        print('_' * 7 + '|' + '_' * 7 + '|' + '_' * 7)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('3' + ' ' * 2 + self.pos[2][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[2][1] + ' ' * 3 + '|' + ' ' * 3 +
              self.pos[2][
                  2] + ' ' * 3)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('')

    def update_pos(self, x, y):
        if self.pos[x][y] == '-':
            self.pos[x][y] = self.turn
            self.turn = 'O' if self.turn == 'X' else 'X'
        else:
            print('invalid position. try again')
        self.draw_board()
        self.check_for_winner()
        return True if self.winner else False

    def check_for_winner(self):
        for y in range(0, 3):
            tmp_hor = []
            tmp_ver = []
            # checks all horizontal and vertical sequences
            for x in range(0, 3):
                tmp_hor.append(self.pos[x][y])
                tmp_ver.append(self.pos[y][x])
                if len(tmp_ver) == 3: self.check_groups(tmp_ver)
                if len(tmp_hor) == 3: self.check_groups(tmp_hor)
            # hardcoding in diagonal sequences
            self.check_groups([self.pos[0][0], self.pos[1][1], self.pos[2][2]])
            self.check_groups([self.pos[2][0], self.pos[1][1], self.pos[0][2]])

    def check_groups(self, seq):
        '''we group together all recurring characters then check if there is more than one group.
        If there are 2 groups or more, the sequence does not have 3 consecutives of any particular key'''
        groups = []
        keys = []
        for k, g in groupby(seq):
            groups.append(list(g))

        if len(groups) == 1 and k != '-':
            self.winner = k

    def getavailablemoves(self):
        self.valid_moves = []
        for row in enumerate(self.pos):
            for col in enumerate(row[1]):
                if col[1] == '-':
                    self.valid_moves.append([row[0], col[0]])

    def validate_input(self, move):
        print("validating input...")
        self.getavailablemoves()
        # try:
        xmove, ymove = map(int, move.split(','))
        # except ValueError:
        #     print("hi")
        # finally:
        return xmove, ymove

    def find_next_move(self, allmoves):
        for move in allmoves:
            newboard = Board(deepcopy(self.pos), self.turn, move[0], move[1])
            next_move = newboard.find_next_move(newboard.valid_moves)
            if len(newboard.valid_moves) == 0:
                newboard = None
        # if len(allmoves) > 1:
        #     for move in allmoves:
        #         print(move)
        #         hypothetical = Board(self.pos, self.turn, move[0], move[1])
        #         if hypothetical.winner:
        #             print(hypothetical.winner + ' would win the match')
        #         else:
        #             hypothetical.getavailablemoves()
        #             hypothetical.find_next_move(hypothetical.valid_moves)
        # elif len(allmoves) > 0:
        #     hypothetical = Board(self.pos, self.turn, allmoves[0][0], allmoves[0][1])

def start_game():
    match = Board([['X', 'O', 'X'], ['-', 'X', '-'], ['-', 'O', '-']], 'O')
    print("make your move, i.e. '3,1' marks the third tile down in the first column.")
    while True:
        match.find_next_move(match.valid_moves)
        move = input()
        xmove, ymove = match.validate_input(move)
        result = match.update_pos(xmove - 1, ymove - 1)
        if result:
            print("Player " + match.winner + " wins!")
            playagain = input("play again? y/n: ")
            break
    return playagain


while True:
    # Start a new game.
    response = start_game()
    # After the game has ended, check if the player wants to play another round
    if response == 'y' or response == 'Y':
        continue
    else:
        break
