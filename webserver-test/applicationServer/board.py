import random
import json

class Board:
    def __init__(self):
        self.board = []
        self.winner = None
        self.available = []
        self.reset()
        
    #Resets the board
    def reset(self):
        self.board = [
            [None for x in range(0,3)]
            for y in range(0,3)
        ]

        self.winner = None
        self.available = self.available_moves()

    #Returns the board
    def get_board(self):
        return self.board

    #Allow the Player to move
    def player_move(self, move : (int,int)) -> str:
        print(self.winner)
        if self.winner != None:
            return "{}"

        (row, col) = move
        pcmove = (3,3)

        #Assure position isn't taken!
        if (row, col) not in self.available:
            return "{}"

        self.board[row][col] = "Player"
        self.available.remove((row,col))

        #Has the Player won?
        if self.game_over((row,col)):
            response = json.JSONEncoder().encode({"winner":self.winner, "move":(3,3)})
            return response

        #If not, let the Computer move
        pcmove = self.pc_move()
        pcrow = pcmove[0]
        pccol = pcmove[1]

        #Has the Computer won?
        if self.game_over((pcrow, pccol)):
            response = json.JSONEncoder().encode({"winner":self.winner, "move":(pcrow+1, pccol+1)})
            return response

        #If not, return Computer's move
        response = json.JSONEncoder().encode({"winner":self.winner, "move":(pcrow+1, pccol+1)})
        
        return response
        


    #Simple logic behind the Computer's turn
    def pc_move(self) -> (int,int):

        #Just pick a random available move
        move = random.choice(self.available)

        row = move[0]
        col = move[1]
        self.board[row][col] = "Computer"
        self.available.remove(move)
        return (row,col)



    """
    Gets available moves at beginning,
    then maintains the available moves by removing
    from the self.available list.
    """
    def available_moves(self) -> []:
        pairs = []

        for row in range(0, len(self.board)):
            for col in range(0, len(self.board)):

                if self.board[row][col] == None:
                    pairs.append((row,col))

        return pairs


    """
    Game rules & logic behind winning
    """

    #Determines if it's game over
    def game_over(self, move : (int,int)) -> bool:
        (row, col) = move

        #Check if the new 'move' makes three in a row
        if self.check_column(col) or self.check_vertical(row) or self.check_diag_left() or self.check_diag_right():
            self.winner = self.board[row][col]

        #When there are no more moves
        elif len(self.available) < 1:
            self.winner = "Tie"
        else:
            return False

        return True


    def check_column(self, col : int) -> bool:
        for row in range(1, len(self.board)):
            if self.board[row - 1][col] != self.board[row][col]:
                return False
        return True

    def check_vertical(self, row : int) -> bool:
        for col in range(1, len(self.board)):
            if self.board[row][col] == None:
                return False

            if self.board[row][col - 1] != self.board[row][col]:
                return False
        return True

    def check_diag_left(self) -> bool:
        for cell in range(1, len(self.board)):
            if self.board[cell][cell] == None:
                return False

            if self.board[cell - 1][cell - 1] != self.board[cell][cell]:
                return False
        return True

    def check_diag_right(self) -> bool:
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[1][1] != None:
                return True
        else:
            return False