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


class Coordinate:
    x = 0
    y = 0


class Ship:
    orientation_vert = 0
    coord_1 = [0, 0]  # stylized x, y
    coord_2 = [0, 0]


# start with a 5 by 5 board filled with "O"s
game_board = PrettyTable()
board_rows = 5
board_columns = 5
board_info = []
ship = Ship


def print_board(init_board=0):
    if init_board == 1:
        game_board.field_names = ["", "1", "2", "3", "4", "5"]
        i = 0
        while i < board_rows:
            board_info.append([])
            j = 0
            while j < board_columns:
                board_info[i].append("O")
                j += 1
            i += 1

    game_board.clear_rows()
    game_board.add_row(["A", board_info[0][0], board_info[0][1], board_info[0][2], board_info[0][3], board_info[0][4]])
    game_board.add_row(["B", board_info[1][0], board_info[1][1], board_info[1][2], board_info[1][3], board_info[1][4]])
    game_board.add_row(["C", board_info[2][0], board_info[0][1], board_info[2][2], board_info[2][3], board_info[2][4]])
    game_board.add_row(["D", board_info[3][0], board_info[0][1], board_info[3][2], board_info[3][3], board_info[3][4]])
    game_board.add_row(["E", board_info[4][0], board_info[0][1], board_info[4][2], board_info[4][3], board_info[4][4]])
    print(game_board)


# boardinfo is stylized board_info[y][x]
def place_ship_random(size):
    random_x = random.randint(0, len(board_info[0]) - 1)
    random_y = random.randint(0, len(board_info) - 1)
    if size > 1:
        if random.randint(0, 1) == 1:  # vertical
            ship.orientation_vert = 1
            if (random_y + size) < len(board_info):
                ship.coord_1[0] = random_x
                ship.coord_1[1] = random_y
                ship.coord_2[0] = random_x
                ship.coord_2[1] = random_y + (size - 1)
            elif (random_y - size) < len(board_info):
                ship.coord_1[0] = random_x
                ship.coord_1[1] = random_y
                ship.coord_2[0] = random_x
                ship.coord_2[1] = random_y - (size - 1)
            else:
                return "not possible!"
        else:  # horizontal
            ship.orientation_vert = 0
            if (random_x + size) < len(board_info[0]):
                ship.coord_1[0] = random_x
                ship.coord_1[1] = random_y
                ship.coord_2[0] = random_x + (size - 1)
                ship.coord_2[1] = random_y
            elif (random_x - size) < len(board_info[0]):
                ship.coord_1[0] = random_x
                ship.coord_1[1] = random_y
                ship.coord_2[0] = random_x - (size - 1)
                ship.coord_2[1] = random_y
            else:
                return "not possible!"
    elif size == 1:
        ship.coord_1[0] = random_x
        ship.coord_1[1] = random_y
        ship.coord_2 = ship.coord_1


print("Welcome to Battleship! There is one ship that is one unit long.\nThe board is a 5 x 5 grid. You will get",
      number_turns, "guesses to find the ship. Good luck!")

print_board(1)  # initiating game board
place_ship_random(3)

print("coord1:", ship.coord_1, "\ncoord2:", ship.coord_2)
# Start the game play. If  you want to add delays, so the game plays more naturally use time.sleep(seconds)

# We need to randomly place the ship on the board. The x-coordinate should have value between 0 and 4. If this were a
# C, B or A level project you would also have to randomly choose vertical or horizontal

# The C level will need an extra function and variable to keep track of vertical or horizontal for the 3 x 1 ship.

# For Testing Where Is The Ship?

# For the higher level projects, you will need to make sure the ships do not go off the board, and do not overlap.

# The next 2 lines are to check where the ship is being placed. so should be removed for final game


# Let the player guess where the ship is. For the basic game we will let the player input integers, but for the real
# battleship game, you will need to enter inputs as "C4" or "D5". so the this row input should be a letter in the
# version you build.
for current_turn in range(number_turns):
    guess = Coordinate
    print("You are on turn ", current_turn + 1, "of", number_turns)
    guess_string = input("Input guess: (ex. A1) ")
    if len(guess_string) != 2:
        print("The guess is not valid!")
    else:
        switch = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
        }
        guess.x = switch.get(guess_string[0])
        guess.y = int(guess.y) - 1

    # Check if the guess is a hit or a miss, or not on the board.
    # When you build the game make sure to let them know if they already guessed that spot.

    if guess.x == range(ship.coord_1[0], ship.coord_2[0]) and guess.y == range(ship.coord_1[1], ship.coord_2[1]):
        board_info[guess.y][guess.x] = Fore.RED + "X" + Fore.RESET
        # This is a hit
        print_board()
        print("You sank my battleship!")
        break
    else:
        if guess.y not in range(len(board_info)) or guess.x not in range(len(board_info[0])):
            print("You missed the ocean!")
        elif board_info[guess.y][guess.x] == "X":
            print("You already guessed that location!")
        else:
            print("You missed my battleship!")
            board_info[guess.y][guess.x] = "X"
        if current_turn == number_turns - 1:
            print("You have ran out of turns. The game is over!")
            print("The ship was at row %d and column %d" % ship.y, ship.x) # later change it to show the board with all ships highlighted
        print_board()

        # Your print statement should should update how many ships are remaining and how many are sunk from your set of
        # ships.
        print("You have one ship remaining. It is a 1 x 1 unit.")

# Convert Letters to numbers.
