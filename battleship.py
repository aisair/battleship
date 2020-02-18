from prettytable import PrettyTable
from colorama import init, Fore
from string import ascii_uppercase, ascii_lowercase
from random import randint
import re


class Coordinate:
    def __init__(self):
        self.x = 0
        self.y = 0


class Ship:
    def __init__(self, length):
        self.coord = Coordinate()
        self.orientation = 0
        self.length = length


class Board:
    def __init__(self):
        self.info = []
        self.state = []

    width = 10
    height = 10


# game vars
turn = 0
number_hits = 0
total_hits = 0
comp_hits = 0
total_comp_hits = 0
number_ships_computer = 3
number_ships_player = 3
# board vars
player_board = Board()  # player attacks from player_board.info, player sets ships on player_board.state
computer_board = Board()  # computer attacks from computer_board.info, computer sets ships on computer_board.state
# ship vars
computer_ships = []
computer_ships.append(Ship(3))
computer_ships.append(Ship(4))
computer_ships.append(Ship(5))
player_ships = []
# dictionaries: currently empty but get filled during game board initiation
letter_to_number = {}
number_to_letter = {}


def print_state_board(board):
    game_board = PrettyTable()
    if board == player_board:
        game_board.title = "your ships"
    column_labels = []
    for char in ascii_uppercase[:10]:
        column_labels.append(char)
    game_board.add_column("", column_labels)
    for x_index in range(board.width):
        temp_board = []
        for _ in board.state[x_index]:
            if _ == 1:
                temp_board.append("\u2588")
            elif _ == 2:
                temp_board.append(Fore.RED + "\u2327" + Fore.RESET)
            elif _ == 3:
                temp_board.append("-")
            else:
                temp_board.append("")
        game_board.add_column(str(x_index + 1), temp_board)
    print(game_board)


def print_board(board):
    game_board = PrettyTable()
    game_board.title = "battleship game board"
    column_labels = []
    for char in ascii_uppercase[:10]:
        column_labels.append(char)
    game_board.add_column("", column_labels)
    for x_index in range(board.width):
        game_board.add_column(str(x_index + 1), board.info[x_index])
    print(game_board)


def place_ship_random(index):
    orientation = 0
    size = randint(1, 5)
    random_coord = Coordinate()
    valid = 0
    while valid == 0:
        valid = 1
        random_coord.x = randint(0, computer_board.width - 1)
        random_coord.y = randint(0, computer_board.height - 1)
        if size > 1:
            # check if ships are inside the board
            if randint(0, 1) == 1:  # vertical
                if (random_coord.y - size) > -2:
                    for size_check_index in range(size - 1):
                        if computer_board.state[random_coord.x][random_coord.y - size_check_index] == 1:
                            valid = 0
                    if valid == 1:
                        for state_update_index in range(size - 1):
                            computer_board.state[random_coord.x][random_coord.y - state_update_index] = 1
                    orientation = 0
                elif (random_coord.y + size) < computer_board.height:
                    for size_check_index in range(size - 1):
                        if computer_board.state[random_coord.x][random_coord.y + size_check_index] == 1:
                            valid = 0
                    if valid == 1:
                        for state_update_index in range(size - 1):
                            computer_board.state[random_coord.x][random_coord.y + state_update_index] = 1
                    orientation = 2
            else:  # horizontal
                if (random_coord.x + size) < computer_board.width:
                    for size_check_index in range(size - 1):
                        if computer_board.state[random_coord.x + size_check_index][random_coord.y] == 1:
                            valid = 0
                    if valid == 1:
                        for state_update_index in range(size - 1):
                            computer_board.state[random_coord.x + state_update_index][random_coord.y] = 1
                    orientation = 1
                elif (random_coord.x - size) > -2:
                    for size_check_index in range(size - 1):
                        if computer_board.state[random_coord.x - size_check_index][random_coord.y] == 1:
                            valid = 0
                    if valid == 1:
                        for state_update_index in range(size - 1):
                            computer_board.state[random_coord.x - state_update_index][random_coord.y] = 1
                    orientation = 3
    computer_ships[index].coord = random_coord
    computer_ships[index].orientation = orientation


