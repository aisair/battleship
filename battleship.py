# This is the in-class tutorial for a basic battle ship game. This game will have one ship, one unit long.  To get a
# C, the game will need 1 ship 3 units long. to get a B, the game should have 3 ships  of different lengths,
# randomly placed vertically or horizontally on the board. To get an A, there must be a computer playing a person
# player.

# We will import the random library to place the 1 x 1 ship randomly
import random

# We will import the time library so we can add a delay between turns
import time

# begin by creating a the game-board. For this level it will be a 5x5 units and initially will be set to show all "O"'s


# append a row of 5 "-'s"


# function to print the board



# Start the game play . If  you want to add delays, so the game plays more naturally use time.sleep(seconds)


# We need to randomly place the ship on the board.  The x-coordinate should have value between 0 and 4.
# If this were a C, B or A level project you would also have to randomly choose vertical or horizontal




# The C level will need an extra function and variable to keep track of vertical or horizontal for the 3 x 1 ship.


# For the highe level projects, you will need to make sure the ships do not go off the board, and do not overlap.

# The next 2 lines are to check where the ship is being placed. so should be removed for final game


# Let the player guess where the ship is
# for the basic game we will let the player input integers, but for the real battleship game,
# you will need to enter inputs as "C4" or "D5"
# so the this row input should be a letter in the version you build.




# Check if the guess is a hit or a miss, or not on the board.
# When you build the game make sure to let them know if they already guessed that spot.





# Your print statement should should update how many ships are remaining and how many are sunk from your set of ships.


# Convert Letters to numbers.