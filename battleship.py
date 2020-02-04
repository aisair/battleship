# This is the in-class tutorial for a basic battle ship game. This game will have one ship, one unit long.  To get a
# C, the game will need 1 ship 3 units long. To get a B, the game should have 3 ships  of different lengths,
# randomly placed vertically or horizontally on the board. To get an A, there must be a computer playing a person
# player.

from prettytable import PrettyTable
from colorama import init, Fore
import random
import time

init()  # initiate colorama for colorful text

number_turns = 12

# start with a 5 by 5 board
game_board = PrettyTable()
board_info = [[], [], [], [], []]
board_info[0].append("-")

# function to print the board
game_board.clear()
game_board.field_names = ["", "1", "2", "3", "4", "5"]
game_board.add_row(["A", board_info[0][0], board_info[0][1], board_info[0][2], board_info[0][3], board_info[0][4]])
game_board.add_row(["B", board_info[1][0], board_info[1][1], board_info[1][2], board_info[1][3], board_info[1][4]])
game_board.add_row(["C", board_info[2][0], board_info[0][1], board_info[2][2], board_info[2][3], board_info[2][4]])
game_board.add_row(["D", board_info[3][0], board_info[0][1], board_info[3][2], board_info[3][3], board_info[3][4]])
game_board.add_row(["E", board_info[4][0], board_info[0][1], board_info[4][2], board_info[4][3], board_info[4][4]])

"""
print(
    "Welcome to Battleship! There is one ship that is one unit long.\nThe board is a 5 x 5 grid. You will get"
    , number_turns, "guesses to find the ship. Good luck!")

print_board(game_board)

# Start the game play. If  you want to add delays, so the game plays more naturally use time.sleep(seconds)
time.sleep(1)


# We need to randomly place the ship on the board. The x-coordinate should have value between 0 and 4. If this were a
# C, B or A level project you would also have to randomly choose vertical or horizontal
def random_row(board):
    return random.randint(0, len(board) - 1)


def random_column(board):
    return random.randint(0, len(board[0]) - 1)


# The C level will need an extra function and variable to keep track of vertical or horizontal for the 3 x 1 ship.
ship_row = random_row(game_board)
ship_column = random_column(game_board)

# For Testing Where Is The Ship?
print("ship row:", ship_row + 1)
print("ship column:", ship_column + 1)

# For the higher level projects, you will need to make sure the ships do not go off the board, and do not overlap.

# The next 2 lines are to check where the ship is being placed. so should be removed for final game


# Let the player guess where the ship is. For the basic game we will let the player input integers, but for the real
# battleship game, you will need to enter inputs as "C4" or "D5". so the this row input should be a letter in the
# version you build.
for current_turn in range(number_turns):
    guess_row = 0
    guess_column = 0
    print("You are on turn ", current_turn + 1, "of", number_turns)
    guess = input("Input guess: ")
    if len(guess) != 2:
        print("The guess is not valid!")
    else:
        switch = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
        }
        guess_row = switch.get(guess[0])
        guess_column = int(guess[1]) - 1

    # Check if the guess is a hit or a miss, or not on the board.
    # When you build the game make sure to let them know if they already guessed that spot.

    if guess_row == ship_row and guess_column == ship_column:
        game_board[guess_row][guess_column] = Fore.RED + "X" + Fore.RESET
        # This is a hit
        print_board(game_board)
        print("You sank my battleship!")
        break
    else:
        if guess_row not in range(5) or \
                guess_column not in range(5):
            print("You missed the ocean!")
        elif game_board[guess_row][guess_column] == "X":
            print("You already guessed that location!")
        else:
            print("You missed my battleship!")
            game_board[guess_row][guess_column] = "X"
        if current_turn == number_turns - 1:
            print("You have ran out of turns. The game is over!")
            print("The ship was at row %d and column %d" % ship_row, ship_column)
        print_board(game_board)

        # Your print statement should should update how many ships are remaining and how many are sunk from your set of
        # ships.
        print("You have one ship remaining. It is a 1 x 1 unit.")

# Convert Letters to numbers.
"""
