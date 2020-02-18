from prettytable import PrettyTable
from colorama import init, Fore
from string import ascii_uppercase, ascii_lowercase
import random
import re


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
    info = []  # board visual contents
    state = []  # shows ship locations


# game vars
number_turns = 70
number_hits = 0
total_hits = 0
number_ships = 3
# board vars
board = Board()
board.height = 10
board.width = 10
# ship vars
ships = []
for _ in range(number_ships):
    ships.append(Ship())
ships[0].length = 3
ships[1].length = 4
ships[2].length = 5
# dictionaries: currently empty but get filled during game board initiation
letter_to_number = {}
number_to_letter = {}


def print_board():
    game_board = PrettyTable()
    column_labels = []
    for char in ascii_uppercase[:10]:
        column_labels.append(char)
    game_board.add_column("", column_labels)
    for x_index in range(board.width):
        game_board.add_column(str(x_index + 1), board.info[x_index])
    print(game_board)


# board.info is stylized board.info[y][x]
def place_ship_random(index):
    orientation = 0
    size = ships[index].length
    random_coord = Coordinate()
    valid = 0
    while valid == 0:
        valid = 1
        random_coord.x = random.randint(0, len(board.info[0]) - 1)
        random_coord.y = random.randint(0, len(board.info) - 1)
        if size > 1:
            # check if ships are inside the board
            if random.randint(0, 1) == 1:  # vertical
                if (random_coord.y - size) > -2:
                    for size_check_index in range(size - 1):
                        if board.state[random_coord.x][random_coord.y - size_check_index] == 1:
                            valid = 0
                    if valid == 1:
                        for state_update_index in range(size - 1):
                            board.state[random_coord.x][random_coord.y - state_update_index] = 1
                    orientation = 0
                elif (random_coord.y + size) < board.height:
                    for size_check_index in range(size - 1):
                        if board.state[random_coord.x][random_coord.y + size_check_index] == 1:
                            valid = 0
                    if valid == 1:
                        for state_update_index in range(size - 1):
                            board.state[random_coord.x][random_coord.y + state_update_index] = 1
                    orientation = 2
            else:  # horizontal
                if (random_coord.x + size) < board.width:
                    for size_check_index in range(size - 1):
                        if board.state[random_coord.x + size_check_index][random_coord.y] == 1:
                            valid = 0
                    if valid == 1:
                        for state_update_index in range(size - 1):
                            board.state[random_coord.x + state_update_index][random_coord.y] = 1
                    orientation = 1
                elif (random_coord.x - size) > -2:
                    for size_check_index in range(size - 1):
                        if board.state[random_coord.x - size_check_index][random_coord.y] == 1:
                            valid = 0
                    if valid == 1:
                        for state_update_index in range(size - 1):
                            board.state[random_coord.x - state_update_index][random_coord.y] = 1
                    orientation = 3
    ships[index].coord = random_coord
    ships[index].orientation = orientation


init()  # initiate Colorama for colorful text
# define dictionaries
if board.width > board.height:
    for number in range(board.width):
        number_to_letter[number] = ascii_lowercase[number]
        letter_to_number[ascii_lowercase[number]] = number
else:
    for number in range(board.height):
        number_to_letter[number] = ascii_lowercase[number]
        letter_to_number[ascii_lowercase[number]] = number
# insert "O" into every cell of board.info and 0 into every cell of board.state
for board_x in range(board.width):
    board.info.append([])
    board.state.append([])
    for _ in range(board.height):
        board.info[board_x].append("O")
        board.state[board_x].append(0)
place_ship_random(0)
place_ship_random(1)
place_ship_random(2)
for ship_index in ships:
    total_hits += ship_index.length
print(
    "welcome to battleship!\nthe board is a {board_width} x {board_height} grid.\nthere are {number} ships that have a "
    "combined length of {ship_lengths} units.\nyou will get {turns} guesses to find the ship.\ngood "
    "luck!".format(number=number_ships, ship_lengths=total_hits, board_width=board.width, board_height=board.height,
                   turns=number_turns))
print_board()  # print the game board

