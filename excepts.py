class GameOver(Exception):
    message = "Player lost"

class OutOfCards(GameOver):
    message = "Player is out of cards"


