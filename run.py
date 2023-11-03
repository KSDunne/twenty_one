import gspread
import pyfiglet
import random
import sys
from os import system, name
from google.oauth2.service_account import Credentials
from colorama import Fore  # color styling

WELCOME_MESSAGE = "WELCOME TO TWENTYONE"
DEFAULT_MESSAGE = "(H)it, (S)tand or (R)ules? (ENTER means hit):\nUser input: "
WIN_MESSAGE = "You win, "
LOSE_MESSAGE = "You lose, "
TIE_MESSAGE = "A tie between the house and "
PLAYER_BUST_MESSAGE = "You bust, sorry "
HOUSE_BUST_MESSAGE = "House bust, you win "
REPLAY_MESSAGE = "Play another game? (Y)es or (N)o\nUser input: "
GOODBYE_MESSAGE = "Goodbye, "
MAIN_MENU_MESSAGE = "(R)ules\n(N)ew game\n(L)eaderboard\n(Q)uit\n\nUser input: "

user_data = None
username = None
user_cell = None


def google_sheets():
    """
    This is a function with a try and except to make sure that
    if the google sheets call fails, the game can still be played.
    The settings here are the settings needed to access twenty_one game data.
    Scope code was taken from code institute love sandwiches project.
    """
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        # Credit: Code altered from code institute love sandwiches project, to get twenty_one spreadsheet
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
    This is a notification function for gameplay user feedback. pyfiglet takes ASCII text
    and renders it in ASCII art fonts. The font used here is called big. The art is displayed on 
    the start screen. It is also displayed on the win, lose and goodbye screens.
    """
    print(pyfiglet.figlet_format(text, font="big"))


# Credit: https://github.com/luizsmania/blackjack/blob/main/run.py#L49C1-L59C28
def clear():
    """
    Fuction for cleaning the terminal
    """
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux
    else:
        _ = system("clear")


def shuffle_cards():
    """
    This is a function to shuffle the deck of cards
    Here we use a set of 4 Unicode symbols for
    suits; spades, hearts, diamonds and clubs
    """
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
    print("RULE 1: Have a hand that totals higher than the dealer's, but is not > 21\n")
    print(
        "RULE 2: Number cards are worth face value, colored cards (i.e. J, Q, K) are 10 and an ace can be 1 or 11\n"
    )
    print(
        "RULE 3: Hit means you take another card, stand means you keep your current hand\n"
    )
    print(
        "RULE 4: If player has > 21, they bust and lose. If the dealer has > 21, they also bust and the player wins\n"
    )
    print(
        "RULE 5: The dealer must hit if they are < 17, unless the player decided to stand and the dealer already has > the player. The dealer wins in this instance\n"
    )
    print(
        "Note: The game here is the basic version of blackjack. It is good for beginners to learn the core game. This is why it was renamed to Twenty-One. Enjoy!\n"
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
        user_data.sort((user_cell.col + 1, "des"))
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
    while answer not in {"", "h", "hit", "s", "S", "r", "R"}:
        print("Not a valid input\n")
        answer = input(DEFAULT_MESSAGE)
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
        if answer in {"l", "L"}:
            show_scoreboard()
        elif answer in {"n", "N"}:
            clear()
            twenty_one()
            replay = input(REPLAY_MESSAGE)
            if replay in {"n", "N"}:
                answer = input(MAIN_MENU_MESSAGE)
                if answer in {"r", "R"}:
                    rules()
                if answer in {"l", "L"}:
                    show_scoreboard()
                if answer in {"q", "Q"}:
                    notification(GOODBYE_MESSAGE + username)
                if answer in {"n", "N"}:
                    clear()
                    twenty_one()
                    replay = input(REPLAY_MESSAGE)
            while replay not in {"y", "Y", "n", "N"}:
                print("Not a valid input\n")
                replay = input(REPLAY_MESSAGE)
            while replay in {"y", "Y"}:
                clear()
                twenty_one()
                replay = input(REPLAY_MESSAGE)
        else:
            print("Not a valid input\n")
        answer = input(MAIN_MENU_MESSAGE)
    notification(GOODBYE_MESSAGE + username)


# Credit: https://github.com/adrianskelton/project3/blob/main/run.py#L138
def show_scoreboard():
    """
    Function to show the scoreboard
    This is called in the main menu at the start when selected by the user
    """
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    try:
        CREDS = Credentials.from_service_account_file("creds.json")
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
        SHEET = GSPREAD_CLIENT.open("twenty_one")
        global user_data
        user_data = SHEET.worksheet("user_data")
        scoreboard_players = user_data.col_values(1)[1:11]
        scoreboard_scores = user_data.col_values(2)[1:11]
        print("TOP 10 SCORES - TWENTY-ONE\n")
        for player, score in zip(scoreboard_players, scoreboard_scores):
            print("PLAYER: {} || POINTS: {} ||".format(player, score))
        input(Fore.BLUE + "Press Enter to continue...\033[39m")
    except:
        return


def personalize():
    global username
    username = input(
        "Your name will be stored for game personalization, so use an alias.\n\nEnter your name: "
    )
    while True:
        if not any(char.isalpha() for char in username):
            username = input(
                "Input doesn't seem to look like a name, please enter your name again: "
            )
        else:
            # find username if already exists, otherwise add to list
            # if google sheet calls fail it won't break game functionality
            global user_cell
            global user_data
            print(
                f"\nWelcome to Twenty-One, {username}!\n\nChoose an option from the main menu:\n"
            )
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
