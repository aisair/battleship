from prettytable import PrettyTable
from colorama import init, Fore
from string import ascii_uppercase
import random

init()  # initiate colorama for colorful text


class Coordinate:
    x = 0
    y = 0


class Ship:
    coord = Coordinate()
    orientation = 0
    length = 0


# game vars
number_turns = 12
number_hits = 0
# board vars
game_board = PrettyTable()
board_rows = 5
board_columns = 5
board_info = []
# ship vars
ship = Ship()
ship.length = 3
# dictionaries
letter_to_number = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
}
number_to_letter = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
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
    i = 0
    while i < board_rows:
        add = [ascii_uppercase[i]]
        j = 0
        while j < board_columns:
            add.append(board_info[i][j])
            j += 1
        game_board.add_row(add)
        i += 1
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


print("welcome to battleship! there is one ship that is", ship.length, "unit(s) long.\nthe board is a 5 x 5 grid. "
                                                                       "you will get", number_turns, "guesses to "
                                                                                                     "find the "
                                                                                                     "ship. good "
                                                                                                     "luck!")

print_board(1)  # initiating game board
place_ship_random(ship.length)

print(Fore.RED + "debug:\nship location:\nhuman co-ord:", number_to_letter[ship.coord.y], ship.coord.x + 1, "\nlength:",
      ship.length, "\norientation:", ship.orientation, Fore.RESET)  # to help debugging, could also use pycharm debugger
for current_turn in range(number_turns):
    guess = Coordinate()
    print("you are on turn", current_turn + 1, "of", number_turns)
    guess_string = input("input guess: (ex. A1) ")
    if len(guess_string) != 2 or letter_to_number.get(guess_string[0].lower(), "INVALID") == "INVALID":
        print("invalid input!")
        guess.x, guess.y = -1, -1
    else:
        guess.x = int(guess_string[1]) - 1
        guess.y = letter_to_number.get(guess_string[0].lower())
    if (ship.orientation == 0 and guess.x == ship.coord.x and guess.y in range(ship.coord.y - (ship.length - 1),
                                                                               ship.coord.y + 1)) or (
            ship.orientation == 1 and guess.x in range(ship.coord.x,
                                                       ship.coord.x + ship.length) and guess.y == ship.coord.y) or (
            ship.orientation == 2 and guess.x == ship.coord.x and guess.y in range(ship.coord.y + (ship.length - 1),
                                                                                   ship.coord.y + 1)) or (
            ship.orientation == 3 and guess.x in range(ship.coord.x - (ship.length - 1),
                                                       ship.coord.x + 1) and guess.y == ship.coord.y):
        board_info[guess.y][guess.x] = Fore.RED + "X" + Fore.RESET  # mark hit
        number_hits += 1
        print_board()
        print(Fore.RED + "hit!\nyou hit my ship at " + number_to_letter[guess.y] + str(guess.x + 1) + "." + Fore.RESET)
        if number_hits == ship.length:
            print("the ship sunk!\n"
                  "congratulations, you won the game!")
            break
    else:
        if guess.y not in range(len(board_info)) or guess.x not in range(len(board_info[0])):  # not on board
            print("you missed the ocean!")
        elif board_info[guess.y][guess.x] in ("X", Fore.RED + "X" + Fore.RESET):  # already guessed
            print("you already guessed that location!")
        else:  # on board but not guessed yet
            print("you missed my battleship!")
            board_info[guess.y][guess.x] = "X"
        print_board()
        if current_turn == number_turns - 1:
            print("you have ran out of turns. the game is over!")
            i = 0
            while i < ship.length:
                if ship.orientation == 0:
                    if board_info[ship.coord.y - i][ship.coord.x] == "O":
                        board_info[ship.coord.y - i][ship.coord.x] = Fore.GREEN + "X" + Fore.RESET
                if ship.orientation == 1:
                    if board_info[ship.coord.y][ship.coord.x + i] == "O":
                        board_info[ship.coord.y][ship.coord.x + i] = Fore.GREEN + "X" + Fore.RESET
                if ship.orientation == 2:
                    if board_info[ship.coord.y + i][ship.coord.x] == "O":
                        board_info[ship.coord.y + i][ship.coord.x] = Fore.GREEN + "X" + Fore.RESET
                if ship.orientation == 3:
                    if board_info[ship.coord.y][ship.coord.x - i] == "O":
                        board_info[ship.coord.y][ship.coord.x - i] = Fore.GREEN + "X" + Fore.RESET
                i += 1
            print_board()
            print("ship locations are highlighted in green x.")
        else:
            print("you have one ship remaining. it has a length of %d." % ship.length)
