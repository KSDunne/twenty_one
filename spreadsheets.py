import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

__CREDS = Credentials.from_service_account_file("creds.json")
__SCOPED_CREDS = __CREDS.with_scopes(SCOPE)
__GSPREAD_CLIENT = gspread.authorize(__SCOPED_CREDS)
__SHEET = __GSPREAD_CLIENT.open("twenty_one")


# Credit: Code altered from code institute love sandwiches project, to get twenty_one spreadsheet
def worksheet():
    try:
        return __SHEET.worksheet("user_data")
    except:
        return None
