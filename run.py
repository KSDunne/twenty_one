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
    # we will use a set of 4 Unicode symbols for suits; spades, hearts, diamonds and clubs

    suits = {"\u2660", "\u2661", "\u2662", "\u2663"}
    ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"}
    deck = []

    # create deck of 52 cards using 2 nested for loops

    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)

    random.shuffle(deck)

    return deck

my_deck = shuffle_cards()
print(my_deck)
