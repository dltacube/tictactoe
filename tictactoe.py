from itertools import groupby
import os
from copy import deepcopy, copy


default_pos = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]


class Board:
    score = []
    cpu = None

    def __init__(self, positions=default_pos, row_move='', col_move=''):
        self.pos = positions
        self.row_move = row_move
        self.col_move = col_move
        self.getavailablemoves()
        if row_move != '' and col_move != '':
            self.update_pos(self.row_move, self.col_move)
        o_plays, x_plays = 0, 0
        # determine whose turn it is anytime a new board is created
        for row in self.pos:
            for col in row:
                if col == 'O':
                    o_plays += 1
                if col == 'X':
                    x_plays += 1
        if x_plays > o_plays:
            self.turn = 'O'
        else:
            self.turn = 'X'
        self.winner = False
        self.valid_moves = []
        self.getavailablemoves()
        self.check_for_winner()

    def draw_board(self):
        # clears the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        # line numbers
        print('player ' + self.turn + "'s turn")
        print(' ' * 3 + '0' + ' ' * 7 + '1' + ' ' * 7 + '2')
        # board
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('0' + ' ' * 2 + self.pos[0][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[0][1] + ' ' * 3 + '|' + ' ' * 3 +
              self.pos[0][2] +
              ' ' * 3)
        print('_' * 7 + '|' + '_' * 7 + '|' + '_' * 7)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('1' + ' ' * 2 + self.pos[1][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[1][1] + ' ' * 3 + '|' + ' ' * 3 +
              self.pos[1][
                  2] + ' ' * 3)
        print('_' * 7 + '|' + '_' * 7 + '|' + '_' * 7)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('2' + ' ' * 2 + self.pos[2][0] + ' ' * 3 + '|' + ' ' * 3 + self.pos[2][1] + ' ' * 3 + '|' + ' ' * 3 +
              self.pos[2][
                  2] + ' ' * 3)
        print(' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7)
        print('')

    # make sure that a move is legal
    def update_pos(self, x, y):
        if self.pos[x][y] == '-':
            self.pos[x][y] = self.turn
            self.turn = 'O' if self.turn == 'X' else 'X'
        else:
            print('invalid position. try again')

    # look for a winner. assign winner to self.winner
    def check_for_winner(self):
        for y in range(0, 3):
            tmp_hor = []
            tmp_ver = []
            # checks all horizontal and vertical sequences
            for x in range(0, 3):
                tmp_hor.append(self.pos[x][y])
                tmp_ver.append(self.pos[y][x])
                if len(tmp_ver) == 3:
                    self.check_groups(tmp_ver)
                if len(tmp_hor) == 3:
                    self.check_groups(tmp_hor)
            # hardcoding in diagonal sequences
            self.check_groups([self.pos[0][0], self.pos[1][1], self.pos[2][2]])
            self.check_groups([self.pos[2][0], self.pos[1][1], self.pos[0][2]])

    def check_groups(self, seq):
        '''we group together all recurring characters then check if there is more than one group.
        One group in a sequence means that there are 3 of the same character in a row.
        If there are 2 groups or more, there is no winner yet'''
        groups = []
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
        xmove, ymove = map(int, move.split(','))
        return xmove, ymove
    # generate a list of all possible moves, and assign a score to each end
    # state.

    def find_next_move(self, allmoves, moves=[], levl=0):
        for i in range(len(allmoves)):
                # initialize a new Board() instance with potential move
            newboard = Board(deepcopy(self.pos), self.turn)
            newboard.update_pos(allmoves[i][0], allmoves[i][1])
            newboard.check_for_winner()
            newboard.getavailablemoves()
            moves.append(allmoves[i])
            if newboard.winner:
                if self.turn == self.cpu:
                    self.score.append([10 - levl, levl, copy(moves)])
                else:
                    self.score.append([levl - 10, levl, copy(moves)])
                moves.pop()
            elif len(newboard.valid_moves) < 1:
                # this means no winner - store this list too for stalemates
                self.score.append([0, levl, copy(moves)])
                moves.pop()
            else:
                newboard.find_next_move(newboard.valid_moves, levl=levl + 1)
                moves.pop()
    # from the list of all moves, with their scores, find the path that leads
    # to the highest score

    def find_best_move(self):
        levels = set([l[0] for l in groupby(self.score, key=lambda x: x[1])])
        total = {}
        for move in self.score:
            firstmv = str(move[2][0])
            if firstmv not in total.keys():
                total.update({firstmv: {move[1]: move[0]}})
            else:
                if move[1] not in total[firstmv].keys():
                    total[firstmv].update({move[1]: move[0]})
                else:
                    total[firstmv][move[1]] += move[0]
        for k, v in total.items():
            print(k + ' ' + str(v))

        for level in levels:
            prev_value = None
            tmp = 0
            move = 0
            for k, v in total.items():
                if not level in v.keys():
                    v[level] = 0
                if prev_value is not None:
                    if v[level] > prev_value:
                        move = k
                        tmp = v[level]
                        prev_value = v[level]
                else:
                    prev_value = v[level]
                    tmp = v[level]
                    move = k
            if [v[level] for k, v in total.items()].count(tmp) == 1:
                return move
        return move


def start_game():
    match = Board()
    print("Would you like to play first? y/n")
    firstplayer = input()
    if firstplayer == 'y':
        Board.cpu = 'O'
    else:
        Board.cpu = 'X'
    match.draw_board()
    print("make your move, i.e. '2,0' marks the third tile down in the first column.")
    while True:
        if match.turn == match.cpu:
            Board.score = []
            match.getavailablemoves()
            match.find_next_move(match.valid_moves)
            print('best move:')
            bestmove = match.find_best_move()
            move = str(bestmove[1]) + ', ' + str(bestmove[4])
        else:
            move = input()
        xmove, ymove = match.validate_input(move)
        result = match.update_pos(xmove, ymove)
        match.draw_board()
        match.check_for_winner()
        if match.winner:
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