for current_turn in range(number_turns - 1):
    guess = Coordinate()
    guess.x = None
    guess.y = None
    print("you are on turn", current_turn + 1, "of", number_turns)
    while guess.x is None and guess.y is None:  # loop while user's guess is invalid
        guess_string = input("input guess: (ex. A1) ")
        if len(guess_string) < 2 or guess_string[0] not in letter_to_number or re.search('[a-zA-Z]', guess_string[1:]) \
                or int(guess_string[1:]) - 1 not in number_to_letter:
            print("invalid input!")
        else:
            guess.x = int(guess_string[1:]) - 1
            guess.y = letter_to_number.get(guess_string[0].lower())
            hit = 0
            for current_ship in ships:
                if (current_ship.orientation == 0 and guess.x == current_ship.coord.x and guess.y in range(
                        current_ship.coord.y - (current_ship.length - 1), current_ship.coord.y + 1)) or (
                        current_ship.orientation == 2 and guess.x == current_ship.coord.x and guess.y in range(
                        current_ship.coord.y, current_ship.coord.y + ships[0].length)) or (
                        current_ship.orientation == 3 and guess.x in range(
                        current_ship.coord.x - (current_ship.length - 1),
                        current_ship.coord.x + 1) and guess.y == current_ship.coord.y) or (
                        current_ship.orientation == 1 and guess.x in range(current_ship.coord.x,
                                                                           current_ship.coord.x + current_ship.length) and guess.y ==
                        ships[0].coord.y):  # check if player hit a ship
                    hit = 1
                    if board.info[guess.x][guess.y] == "O":  # check if the player hasn't already guessed that spot
                        board.info[guess.x][guess.y] = Fore.RED + "X" + Fore.RESET  # mark hit
                        number_hits += 1
                        print_board()
                        print(Fore.RED + "hit!\nyou hit one of my ships at " + number_to_letter[guess.y] + str(
                            guess.x + 1) + "." + Fore.RESET)
                    else:  # if the player already guessed that spot
                        print_board()
                        print("you seem to have hit the same spot on a"
                              " ship.\nno damage taken.")
                    if number_hits == total_hits:  # check for game end
                        secret_string = ""
                        if current_turn + 1 < total_hits:
                            secret_string = " how did you do it?"
                        print(Fore.GREEN + "all ships sunk!\ncongratulations, you won the game in {turns} turns!"
                                           "{secret}".format(turns=current_turn + 1, secret=secret_string) + Fore.RESET)
                        exit()
            if hit == 0:
                if guess.x not in range(len(board.info)) or guess.y not in range(len(board.info[0])):  # not on board
                    print("you missed the ocean!")
                elif board.info[guess.x][guess.y] in ("-", Fore.RED + "X" + Fore.RESET):  # already guessed
                    print("you already guessed that location!")
                else:  # on board but not guessed yet
                    print("you missed my battleship!")
                    board.info[guess.x][guess.y] = "-"
                print_board()
print("you have ran out of turns. the game is over!")
for ship_index in ships:
    for i in range(ship_index.length):
        if ship_index.orientation == 0:
            if board.info[ship_index.coord.x][ship_index.coord.y - i] == "O":
                board.info[ship_index.coord.x][ship_index.coord.y - i] = Fore.GREEN + "X" + Fore.RESET
        if ship_index.orientation == 1:
            if board.info[ship_index.coord.x + i][ship_index.coord.y] == "O":
                board.info[ship_index.coord.x + i][ship_index.coord.y] = Fore.GREEN + "X" + Fore.RESET
        if ship_index.orientation == 2:
            if board.info[ship_index.coord.x][ship_index.coord.y + i] == "O":
                board.info[ship_index.coord.x][ship_index.coord.y + i] = Fore.GREEN + "X" + Fore.RESET
        if ship_index.orientation == 3:
            if board.info[ship_index.coord.x - i][ship_index.coord.y] == "O":
                board.info[ship_index.coord.x - i][ship_index.coord.y] = Fore.GREEN + "X" + Fore.RESET
print_board()
print("ship locations are highlighted in green x.")
