import gspread
import pyfiglet
import random
import sys
from google.oauth2.service_account import Credentials

WELCOME_MESSAGE = "WELCOME TO TWENTYONE"
DEFAULT_MESSAGE = "(H)it or (S)tand? (ENTER means hit):\nUser input: "
WIN_MESSAGE = "You win, "
LOSE_MESSAGE = "You lose, "
TIE_MESSAGE = "A tie between the house and "
PLAYER_BUST_MESSAGE = "You bust, sorry "
HOUSE_BUST_MESSAGE = "House bust, you win "
REPLAY_MESSAGE = "Play another game? (Y)es or (N)o\nUser input: "
GOODBYE_MESSAGE = "Goodbye, "
MAIN_MENU_MESSAGE = "(R)ules\n(N)ew game\n(Q)uit\n\nUser input: "

user_data = None
username = None
user_cell = None


# if google sheets calls fail, game doesn't break
def google_sheets():
    # Credit: Scope code taken from code institute love sandwiches project
    # These settings are needed to access twenty_one game data
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        # Credit: Code altered from code institute love sandwiches project, to get twenty_one spreadsheet
        # These settings are needed to access twenty_one game data
        CREDS = Credentials.from_service_account_file("creds.json")
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
        SHEET = GSPREAD_CLIENT.open("twenty_one")
        global user_data
        user_data = SHEET.worksheet("user_data")
    except:
        return


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
    print("Rule1: Have a hand that totals higher than the dealer's, but is not > 21\n")
    print(
        "Rule2: Number cards are worth face value, colored cards (i.e. J, Q and K) are 10 and an ace can be 1 or 11\n"
    )
    print(
        "Rule3: Hit means you take another card, stand means you keep your current hand\n"
    )
    print(
        "Rule4: If player has > 21, they bust and lose. If the dealer has > 21, they also bust and the player wins\n"
    )
    print(
        "Rule5: The dealer must hit if they are < 17, unless the player decided to stand and the dealer already has > the player.\nThe dealer wins in this instance\n"
    )
    print(
        "Note: The game presented here is the basic version of blackjack, therefore it is good for beginners to learn the core game.\nThis is why it was renamed to TwentyOne. Enjoy!\n"
    )


# increment the wins column for the user
# in case google sheet call fails, game doesn't break
def increment_wins():
    global user_cell
    global user_data
    try:
        user_data.update_cell(
            user_cell.row,
            user_cell.col + 1,
            int(user_data.cell(user_cell.row, user_cell.col + 1).value) + 1,
        )
    except:
        return


# increment the losses column for the user
# in case google sheet call fails, game doesn't break
def increment_losses():
    global user_cell
    global user_data
    try:
        user_data.update_cell(
            user_cell.row,
            user_cell.col + 2,
            int(user_data.cell(user_cell.row, user_cell.col + 2).value) + 1,
        )
    except:
        return


def compare_hands(house, player):
    # Determines winner

    house_total, player_total = total(house), total(player)

    if house_total > player_total:
        notification(LOSE_MESSAGE + username)
        increment_losses()
    elif house_total < player_total:
        notification(WIN_MESSAGE + username)
        increment_wins()
    elif house_total == 21 and 2 == len(house) < len(player):
        notification(LOSE_MESSAGE + username)
        increment_losses()
    elif player_total == 21 and 2 == len(player) < len(house):
        notification(WIN_MESSAGE + username)
        increment_wins()
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
                increment_losses()
                return
        answer = input(DEFAULT_MESSAGE)

    # House must play only if house total is less than or equal to player total
    if total(house) <= total(player):
        while total(house) < 17:  # House must hit until > 16
            card = deal_cards(deck, house)
            print("House got {:>7}".format(card))
            if total(house) > 21:  # House bust
                notification(HOUSE_BUST_MESSAGE + username)
                increment_wins()
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
            # find username if already exists, otherwise add to list
            # if google sheet calls fail it won't break game functionality
            global user_cell
            global user_data
            try:
                cell = user_data.find(username)
                if cell:
                    user_cell = cell
                else:
                    user_data.append_row([username, 0, 0])
                    user_cell = user_data.find(username)
            except:
                return
            break


# Credit: https://stackoverflow.com/questions/37340049/how-do-i-print-colored-output-to-the-terminal-in-python
# Credit: https://github.com/pwaller/pyfiglet/blob/main/pyfiglet/__init__.py#L53
def main():
    """
    Main function that calls all functions in order.
    Setting the terminal text color to green before calling other methods.
    """
    sys.stdout.write("\033[0;97m")
    google_sheets()
    notification(WELCOME_MESSAGE)
    personalize()
    main_menu()


main()
