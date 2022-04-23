import sys

# Convert command line arguments into dictionary format
lst = sys.argv
# print(lst)

def Convert(lst):
    for x in range(len(lst)):
        res_dct = {lst[i]: int(lst[i + 1]) for i in range(x+1, len(lst), 2)}
        return res_dct

dict=Convert(lst)
print(dict)

# Hard-coded board size and number of conects/pieces
BOARD_ROWS = 6
BOARD_COLS = 7
PIECES = 3

for k,v in dict.items():
    if k=="-r":
        BOARD_ROWS=v
        if BOARD_ROWS<=0:
            BOARD_ROWS=int(input("Please enter a positive, non-zero integer for the number of rows:"))
    elif k=="-c":
        BOARD_COLS=v
        if BOARD_COLS<=0:
            BOARD_COLS=int(input("Please enter a positive, non-zero integer for the number of columns:"))
    elif k=="-p":
        PIECES=v
        if PIECES<=0:
            PIECES=int(input("Please enter a positive, non-zero integer for the number of pieces to connect:"))
    else:
        print("wrong input given")

print("BOARD_ROWS: ",BOARD_ROWS)
print("BOARD_COLS: ",BOARD_COLS)
print("PIECES: ",PIECES)
first_player=str(input("Player one, do you want red or yellow (r or y)?"))

# Game board object
class Board():
    def __init__(self):
        self.board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.turns = 0
        self.last_move = [-1, -1] # [r, c]

    def print_board(self):
        print("\n")
        # Number the columns seperately to keep it cleaner
        for r in range(BOARD_COLS):
            print(f"  ({r+1}) ", end="")
        print("\n")

        # Print the slots of the game board
        for r in range(BOARD_ROWS):
            print('|', end="")
            for c in range(BOARD_COLS):
                print(f"  {self.board[r][c]}  |", end="")
            print("\n")
            print(f"{'-' * 42}\n")

        # print(f"{'-' * 42}\n")

    def which_turn(self):
        if first_player=='r':
            players = ['r', 'y']
        else:
            players = ['y', 'r']
        return players[self.turns % 2]
    
    def in_bounds(self, r, c):
        return (r >= 0 and r < BOARD_ROWS and c >= 0 and c < BOARD_COLS)

    def turn(self, column):
        # Search bottom up for an open slot
        for i in range(BOARD_ROWS-1, -1, -1):
            if self.board[i][column] == ' ':
                self.board[i][column] = self.which_turn()
                self.last_move = [i, column]

                self.turns += 1
                return True

        return False

    def check_winner(self):
        last_row = self.last_move[0]
        last_col = self.last_move[1]
        last_letter = self.board[last_row][last_col]

        # [r, c] direction, matching letter count, locked bool
        directions = [[[-1, 0], 0, True], 
                      [[1, 0], 0, True], 
                      [[0, -1], 0, True],
                      [[0, 1], 0, True],
                      [[-1, -1], 0, True],
                      [[1, 1], 0, True],
                      [[-1, 1], 0, True],
                      [[1, -1], 0, True]]
        
        # Search outwards looking for matching pieces
        for a in range(PIECES):
            for d in directions:
                r = last_row + (d[0][0] * (a+1))
                c = last_col + (d[0][1] * (a+1))

                if d[2] and self.in_bounds(r, c) and self.board[r][c] == last_letter:
                    d[1] += 1
                else:
                    # Stop searching in this direction
                    d[2] = False

        # Check possible direction pairs for '4 pieces in a row'
        for i in range(0, BOARD_COLS, 2):
            if (directions[i][1] + directions[i+1][1] >= PIECES-1):
                self.print_board()
                print(f"{last_letter} is the winner!")
                again = int(input("Do you want to play again (0-no, 1-yes)?"))
                if again == 1:
                    play()
                else:
                    print("Thankyou !!!")
                    sys.exit(0)
                return last_letter   

        # Did not find any winners
        return False

def play():
    game = Board()

    game_over = False
    while not game_over:
        game.print_board()

        # Ask the user for input, but only accept valid turns
        valid_move = False
        while not valid_move:
            user_move = input(f"Player {game.which_turn()}, what column(1-{BOARD_COLS}) do you want to put your piece? ")
            try:
                valid_move = game.turn(int(user_move)-1)
            except:
                print(f"Please choose a number between 1 and {BOARD_COLS}")

        # End the game if there is a winner
        game_over = game.check_winner()
        
        # End the game if there is a tie
        if not any(' ' in x for x in game.board):
            print("The game is a draw..")
            return

        
if __name__ == '__main__':
    play()