import unittest
from game import *
from exceptions import *

class TCGTest(unittest.TestCase):

    def test_simple_interaction(self):

        d1 = Field(None)
        d1.add(Card, 0)
        self.assertEquals(d1.cards[0].hp, 5)

        d2 = Field(None)
        d2.add(Card, 0)
        self.assertEquals(d2.cards[0].hp, 5)

        d1.attack(d2)
        self.assertEquals(d2.cards[0].hp, 3)
        self.assertEquals(d1.cards[0].hp, 3)
        d1.attack(d2)
        d1.attack(d2)
        
    def test_empty_field_attacks_player(self):
        p1 = Player("one")
        p2 = Player("two")
        p1.field.add(Card, 1)
        p1.attack(p2)
        self.assertEquals(p2.hp, 18)

    def test_deck(self):
        p1 = Player("one")
        self.assertTrue(p1.deck)
        p1.draw()
        p1.draw()
        p1.draw()
        with self.assertRaises(OutOfCards):
            p1.draw()
        self.assertEquals(len(p1.hand),3)

    def _game_factory(self, field_config1, field_config2):
        p1 = Player("one")
        p2 = Player("two")
        for card_class, i in zip(field_config1, range(len(field_config1))):
            p1.field.add(card_class, i)
        for card_class, i in zip(field_config2, range(len(field_config2))):
            p2.field.add(card_class, i)
        return p1, p2

    def test_simple_effect(self):
        p1, p2 = self._game_factory([],[Card, CardWithEffect, Card])
        p2.attack(p1)
        self.assertEquals(p1.hp, 12)

    def test_defense_modifier(self):
        p1, p2 = self._game_factory([DefensiveCard, Card],[Card])
        p1.field.cards[1].die()
        self.assertEquals(type(p1.field.cards[1]), EmptyField)
        self.assertEquals(len(p1.field.cards[0].effects),2)
        self.assertEquals(p1.field.cards[0].get_hp(),7)


    #TODO: game engine for turns and to connect controls

    #TODO: console game

    #TODO: more card types

    #TODO: card effects

unittest.main()