def player_place():
    orientation_dictionary = {
        "up": 0,
        "right": 1,
        "down": 2,
        "left": 3
    }
    place_coord = Coordinate()
    place_length = 0
    place_orientation = 0
    placement_valid = 1
    while placement_valid != 0:
        valid_input = 0
        while valid_input == 0:
            valid_input = 1
            place_input_string = input("where would you like one end of your ship to be? ")
            if len(place_input_string) < 2 or place_input_string[0] not in letter_to_number or re.search('[^0-9]a1',
                                                                                                         place_input_string[
                                                                                                         1:]) or int(
                    place_input_string[1:]) - 1 not in number_to_letter:
                print("invalid location!")
                valid_input = 0
            else:
                place_coord.x = int(place_input_string[1:]) - 1
                place_coord.y = letter_to_number.get(place_input_string[0].lower())
        valid_input = 0
        while valid_input == 0:
            valid_input = 1
            place_length_string = input("how long would you like your ship to be? ")
            if re.search('[^0-9]', place_length_string):
                print("invalid length!")
                valid_input = 0
            else:
                place_length = int(place_length_string)
        valid_input = 0
        while valid_input == 0:
            valid_input = 1
            place_orientation_string = input(
                "what direction should your ship extend from the original coordinate? (up, down, left, right): ")
            if place_orientation_string.lower() not in orientation_dictionary:
                print("invalid orientation!")
                valid_input = 0
            else:
                place_orientation = orientation_dictionary[place_orientation_string]
        placement_valid = 0  # 0 is valid, 1 is invalid (outside board), 2 is invalid (overlapping ships)
        if place_length > 1:
            if place_orientation == 0:
                if (place_coord.y - place_length) > -2:
                    for player_length_check_index in range(place_length - 1):
                        if player_board.state[place_coord.x][place_coord.y - player_length_check_index] == 1:
                            placement_valid = 2
                else:
                    placement_valid = 1
            elif place_orientation == 1:
                if (place_coord.x + place_length) < player_board.width:
                    for length_check_index in range(place_length - 1):
                        if player_board.state[place_coord.x + length_check_index][place_coord.y] == 1:
                            placement_valid = 2
                else:
                    placement_valid = 1
            elif place_orientation == 2:
                if (place_coord.y + place_length) < player_board.height:
                    for player_length_check_index in range(place_length - 1):
                        if player_board.state[place_coord.x][place_coord.y + player_length_check_index] == 1:
                            placement_valid = 2
                else:
                    placement_valid = 1
            elif place_orientation == 3:
                if (place_coord.x - place_length) > -2:
                    for length_check_index in range(place_length - 1):
                        if player_board.state[place_coord.x - length_check_index][place_coord.y] == 1:
                            placement_valid = 2
                else:
                    placement_valid = 1
        if placement_valid == 0:
            player_ships.append(Ship(place_length))
            player_ships[-1].coord = place_coord
            player_ships[-1].orientation = place_orientation
            for state_update_index in range(place_length):
                if place_orientation == 0:
                    player_board.state[place_coord.x][place_coord.y - state_update_index] = 1
                elif place_orientation == 1:
                    player_board.state[place_coord.x + state_update_index][place_coord.y] = 1
                elif place_orientation == 2:
                    player_board.state[place_coord.x][place_coord.y + state_update_index] = 1
                elif place_orientation == 3:
                    player_board.state[place_coord.x - state_update_index][place_coord.y] = 1
            print("your ship is valid and has been placed!")
        elif placement_valid == 1:
            print("your ship is partially outside the board!")
        elif placement_valid == 2:
            print("your ship is overlapping another one of your ships!")


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
# insert "O" into every cell of board.info and 0 into every cell of board.state
for board_x in range(player_board.width):
    player_board.info.append([])
    player_board.state.append([])
    computer_board.info.append([])
    computer_board.state.append([])
    for _ in range(player_board.height):
        player_board.info[board_x].append("")
        player_board.state[board_x].append(0)
        computer_board.info[board_x].append("")
        computer_board.state[board_x].append(0)
place_ship_random(0)
place_ship_random(1)
place_ship_random(2)
for ship_index in computer_ships:
    total_hits += ship_index.length
print(
    "    __          __  __  __          __    _\n   / /_  ____ _/ /_/ /_/ /__  _____/ /_  (_)___ \n  / __ \/ __ `/ __/ __/ / _ \/ ___/ __ \/ / __ \n / /_/ / /_/ / /_/ /_/ /  __(__  ) / / / / /_/ /\n/_.___/\__,_/\__/\__/_/\___/____/_/ /_/_/ .___/ \n                                       /_/      ")
print(
    "welcome to battleship (against the computer)! you get to choose where to place your ships in this one.\nboth of the boards will be a {width} x {height} grid\nthe computer will have {number_computer} ships that have a combined length of {combined_length} unites.\nyou will also get to place {number_player} ships, so don't worry!\nthere's no turn limit in this one, whoever destroys the other first wins! good luck!~".format(
        width=player_board.width, height=player_board.height, number_computer=number_ships_computer,
        combined_length=total_hits, number_player=number_ships_player))

