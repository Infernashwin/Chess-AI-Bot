import chess as CHS
import random as r

MAX_VALUE = 9999999
MIN_VALUE = -MAX_VALUE
class chess_engine:

    def __init__(self, board, max_depth, colour):
        self.board = board
        self.colour = colour
        self.depth = max_depth

    def best_move(self):
        return self.calculate(None, 1)

    def eval_pos(self):
        score = 0
        for i in range(64):
            score += self.square_points(CHS.SQUARES[i])
        score += self.can_mate() + self.openning() + 0.1*r.random()
        return score

    def square_points(self, square):
        value = 0
        if self.board.piece_type_at(square) == CHS.PAWN:
            value = 1
        elif self.board.piece_type_at(square) == CHS.ROOK:
            value = 5
        elif self.board.piece_type_at(square) == CHS.BISHOP:
            value = 3
        elif self.board.piece_type_at(square) == CHS.KNIGHT:
            value = 3
        elif self.board.piece_type_at(square) == CHS.QUEEN:
            value = 9

        return value*(1 - 2*(self.board.color_at(square)!=self.colour))

    def can_mate(self):
        if self.board.legal_moves.count()==0:
            if (self.board.turn) == self.colour:
                return MAX_VALUE
            else:
                return MIN_VALUE
        return 0

    def openning(self):
        if self.board.fullmove_number<10:
            if self.board.turn == self.colour:
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        return 0

    def calculate(self, position_score, depth):
        if depth == self.depth or self.board.legal_moves.count() == 0:
            return self.eval_pos()

        else:
            pos_moves = list(self.board.legal_moves)

            new_position_score = float("inf")*(1 - 2*(depth%2))
            for move in pos_moves:
                self.board.push(move)
                value = self.calculate(new_position_score, depth + 1)
                if value > new_position_score and depth%2:
                    if depth == 1:
                        play = move
                    new_position_score = value

                elif value < new_position_score and not depth%2:
                    new_position_score = value

                if position_score != None and value < position_score and not depth%2:
                    self.board.pop()
                    break

                elif position_score != None and value > position_score and depth%2:
                    self.board.pop()
                    break

                self.board.pop()

            if depth>1:
                return new_position_score
            else:
                return play
