class GameOver(Exception):
    message = "Player lost"

class OutOfCards(GameOver):
    message = "Player is out of cards"

class OutOfAP(Exception):
    message = "Not enough AP"
