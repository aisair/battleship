from prettytable import PrettyTable
from colorama import init, Fore
from string import ascii_uppercase, ascii_lowercase
from itertools import repeat
import random


class Coordinate:
    x = 0
    y = 0


class Ship:
    coord = Coordinate()
    orientation = 0
    length = 0


class Board:
    width = 0
    height = 0
    game = PrettyTable()
    info = []


# game vars
number_turns = 12
number_hits = 0
# board vars
board = Board()
board.height = 5
board.width = 5
# ship vars
ship = [Ship()]
ship[0].length = 3
# dictionaries: currently empty but get filled during game board initiation
letter_to_number = {}
number_to_letter = {}


def print_board(init_board=0):
    if init_board == 1:
        # set fields
        field_names_array = [""]
        for field_name in range(1, board.height + 1):
            field_names_array.append(str(field_name))
        board.game.field_names = field_names_array.copy()
        # insert "O" into every cell
        for board_y in range(board.height):
            number_to_letter[board_y] = ascii_lowercase[board_y]
            letter_to_number[ascii_lowercase[board_y]] = board_y
            board.info.append([])
            for _ in repeat(None, board.width):
                board.info[board_y].append("O")
    board.game.clear_rows()
    for y_index in range(board.height):
        add = [ascii_uppercase[y_index]]
        for x_index in range(board.width):
            add.append(board.info[y_index][x_index])
        board.game.add_row(add)
    print(board.game)


# board.info is stylized board.info[y][x]
def place_ship_random(size):
    ship[0].length = size
    random_coord = Coordinate()
    random_coord.x = random.randint(0, len(board.info[0]) - 1)
    random_coord.y = random.randint(0, len(board.info) - 1)
    ship[0].coord = random_coord
    if size > 1:
        if random.randint(0, 1) == 1:  # vertical
            if (random_coord.y + size) < len(board.info):
                ship[0].orientation = 2
            elif (random_coord.y - size) < len(board.info):
                ship[0].orientation = 0
        else:  # horizontal
            if (random_coord.x + size) < len(board.info[0]):
                ship[0].orientation = 1
            elif (random_coord.x - size) < len(board.info[0]):
                ship[0].orientation = 3


init()  # initiate Colorama for colorful text
print(
    "welcome to battleship!\nthe board is a {board_width} x {board_height} grid.\nthere is one ship that is "
    "{ship_length} unit(s) long.\nyou will get {turns} guesses to find the ship.\ngood luck!".format(ship_length=ship[
        0].length, board_width=board.width, board_height=board.height, turns=number_turns))

print_board(1)  # print and initiate game board
place_ship_random(ship[0].length)

for current_turn in range(number_turns):
    guess = Coordinate()
    print("you are on turn", current_turn + 1, "of", number_turns)
    guess_string = input("input guess: (ex. A1) ")
    if len(guess_string) != 2 or letter_to_number.get(guess_string[0].lower(), "INVALID") == "INVALID":
        print("invalid input!")
        guess.x, guess.y = -1, -1
    else:
        guess.x = int(guess_string[1:]) - 1
        guess.y = letter_to_number.get(guess_string[0].lower())
    if (ship[0].orientation == 0 and guess.x == ship[0].coord.x and guess.y in range(
            ship[0].coord.y - (ship[0].length - 1), ship[0].coord.y + 1)) or (
            ship[0].orientation == 2 and guess.x == ship[0].coord.x and guess.y in range(ship[0].coord.y,
                                                                                         ship[0].coord.y + ship[
                                                                                             0].length)) or (
            ship[0].orientation == 3 and guess.x in range(ship[0].coord.x - (ship[0].length - 1),
                                                          ship[0].coord.x + 1) and guess.y == ship[0].coord.y) or (
            ship[0].orientation == 1 and guess.x in range(ship[0].coord.x,
                                                          ship[0].coord.x + ship[0].length) and guess.y == ship[
                0].coord.y):
        if board.info[guess.y][guess.x] == "O":  # check if the player already guessed that spot
            board.info[guess.y][guess.x] = Fore.RED + "X" + Fore.RESET  # mark hit
            number_hits += 1
            print_board()
            print(Fore.RED + "hit!\nyou hit my ship at " + number_to_letter[guess.y] + str(
                guess.x + 1) + "." + Fore.RESET)
        else:  # if the player already guessed that spot
            print_board()
            print("you seem to have hit the same spot on a"
                  " ship[0].\nno damage taken.")
        if number_hits == ship[0].length:  # check for game end
            print(Fore.GREEN + "the ship sunk!\ncongratulations, you won the game!" + Fore.RESET)
            break
    else:
        if guess.y not in range(board.height) or guess.x not in range(board.width):  # not on board
            print("you missed the ocean!")
        elif board.info[guess.y][guess.x] in ("X", Fore.RED + "X" + Fore.RESET):  # already guessed
            print("you already guessed that location!")
        else:  # on board but not guessed yet
            print("you missed my battleship!")
            board.info[guess.y][guess.x] = "X"
        print_board()
        if current_turn == number_turns - 1:
            print("you have ran out of turns. the game is over!")
            for i in range(ship[0].length):
                if ship[0].orientation == 0:
                    if board.info[ship[0].coord.y - i][ship[0].coord.x] == "O":
                        board.info[ship[0].coord.y - i][ship[0].coord.x] = Fore.GREEN + "X" + Fore.RESET
                if ship[0].orientation == 1:
                    if board.info[ship[0].coord.y][ship[0].coord.x + i] == "O":
                        board.info[ship[0].coord.y][ship[0].coord.x + i] = Fore.GREEN + "X" + Fore.RESET
                if ship[0].orientation == 2:
                    if board.info[ship[0].coord.y + i][ship[0].coord.x] == "O":
                        board.info[ship[0].coord.y + i][ship[0].coord.x] = Fore.GREEN + "X" + Fore.RESET
                if ship[0].orientation == 3:
                    if board.info[ship[0].coord.y][ship[0].coord.x - i] == "O":
                        board.info[ship[0].coord.y][ship[0].coord.x - i] = Fore.GREEN + "X" + Fore.RESET
            print_board()
            print("ship locations are highlighted in green x.")
        else:
            print("you have one ship remaining. it has a length of %d." % ship[0].length)
