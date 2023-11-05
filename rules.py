def print_rules():
    """
    This prints 5 basic rules of the game to the screen. The game presented
    here is a simple version of blackjack and so it was renamed to twenty-one.
    """

    print("Rules for playing the game:\n")
    print(
        "RULE 1: Have a hand that totals higher than the dealer's, but is"
        + "not > 21\n"
    )
    print(
        "RULE 2: Number cards are worth face value, colored cards"
        + "(i.e. J, Q, K) are 10 and an ace can be 1 or 11\n"
    )
    print(
        "RULE 3: Hit means you take another card, stand means you keep your"
        + "current hand\n"
    )
    print(
        "RULE 4: If player has > 21, they bust and lose. If the dealer"
        + "has > 21, they also bust and the player wins\n"
    )
    print(
        "RULE 5: The dealer must hit if they are < 17, unless the player"
        + "decided to stand and the dealer already has > the player. The"
        + "dealer wins in this instance\n"
    )
    print(
        "Note: The game here is the basic version of blackjack. It is good"
        + "for beginners to learn the core game. This is why it was renamed"
        + "to Twenty-One. Enjoy!\n"
    )
