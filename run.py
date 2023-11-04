import messages
import random
import sys
from os import system, name
from colorama import Fore  # color styling
from spreadsheets import worksheet
from rules import print_rules


# Credit: https://github.com/luizsmania/blackjack/blob/main/run.py#L49C1-L59C28
def clear():
    """
    Here is a function for clearing the terminal. This function is good for user experience
    during gameplay, as the terminal backlog can look confusing.
    """
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux
    else:
        _ = system("clear")


def shuffle_cards():
    """
    This is a function to shuffle the deck of cards. Here we use a set
    of 4 Unicode symbols for suits; spades, hearts, diamonds and clubs.
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
    """
    Here is a function that deals a card to the player and removes
    that card from the deck. The list will change from length of 52 to 51.
    """

    card = deck.pop()
    player.append(card)
    return card


def total(hand):
    """
    This function computes the numerical total of a hand. It is used at
    multiple different times to calculate the total for the player and the dealer.
    """

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


def increment_wins(user_data, user_cell):
    """
    This function increments the wins column for the user in google sheets.
    Error handling was used here, so if the google sheet call fails, the game doesn't break.
    """
    try:
        user_data.update_cell(
            user_cell.row,
            user_cell.col + 1,
            int(user_data.cell(user_cell.row, user_cell.col + 1).value) + 1,
        )
        user_data.sort((user_cell.col + 1, "des"))
    except:
        return


def increment_losses(user_data, user_cell):
    """
    This function increments the losses column for the user in google sheets.
    Error handling was used here, so if the google sheet call fails, the game doesn't break.
    """
    try:
        user_data.update_cell(
            user_cell.row,
            user_cell.col + 2,
            int(user_data.cell(user_cell.row, user_cell.col + 2).value) + 1,
        )
    except:
        return


def compare_hands(house, player, user_data, username, user_cell):
    """
    This is a comparison function that looks at the numerical value of the players hand and the dealers hand
    and determines a winner.
    """
    house_total, player_total = total(house), total(player)

    if house_total > player_total:
        messages.notification(messages.LOSE_MESSAGE + username)
        increment_losses(user_data, user_cell)
    elif house_total < player_total:
        messages.notification(messages.WIN_MESSAGE + username)
        increment_wins(user_data, user_cell)
    elif house_total == 21 and 2 == len(house) < len(player):
        messages.notification(messages.LOSE_MESSAGE + username)
        increment_losses(user_data, user_cell)
    elif player_total == 21 and 2 == len(player) < len(house):
        messages.notification(messages.WIN_MESSAGE + username)
        increment_wins(user_data, user_cell)
    else:
        messages.notification(messages.TIE_MESSAGE + username)


def twenty_one(user_data, username, user_cell):
    """
    The twenty one function simulates a game of blackjack. Here is where all of the core game functions
    are called appropriately.
    """
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

    answer = input(messages.DEFAULT_MESSAGE)
    # 's' or 'S' skips player turn and goes to house play
    while answer not in {"", "h", "hit", "s", "S", "r", "R"}:
        print("Not a valid input\n")
        answer = input(messages.DEFAULT_MESSAGE)
    while answer in {"", "h", "hit", "s", "S", "r", "R"}:
        if answer in {"r", "R"}:
            print_rules()
        elif answer in {"s", "S"}:
            break
        else:
            card = deal_cards(deck, player)
            print("You got {:<7}".format(card))
            if total(player) > 21:  # you bust
                messages.notification(messages.PLAYER_BUST_MESSAGE + username)
                increment_losses(user_data, user_cell)
                return
        answer = input(messages.DEFAULT_MESSAGE)

    # House must play only if house total is less than or equal to player total
    if total(house) <= total(player):
        while total(house) < 17:  # House must hit until > 16
            card = deal_cards(deck, house)
            print("House got {:>7}".format(card))
            if total(house) > 21:  # House bust
                messages.notification(messages.HOUSE_BUST_MESSAGE + username)
                increment_wins(user_data, user_cell)
                return
    # Both hands are now done, see who wins
    compare_hands(house, player, user_data, username, user_cell)
    return


def main_menu(user_data, username, user_cell):
    """
    Here is the main menu function. It shows the user a list of options to navigate the game.
    The options shown are: (R)ules, (N)ew game, (L)eaderboard, and (Q)uit.
    """
    answer = input(messages.MAIN_MENU_MESSAGE)
    while answer not in {"q", "Q"}:
        if answer in {"r", "R"}:
            print_rules()
        elif answer in {"l", "L"}:
            show_scoreboard(user_data)
        elif answer in {"n", "N"}:
            clear()
            twenty_one(user_data, username, user_cell)
            replay = input(messages.REPLAY_MESSAGE)
            if replay in {"n", "N"}:
                answer = input(messages.MAIN_MENU_MESSAGE)
                if answer in {"r", "R"}:
                    print_rules()
                if answer in {"l", "L"}:
                    show_scoreboard(user_data)
                if answer in {"q", "Q"}:
                    messages.notification(messages.GOODBYE_MESSAGE + username)
                if answer in {"n", "N"}:
                    clear()
                    twenty_one(user_data, username, user_cell)
                    replay = input(messages.REPLAY_MESSAGE)
            while replay not in {"y", "Y", "n", "N"}:
                print("Not a valid input\n")
                replay = input(messages.REPLAY_MESSAGE)
            while replay in {"y", "Y"}:
                clear()
                twenty_one(user_data, username, user_cell)
                replay = input(messages.REPLAY_MESSAGE)
        else:
            print("Not a valid input\n")
        answer = input(messages.MAIN_MENU_MESSAGE)
    messages.notification(messages.GOODBYE_MESSAGE + username)


# Credit: https://github.com/adrianskelton/project3/blob/main/run.py#L138
def show_scoreboard(user_data):
    """
    Function to show the scoreboard. This is called in the main menu
    when selected by the user.
    """
    user_data = worksheet()
    if user_data is not None:
        scoreboard_players = user_data.col_values(1)[1:11]
        scoreboard_scores = user_data.col_values(2)[1:11]
        print("TOP 10 SCORES - TWENTY-ONE\n")
        for player, score in zip(scoreboard_players, scoreboard_scores):
            print("PLAYER: {} || POINTS: {} ||".format(player, score))
        input(Fore.BLUE + "Press Enter to continue...\033[39m")
    else:
        print("Google sheets data unavailable\n")
        input(Fore.BLUE + "Press Enter to continue...\033[39m")


def personalize(user_data):
    """
    Here is a function that takes the user name as an input. It can then be used in the
    win message, lose message, bust message and goodbye messages for personalization.
    """
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

                return username, user_cell
            except:
                return None, None


# Credit: https://stackoverflow.com/questions/37340049/how-do-i-print-colored-output-to-the-terminal-in-python
# Credit: https://github.com/pwaller/pyfiglet/blob/main/pyfiglet/__init__.py#L53
def main():
    """
    Main function that calls all functions in order.
    Setting the terminal text color to white before calling other methods.
    """
    sys.stdout.write("\033[0;97m")
    user_data = worksheet()
    messages.notification(messages.WELCOME_MESSAGE)
    username, user_cell = personalize(user_data)
    main_menu(user_data, username, user_cell)


if __name__ == "__main__":
    main()