print_board(player_board)  # print the game board

print("you're able to place {number_player} ships!".format(number_player=number_ships_player))
for _ in range(number_ships_player):
    print("ship {number}: ".format(number=_ + 1))
    player_place()
for x_index in range(player_board.width):
    for y_index in range(player_board.height):
        if player_board.state[x_index][y_index] == 1:
            total_comp_hits += 1
print_state_board(player_board)
print("those are your ships!")

while comp_hits != total_comp_hits:
    guess = Coordinate()
    guess.x = None
    guess.y = None
    while guess.x is None and guess.y is None:  # loop while user's guess is invalid
        guess_string = input("input guess: (ex. A1) ")
        if len(guess_string) < 2 or guess_string[0] not in letter_to_number or re.search('[a-zA-Z]',
                                                                                         guess_string[1:]) or int(
            guess_string[1:]) - 1 not in number_to_letter:
            print("invalid input!")
        else:
            guess.x = int(guess_string[1:]) - 1
            guess.y = letter_to_number.get(guess_string[0].lower())
            hit = 0
            for current_ship in computer_ships:
                if (current_ship.orientation == 0 and guess.x == current_ship.coord.x and guess.y in range(
                        current_ship.coord.y - (current_ship.length - 1), current_ship.coord.y + 1)) or (
                        current_ship.orientation == 2 and guess.x == current_ship.coord.x and guess.y in range(
                    current_ship.coord.y, current_ship.coord.y + computer_ships[0].length)) or (
                        current_ship.orientation == 3 and guess.x in range(
                    current_ship.coord.x - (current_ship.length - 1),
                    current_ship.coord.x + 1) and guess.y == current_ship.coord.y) or (
                        current_ship.orientation == 1 and guess.x in range(current_ship.coord.x,
                                                                           current_ship.coord.x + current_ship.length) and guess.y ==
                        computer_ships[0].coord.y):  # check if player hit a ship
                    hit = 1
                    if player_board.info[guess.x][
                        guess.y] == "":  # check if the player hasn't already guessed that spot
                        player_board.info[guess.x][guess.y] = Fore.RED + "\u2327" + Fore.RESET  # mark hit
                        number_hits += 1
                        print_board(player_board)
                        print(Fore.RED + "hit!\nyou hit one of my ships at " + number_to_letter[guess.y] + str(
                            guess.x + 1) + "." + Fore.RESET)
                    else:  # if the player already guessed that spot
                        print_board(player_board)
                        print("you seem to have hit the same spot on a ship.\nno damage taken.")
                    if number_hits == total_hits:  # check for game end
                        secret_string = ""
                        if turn + 1 < total_hits:
                            secret_string = " how did you do it?"
                        print(
                            Fore.GREEN + "all ships sunk!\ncongratulations, you won the game in {turns} turns!{secret}".format(
                                turns=turn + 1, secret=secret_string) + Fore.RESET)
                        exit()
            if hit == 0:
                if guess.x not in range(player_board.width) or guess.y not in range(
                        player_board.height):  # guess is not on board
                    print("you missed the ocean!")
                elif player_board.info[guess.x][guess.y] in ("-", Fore.RED + "X" + Fore.RESET):  # already guessed
                    print("you already guessed that location!")
                else:  # on board but not guessed yet
                    print("you missed my battleship!")
                    player_board.info[guess.x][guess.y] = "-"
                print_board(player_board)
    comp_guess = Coordinate()
    comp_guess.x = randint(0, player_board.width - 1)
    comp_guess.y = randint(0, player_board.height - 1)
    if player_board.state[comp_guess.x][comp_guess.y] == 1:
        player_board.state[comp_guess.x][comp_guess.y] = 2
        comp_hits += 1
    elif player_board.state[comp_guess.x][comp_guess.y] == 0:
        player_board.state[comp_guess.x][comp_guess.y] = 3
    print("the computer guessed and got this:")
    print_state_board(player_board)
print(Fore.RED + "game over!\nthe computer sunk all of your ships!" + Fore.RESET)
for x_index in range(computer_board.width):
    for y_index in range(computer_board.height):
        if computer_board.state[x_index][y_index] == 1:
            if player_board.info[x_index][y_index] == "":
                player_board.info[x_index][y_index] = Fore.GREEN + "\u2588" + Fore.RESET
print_board(player_board)
print("computer ship locations are highlighted in green.")
