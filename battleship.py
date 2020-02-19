import copy
from prettytable import PrettyTable
from colorama import init, Fore
from string import ascii_uppercase, ascii_lowercase
import random
import re


class Coordinate:
    def __init__(self):
        self.x = 0
        self.y = 0


class Ship:
    def __init__(self, coord, length, orientation):
        self.coord = coord
        self.orientation = orientation
        self.length = length
        self.damage = 0


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.info = []  # board visual contents
        self.state = []  # shows ship locations


# game vars
number_turns = 70
number_ships = 3
number_hits = 0
total_hits = 0
# board vars
player_board = Board(10, 10)
# ship var
ships = []
# dictionaries: currently empty but get filled during game board initiation
letter_to_number = {}
number_to_letter = {}


def print_board():
    game_board = PrettyTable()
    column_labels = []
    for char in ascii_uppercase[:10]:
        column_labels.append(char)
    game_board.add_column("", column_labels)
    for x_index in range(player_board.width):
        game_board.add_column(str(x_index + 1), player_board.info[x_index])
    print(game_board)


def generate_ship_random(length):  # generates and returns a random but valid Ship object
    random_coord = Coordinate()
    orientation = 0
    valid = 0
    while valid == 0:
        valid = 1
        random_coord.x = random.randint(0, player_board.width - 1)
        random_coord.y = random.randint(0, player_board.height - 1)
        if length > 1:  # check if ships are inside the board and not overlapping
            if random.randint(0, 1) == 1:  # vertical
                if (random_coord.y - length) > -2:  # up
                    orientation = 0
                    for length_check_index in range(length - 1):
                        if player_board.state[random_coord.x][random_coord.y - length_check_index] == 1:
                            valid = 0
                elif (random_coord.y + length) < player_board.height:  # down
                    orientation = 2
                    for length_check_index in range(length - 1):
                        if player_board.state[random_coord.x][random_coord.y + length_check_index] == 1:
                            valid = 0
            else:  # horizontal
                if (random_coord.x + length) < player_board.width:  # right
                    orientation = 1
                    for length_check_index in range(length - 1):
                        if player_board.state[random_coord.x + length_check_index][random_coord.y] == 1:
                            valid = 0
                elif (random_coord.x - length) > -2:  # left
                    orientation = 3
                    for length_check_index in range(length - 1):
                        if player_board.state[random_coord.x - length_check_index][random_coord.y] == 1:
                            valid = 0
    return Ship(random_coord, length, orientation)


def update_state_ship(ship, board):  # updates a state board with a ship
    for state_update_index in range(ship.length):
        if ship.orientation == 0:
            board.state[ship.coord.x][ship.coord.y - state_update_index] = 1
        elif ship.orientation == 1:
            board.state[ship.coord.x + state_update_index][ship.coord.y] = 1
        elif ship.orientation == 2:
            board.state[ship.coord.x][ship.coord.y + state_update_index] = 1
        elif ship.orientation == 3:
            board.state[ship.coord.x - state_update_index][ship.coord.y] = 1


init()  # initiate Colorama for colorful text

# define dictionaries
if player_board.width > player_board.height:
    for number in range(player_board.width):
        number_to_letter[number] = ascii_lowercase[number]
        letter_to_number[ascii_lowercase[number]] = number
else:
    for number in range(player_board.height):
        number_to_letter[number] = ascii_lowercase[number]
        letter_to_number[ascii_lowercase[number]] = number

# insert blank character into every cell of board.info and 0 into every cell of board.state
for board_x in range(player_board.width):
    player_board.info.append([])
    player_board.state.append([])
    for _ in range(player_board.height):
        player_board.info[board_x].append("")
        player_board.state[board_x].append(0)

# generate random ships, store them in ships array, and mark them on the state board
ships.append(generate_ship_random(3))
update_state_ship(ships[-1], player_board)
ships.append(generate_ship_random(4))
update_state_ship(ships[-1], player_board)
ships.append(generate_ship_random(5))
update_state_ship(ships[-1], player_board)

for ship_index in ships:
    total_hits += ship_index.length

print(
    "welcome to battleship!\nthe board is a {board_width} x {board_height} grid.\nthere are {number} ships that have a "
    "combined length of {ship_lengths} units.\nyou will get {turns} guesses to find the ship.\ngood "
    "luck!".format(number=number_ships, ship_lengths=total_hits, board_width=player_board.width,
                   board_height=player_board.height,
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
                    if player_board.info[guess.x][
                        guess.y] == "":  # check if the player hasn't already guessed that spot
                        player_board.info[guess.x][guess.y] = Fore.RED + "\u2327" + Fore.RESET  # mark hit
                        current_ship.damage += 1
                        number_hits += 1
                        print_board()
                        print(Fore.RED + "hit!\nyou hit one of my ships at " + number_to_letter[guess.y] + str(
                            guess.x + 1) + "." + Fore.RESET)
                        if current_ship.damage == current_ship.length:
                            print(Fore.GREEN + "you sunk my ship! it was {length} units long.".format(
                                length=current_ship.length) + Fore.RESET)
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
                if guess.x not in range(len(player_board.info)) or guess.y not in range(
                        len(player_board.info[0])):  # not on board
                    print("you missed the ocean!")
                elif player_board.info[guess.x][guess.y] in ("-", Fore.RED + "X" + Fore.RESET):  # already guessed
                    print("you already guessed that location!")
                else:  # on board but not guessed yet
                    print("you missed my battleship!")
                    player_board.info[guess.x][guess.y] = "-"
                print_board()
print("you have ran out of turns. the game is over!")
for ship_index in ships:
    for i in range(ship_index.length):
        if ship_index.orientation == 0:
            if player_board.info[ship_index.coord.x][ship_index.coord.y - i] == "O":
                player_board.info[ship_index.coord.x][ship_index.coord.y - i] = Fore.GREEN + "X" + Fore.RESET
        if ship_index.orientation == 1:
            if player_board.info[ship_index.coord.x + i][ship_index.coord.y] == "O":
                player_board.info[ship_index.coord.x + i][ship_index.coord.y] = Fore.GREEN + "X" + Fore.RESET
        if ship_index.orientation == 2:
            if player_board.info[ship_index.coord.x][ship_index.coord.y + i] == "O":
                player_board.info[ship_index.coord.x][ship_index.coord.y + i] = Fore.GREEN + "X" + Fore.RESET
        if ship_index.orientation == 3:
            if player_board.info[ship_index.coord.x - i][ship_index.coord.y] == "O":
                player_board.info[ship_index.coord.x - i][ship_index.coord.y] = Fore.GREEN + "X" + Fore.RESET
print_board()
print("ship locations are highlighted in green x.")
