from exceptions import *
from cards import *
from utils import FieldUtilsMixin
import random
class OutOfCards(Exception):
    message = "Player is out of cards"

class Field(FieldUtilsMixin, object):
    def __init__(self, player):
        self.cards = [EmptyField(self) for i in range(4)]
        self.player = player
    def add(self, cardclass, position):
        self.cards[position] = cardclass(self)
    def remove(self, card):
        self.cards.remove(card)
    def attack(self, field):
        for c1, c2 in zip(self.cards, field.cards):
            c1.attack(c2)         
    def __str__(self):
        return " ".join(map(str, self.cards))

class Deck(object):
    def __init__(self):
        self.cards = self.loadcards()
    def loadcards(self):
        cards = [Card, Card, Card, DefensiveCard, CardWithEffect]
        random.shuffle(cards)
        return cards


class Player(object):
    hp = 20
    def __init__(self, name):
        self.name = name
        self.field = Field(self)
        self.deck = Deck()
        self.hand = []

    def draw(self):
        if self.deck.cards:
            self.hand.append(self.deck.cards.pop())
        else:
            raise OutOfCards

    def attack(self, player):
        self.field.attack(player.field)


#next steps

