import gspread
from google.oauth2.service_account import Credentials

# Credit: Scope code taken from code institute love sandwiches project
# These settings are needed to access twenty_one game data
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Credit: Code altered from code institute love sandwiches project, to get twenty_one spreadsheet
# These settings are needed to access twenty_one game data
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('twenty_one')

game_data = SHEET.worksheet('game_data')

data = game_data.get_all_values()

print(data)
