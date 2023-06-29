#
# Simple console-based flashcard utility
#
# The text for each flashcard is stored in a standard text file where
# each line contains the text for a single flashcard. Blank lines and
# lines that start with `#` are ignored. Default flashcard filename
# is `flashcards.txt`. To specify a different file, use the
# -f, --flashcard command-line argument.
#
# A new card is shown automatically every five seconds by default.
# Change the wait time with the -w, --wait command-line argument.
#
# Examples:
#   python flashcards.py
#   python flashcards.py -f practice_questions.txt
#   python flashcards.py -w 10
#   python flashcards.py -f exam.txt -w 1.5
#
# To terminate showing cards, hit <Esc> or 'q'.
#
# Required packages:
#   keyboard  # pip install keyboard

# Imports
import argparse
import keyboard
import random
import time

# Constants
VERSION = 'v1.00'

# Global variables
flashcards = []  # list of strings
stop_flashcards = False


def load_flashcards(flashcard_file):
    """Read flashcard text from a file

    :param flashcard_file: Filename that contains the text for all flashcards
    :return: True if success, else False

    The text for each flashcard is contained on a single line in the `flashcard_file`. Comments lines start with '#'.

    Sample `flashcard_file`:

    Name the capital of North Dakota
    What is the sum of 4 + 3
    # Comments are ignored
    # What is the square root of pi
    etc.

    """

    global flashcards

    try:
        with open(flashcard_file) as f:
            flashcards = f.read().splitlines()
    except OSError as e:
        print(e)
        return False

    # Remove comments and blank lines
    flashcards = [card for card in flashcards if card and card[0] != '#']
    return True


def quit_flashcards():
    """Stop showing flashcards."""
    global stop_flashcards
    stop_flashcards = True


def show_flashcards(wait):
    """Cycle randomly through flashcards.

    To terminate, hit <Esc> or 'q'.

    :param wait: Seconds until next flashcard
    """

    global flashcards, stop_flashcards

    # Show flashcards until <Esc> or 'q' is pressed
    keyboard.add_hotkey('Esc', lambda: quit_flashcards())
    keyboard.add_hotkey('q', lambda: quit_flashcards())

    random.seed()
    last_card = None  # Do not immediately repeat last card
    while not stop_flashcards:
        card = random.choice(flashcards)
        while card == last_card:
            card = random.choice(flashcards)
        print(card)
        last_card = card
        time.sleep(wait)


def main():
    # Splash screen
    print('===================')
    print(f'Flashcards    {VERSION}')
    print('===================\n')

    # Process command-line arguments
    arg_parser = argparse.ArgumentParser(description='Console-based flashcard utility')
    arg_parser.add_argument('-f', '--flashcards', dest='flashcards', metavar='flashcards', default='flashcards.txt',
                            help='flashcard file')
    arg_parser.add_argument('-w', '--wait', dest='wait', metavar='wait', default=5,
                            help='seconds between flashcards')
    args = arg_parser.parse_args()
    flashcard_file = args.flashcards
    wait = args.wait

    if not load_flashcards(flashcard_file):
        exit(1)

    # Show flashcards
    show_flashcards(wait)


if __name__ == '__main__':
    main()
