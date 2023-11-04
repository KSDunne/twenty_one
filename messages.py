import pyfiglet

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


# Credit: https://github.com/kpsdev1/blackjack/blob/main/run.py
def notification(text):
    """
    This is a notification function for gameplay user feedback. pyfiglet takes ASCII text
    and renders it in ASCII art fonts. The font used here is called big. The art is displayed on
    the start screen. It is also displayed on the win, lose and goodbye screens.
    """
    print(pyfiglet.figlet_format(text, font="big"))
