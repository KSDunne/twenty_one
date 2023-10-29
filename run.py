import gspread
from google.oauth2.service_account import Credentials
import random
import pyfiglet
import sys

# Credit: Scope code taken from code institute love sandwiches project
# These settings are needed to access twenty_one game data
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Credit: Code altered from code institute love sandwiches project, to get twenty_one spreadsheet
# These settings are needed to access twenty_one game data
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("twenty_one")

WELCOME_MESSAGE = "WELCOME TO BLACKJACK"
DEFAULT_MESSAGE = "(H)it or (S)tand? (ENTER means hit):\n"
WIN_MESSAGE = "You win, "
LOSE_MESSAGE = "You lose, "
TIE_MESSAGE = "A tie between the house and "
PLAYER_BUST_MESSAGE = "You bust, sorry "
HOUSE_BUST_MESSAGE = "House bust, you win "
REPLAY_MESSAGE = "Play another game? (Y)es or (N)o\n"
GOODBYE_MESSAGE = "Goodbye, "
MAIN_MENU_MESSAGE = "(R)ules\n(N)ew game\n(Q)uit\n\nUser input: "

game_data = SHEET.worksheet("game_data")

data = game_data.get_all_values()

# print(data)

username = None


# Credit: https://github.com/kpsdev1/blackjack/blob/main/run.py
def notification(text):
    """
    This is a function for the gameplay user feedback.
    """
    print(pyfiglet.figlet_format(text, font="big"), flush=True)


def shuffle_cards():
    # Here we use a set of 4 Unicode symbols for suits; spades, hearts, diamonds and clubs

    suits = ["\u2660", "\u2661", "\u2662", "\u2663"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = []

    # Create a deck of 52 cards using 2 nested for loops

    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)

    random.shuffle(deck)

    return deck


my_deck = shuffle_cards()
# print(my_deck)


def deal_cards(deck, player):
    # Deal card to the player and remove that card from the deck. The list will change from length of 52 to 51

    card = deck.pop()
    player.append(card)
    return card


def total(hand):
    # Compute the total of hand

    values = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "1": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
        "A": 11,
    }

    result = 0
    num_aces = 0
    for card in hand:
        result += values[card[0]]
        if card[0] == "A":
            num_aces += 1

    while result > 21 and num_aces > 0:
        result -= 10
        num_aces -= 1

    return result


def rules():
    print("Rules for playing the game:\n")
    print("Rule1:\n")
    print("...\n")
    print("RuleN:\n")


def compare_hands(house, player):
    # Determines winner

    house_total, player_total = total(house), total(player)

    if house_total > player_total:
        notification(LOSE_MESSAGE + username)
    elif house_total < player_total:
        notification(WIN_MESSAGE + username)
    elif house_total == 21 and 2 == len(house) < len(player):
        notification(LOSE_MESSAGE + username)
    elif player_total == 21 and 2 == len(player) < len(house):
        notification(WIN_MESSAGE + username)
    else:
        notification(TIE_MESSAGE + username)


def twenty_one():
    # Simulates a game of blackjack

    deck = shuffle_cards()
    house = []
    player = []

    for i in range(2):
        deal_cards(deck, player)
        deal_cards(deck, house)

    # Print hands

    print("House: {:>7}{:>7}".format(house[0], house[1]))
    print("You: {:>7}{:>7}".format(player[0], player[1]))

    # Give cards to user as requested

    answer = input(DEFAULT_MESSAGE)
    # 's' or 'S' skips player turn and goes to house play
    while answer in {"", "h", "hit", "s", "S", "r", "R"}:
        if answer in {"r", "R"}:
            rules()
        elif answer in {"s", "S"}:
            break
        else:
            card = deal_cards(deck, player)
            print("You got {:<7}".format(card))
            if total(player) > 21:  # you bust
                notification(PLAYER_BUST_MESSAGE + username)
                return
        answer = input(DEFAULT_MESSAGE)

    # House must play only if house total is less than or equal to player total
    if total(house) <= total(player):
        while total(house) < 17:  # House must hit until > 16
            card = deal_cards(deck, house)
            print("House got {:>7}".format(card))
            if total(house) > 21:  # House bust
                notification(HOUSE_BUST_MESSAGE + username)
                return

    # Both hands are now done, see who wins
    compare_hands(house, player)
    return


def main_menu():
    answer = input(MAIN_MENU_MESSAGE)
    while answer not in {"q", "Q"}:
        if answer in {"r", "R"}:
            rules()
        elif answer in {"n", "N"}:
            twenty_one()
            replay = input(REPLAY_MESSAGE)
            while replay in {"y", "Y"}:
                twenty_one()
                replay = input(REPLAY_MESSAGE)
        else:
            print("Not a valid input\n")
        answer = input(MAIN_MENU_MESSAGE)
    notification(GOODBYE_MESSAGE + username)


# This name validation can be extended further
def personalize():
    global username
    username = input("Your name: ")
    while True:
        if any(char.isdigit() for char in username):
            username = input(
                "Input doesn't seem to look like a name, please enter your name again: "
            )
        else:
            break


# Credit: https://stackoverflow.com/questions/37340049/how-do-i-print-colored-output-to-the-terminal-in-python
def main():
    """
    Main function that calls all functions in order.
    Setting the terminal text color to green before calling other methods.
    """
    sys.stdout.write("\033[0;32m")
    notification(WELCOME_MESSAGE)
    personalize()
    main_menu()


main()
