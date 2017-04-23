import sys
from itertools import groupby
import os


# pos = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

class board():
    turn = 'X'
    winner = False
    pos = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def __init__(self):
        self.draw_board()
        self.pos = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def draw_board(self):
        # clears the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        # line numbers
        print('player ' + self.turn + "'s turn")
        print(' ' * 3 + '1' + ' ' * 7 + '2' + ' ' * 7 + '3')
        # board
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('1' + ' ' * 2 + self.pos[0][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[0][1] + ' ' * 3 + '|' + ' ' * 3 + self.pos[0][2] +
              ' ' * 3)
        print('_' * 7 + '|' + '_' * 7 + '|' + '_' * 7)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('2' + ' ' * 2 + self.pos[1][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[1][1] + ' ' * 3 + '|' + ' ' * 3 + self.pos[1][
            2] + ' ' * 3)
        print('_' * 7 + '|' + '_' * 7 + '|' + '_' * 7)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('3' + ' ' * 2 + self.pos[2][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[2][1] + ' ' * 3 + '|' + ' ' * 3 + self.pos[2][
            2] + ' ' * 3)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('')

    def update_pos(self, x, y):
        if self.pos[x][y] == '-':
            self.pos[x][y] = self.turn
            self.turn = 'O' if self.turn == 'X' else 'X'
            self.check_for_winner()
        else:
            print('invalid position. try again')
        self.draw_board()
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


def start_game():
    match = board()
    print("make your move, i.e. '3,1' marks the third tile down in the first column.")
    while True:
        move = input()
        xmove, ymove = map(int, move.split(','))
        result = match.update_pos(xmove - 1, ymove - 1)
        if result:
            print("Player " + match.winner + " wins!")
            playagain = input("play again? y/n: ")
            break
    return playagain

while True:
    response = start_game()
    if response == 'y' or response == 'Y':
        continue
    else:
        break

