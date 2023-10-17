import gspread
from google.oauth2.service_account import Credentials
import random

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

game_data = SHEET.worksheet("game_data")

data = game_data.get_all_values()

print(data)


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


def compare_hands(house, player):
    # Determines winner

    house_total, player_total = total(house), total(player)

    if house_total > player_total:
        print("You lose.")
    elif house_total < player_total:
        print("You win.")
    elif house_total == 21 and 2 == len(house) < len(player):
        print("You lose")
    elif player_total == 21 and 2 == len(player) < len(house):
        print("You win.")
    else:
        print("A Tie!")


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
    print("Y o u: {:>7}{:>7}".format(player[0], player[1]))

    # Give cards to user as requested

    answer = input("hit or stand? (ENTER means hit):\n")
    while answer in {"", "h", "hit"}:
        card = deal_cards(deck, player)
        print("You got {:<7}".format(card))

        if total(player) > 21:  # you bust
            print("You bust, sorry")
            return

        answer = input("hit or stand? (ENTER means hit) :\n")

        # House must play

        while total(house) < 17:  # House must hit until > 16
            card = deal_cards(deck, house)
            print("House got {:>7}".format(card))

            if total(house) > 21:  # House bust
                print("House bust, you win.")
                return

            # Both hands are now done, see who wins
            compare_hands(house, player)
            return
