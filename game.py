from excepts import *
from cards import *
from utils import FieldUtilsMixin
import random


class Board(FieldUtilsMixin, object):
    """
    Class for everything on a player's side of the board
    """
    def __init__(self, player):
        self.cards = [EmptyField(self) for i in range(4)]
        self.player = player
        self.buildings = [None] * 4

    def add(self, cardclass, position):
        if issubclass(cardclass, CreatureCard):
            if issubclass(self.cards[position].__class__, CreatureCard):
                self.player.discard_pile.append(self.cards[position].__class__)
            self.cards[position] = cardclass(self)
        elif cardclass == EmptyField:
            self.cards[position] = cardclass(self)
        elif issubclass(cardclass, SpellCard):
            cardclass(self)
        elif issubclass(cardclass, BuildingCard):
            if issubclass(self.buildings[position].__class__, BuildingCard):
                self.player.discard_pile.append(self.buildings[position].__class__)
            self.buildings[position] = cardclass(self)

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
        cards = [CreatureCard, DefensiveCard, CardWithEffect,
                 DrawCardsCard, CelestialCastle]
        cards = cards * 3
        random.shuffle(cards)
        return cards



class Player(object):
    hp = 20
    def __init__(self, name):
        self.name = name
        self.board = Board(self)
        self.deck = Deck()
        self.hand = []
        self.discard_pile = []

    def draw(self):
        if self.deck.cards:
            self.hand.append(self.deck.cards.pop())
        else:
            raise OutOfCards

    def attack(self, player):
        self.board.attack(player.board)

    def get_hit(self, dmg):
        self.hp -= dmg
        if self.hp == 0:
            raise GameOver


