# This is the in-class tutorial for a basic battle ship game. This game will have one ship, one unit long.  To get a
# C, the game will need 1 ship 3 units long. To get a B, the game should have 3 ships  of different lengths,
# randomly placed vertically or horizontally on the board. To get an A, there must be a computer playing a person
# player.

from prettytable import PrettyTable
from colorama import init, Fore
import random

init()  # initiate colorama for colorful text

number_turns = 12


class Coordinate:
    def __init__(self):
        self.x = 0
        self.y = 0

    x = 0
    y = 0


class Ship:
    orientation = 0
    coord = Coordinate()
    coord_2 = Coordinate()
    length = 0

    def __init__(self):
        self.length = 0
        self.orientation = 0


# start with a 5 by 5 board filled with "O"s
game_board = PrettyTable()
board_rows = 5
board_columns = 5
board_info = []
ship = Ship
lettertrans = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
}


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


# board_info is stylized board_info[y][x]
def place_ship_random(size):
    random_coord = Coordinate()
    random_coord.x = random.randint(0, len(board_info[0]) - 1)
    random_coord.y = random.randint(0, len(board_info) - 1)
    ship.coord = random_coord
    ship.length = size
    if size > 1:
        if random.randint(0, 1) == 1:  # vertical
            if (random_coord.y + size) < len(board_info):
                ship.orientation = 2
            elif (random_coord.y - size) < len(board_info):
                ship.orientation = 0
        else:  # horizontal
            if (random_coord.x + size) < len(board_info[0]):
                ship.orientation = 1
            elif (random_coord.x - size) < len(board_info[0]):
                ship.orientation = 3


print("Welcome to Battleship! There is one ship that is", ship.length + 1, "unit(s) long.\nThe board is a 5 x 5 grid. "
                                                                           "You will get", number_turns, "guesses to "
                                                                                                         "find the "
                                                                                                         "ship. Good "
                                                                                                         "luck!")

print_board(1)  # initiating game board
place_ship_random(1)

print(Fore.RED + "DEBUG:\nShip Location:\nco-ord:", ship.coord.x, ship.coord.y, "\nlength:", ship.length,
      "\norientation:", ship.orientation, Fore.RESET)
# Start the game play. If  you want to add delays, so the game plays more naturally use time.sleep(seconds)

# We need to randomly place the ship on the board. The x-coordinate should have value between 0 and 4. If this were a
# C, B or A level project you would also have to randomly choose vertical or horizontal
# For the higher level projects, you will need to make sure the ships do not go off the board, and do not overlap.

# Let the player guess where the ship is. For the basic game we will let the player input integers, but for the real
# battleship game, you will need to enter inputs as "C4" or "D5". so the this row input should be a letter in the
# version you build.
for current_turn in range(number_turns):
    guess = Coordinate()
    print("You are on turn ", current_turn + 1, "of", number_turns)
    guess_string = input("Input guess: (ex. A1) ")
    if len(guess_string) != 2:
        print("The guess is not valid!")
    else:
        guess.y = lettertrans.get(guess_string[0].lower(), "INVALID")
        if guess.y == "INVALID":
            print("invalid input!")
            break
        guess.x = int(guess_string[1]) - 1
    if (ship.orientation == 0 and guess.x == ship.coord.x and guess.y in range(ship.coord.y - (ship.length - 1),
                                                                               ship.coord.y + 1)) or (
            ship.orientation == 1 and guess.x in range(ship.coord.x,
                                                       ship.coord.x + ship.length) and guess.y == ship.coord.y) or (
            ship.orientation == 2 and guess.x == ship.coord.x and guess.y in range(ship.coord.y + (ship.length - 1),
                                                                                   ship.coord.y + 1)) or (
            ship.orientation == 3 and guess.x in range(ship.coord.x - (ship.length - 1),
                                                       ship.coord.x + 1) and guess.y == ship.coord.y):
        # guess.x in range(ship.coord.x, ship.coord.x + ship.length - 1) and guess.y in range(ship.coord.y, ship.coord.y
        # + ship.length - 1):
        board_info[guess.y][guess.x] = Fore.RED + "X" + Fore.RESET  # mark hit
        print_board()
        print(Fore.RED + "Hit!\nYou hit my ship at (" + str(guess.x + 1) + ", " + str(guess.y + 1) + ")." + Fore.RESET)
    else:
        if guess.y not in range(len(board_info)) or guess.x not in range(len(board_info[0])):  # not on board
            print("You missed the ocean!")
        elif board_info[guess.y][guess.x] == "X":  # already guessed
            print("You already guessed that location!")
        else:  # on board but not guessed yet
            print("You missed my battleship!")
            board_info[guess.y][guess.x] = "X"
        if current_turn == number_turns - 1:
            print("You have ran out of turns. The game is over!")
            print("The ship was at row %d and column %d" % ship.coord.y, ship.coord.x)
            # later change it to show the board with all ships highlighted
        print_board()

        # Your print statement should should update how many ships are remaining and how many are sunk from your set of
        # ships.
        print("You have one ship remaining. It is a 1 x 1 unit.")
