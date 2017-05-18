import sys
from itertools import groupby
import os
import ctypes
from copy import deepcopy, copy


# pos = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
default_pos = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
# zebra = 1
class Board:
    # pos = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    # pos = []
    score = []
    cpu = None
    def __init__(self, positions = default_pos, row_move = '', col_move = ''):
        self.pos = positions
        self.row_move = row_move
        self.col_move = col_move
        self.getavailablemoves()
        if row_move != '' and col_move != '':
             self.update_pos(self.row_move, self.col_move)
        o_plays, x_plays = 0,0
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

    def find_next_move(self, allmoves, moves=[], levl=0):
        # global zebra
        # print(zebra)
        # zebra += 1
            for i in range(len(allmoves)):
                newboard = Board(deepcopy(self.pos), self.turn)
                newboard.update_pos(allmoves[i][0], allmoves[i][1])
                newboard.check_for_winner()
                newboard.getavailablemoves()
                moves.append(allmoves[i])
                if newboard.winner:
                    # newboard.draw_board()
                    # print(newboard.winner + ' wins the match')
                    # print(moves)
                    # print('level: ' + str(levl))
                    if self.turn == self.cpu:
                        self.score.append([10 - levl, levl, copy(moves)])
                    else:
                        self.score.append([levl - 10, levl, copy(moves)])
                    # long term storage for movelist goes here
                    moves.pop()
                elif len(newboard.valid_moves) < 1:
                    # print('stalemate')
                    # print(moves)
                    # print('level: ' + str(levl))
                    #this means no winner - store this list too for stalemates
                    self.score.append([0, levl, copy(moves)])
                    moves.pop()
                else:
                    newboard.find_next_move(newboard.valid_moves, levl=levl+1)
                    moves.pop()

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
                    # if (level % 2 == 1) and v[level] < prev_value:
                    #   tmp = v[level]
                    #  prev_value = v[level]
                    # print(tmp)
                    if v[level] > prev_value:  # (level % 2 == 0) and
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


        # bestmove = None
        # prev_value = None
        # for level in levels:
        #     for k, v in total.items():
        #         if not prev_value:
        #             prev_value = 0
        #         if 1 not in v.keys():
        #             if prev_value <= 0:
        #                 bestmove = k
        #                 prev_value = 0
        #         else:
        #             if prev_value < v[1]:
        #                 bestmove = k
        #                 prev_value = v[1]
        #     if not bestmove:
        #         bestmove = self.valid_moves[0]
        #
        # return str(bestmove)

                        # total = {}
        # for move in self.valid_moves:
        #     tmp = 0
        #     for x in self.score:
        #         if x[2][0] == move:
        #             tmp += x[0]
        #     total.update({str(move): tmp})
        # for key in total.keys():
        #     if total[key] == max(total.values()):
        #         return(key)

        # maximin = max(self.score)
        # minimax = min(self.score)
        # if maximin[2][0] == minimax[2][-1]:
        #     return maximin[2][0]
        # if abs(minimax[0]) > abs(maximin[0]):
        #     return minimax[2][-1]
        # else:
        #     return maximin[2][0]


                # if maximin[1] < minimax[1]:
        #     return maximin[2][0]
        # else:
        #     return minimax[2][0]
        # if maximin[2][0] == minimax[2][-1]:
        #     return maximin[2][0]
                # for omove in self.valid_moves:
                #     otmp = 0
                #     for xmove in self.valid_moves:
                #         if xmove != omove:
                #             tmp = 0
                #             for x in self.score:
                #                 if omove == x[2][0] and xmove == x[2][1]:
                #                     tmp += x[0]
                #                     otmp += x[0]
                #             print(str(omove) + ' ' + str(xmove) + ' = ' + str(tmp))
                #     print(str(omove) + ' ' + str(otmp))

                    #
        # firstmoves = []
        # for x in self.score:
        #     firstmoves.append(x[2][0])
        # fmove = []
        # for k, g in groupby(firstmoves):
        #     fmove.append(k)
        # tally = {}
        # for play in self.score:
        #     if play[2][0] in fmove:
        #         if str(play[2][0]) in tally:
        #             tally[str(play[2][0])] = tally[str(play[2][0])] + play[0]
        #         else:
        #             tally[str(play[2][0])] = play[0]

        # get the highest value
        # return sorted(tally, key=tally.get)[0].strip('[]').split(',')
        # ls = []
        # win = []
        # # isolate winning moves
        # for x in self.score:
        #     if x[0] == 10:
        #         ls.append(x[2][0])
        # for move, g in groupby(ls):
        #     win.append(move)
        # winning_tree = [x for x in self.score if x[2][0] in win]
        # # byfirstmove = sorted(winning_tree, key=lambda firstmove: firstmove[2][0])
        # # byscore = sorted(byfirstmove, key=lambda score: score[0])
        # bydepth = sorted(byfirstmove, key=lambda key: key[1])
        # for x in sorted(self.score, key=lambda firstmove: firstmove[2][0]):
        #     if x[2][0] in win:
        #         print(x)


def start_game():
    # match = Board([['X', 'O', 'X'], ['-', 'X', '-'], ['-', 'O', '-']], 'O')
    # match = Board([['X', 'O', 'X'], ['-', 'O', '-'], ['-', '-', '-']], 'X')
    # match = Board([['O', '-', '-'], ['X', 'X', '-'], ['O', '-', 'X']], 'O')
    # Board.cpu = 'O'
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
        # Board.cpu = 'O'
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
