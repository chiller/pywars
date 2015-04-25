import unittest
from game import *

class TCGTest(unittest.TestCase):
        
    def test_empty_field_attacks_player(self):
        p1 = Player("one")
        p2 = Player("two")
        p1.field.add(CreatureCard, 1)
        p1.attack(p2)
        self.assertEquals(p2.hp, 18)

    def test_deck(self):
        p1 = Player("one")
        self.assertTrue(p1.deck)
        cards_cnt = len(p1.deck.cards)
        [p1.draw() for i in range(cards_cnt)]
        from excepts import OutOfCards
        with self.assertRaises(OutOfCards):
            p1.draw()
        self.assertEquals(len(p1.hand),cards_cnt)

    def _game_factory(self, field_config1, field_config2):
        p1 = Player("one")
        p2 = Player("two")
        for card_class, i in zip(field_config1, range(len(field_config1))):
            p1.field.add(card_class, i)
        for card_class, i in zip(field_config2, range(len(field_config2))):
            p2.field.add(card_class, i)
        return p1, p2

    def test_simple_effect(self):
        p1, p2 = self._game_factory([],[CreatureCard, CardWithEffect, CreatureCard])
        p2.attack(p1)
        cwe = p2.field.cards[1]
        self.assertEquals(type(p2.field.cards[3]),EmptyField)
        self.assertEquals(p1.hp, 12)

    def test_defense_modifier(self):
        p1, p2 = self._game_factory([DefensiveCard, CreatureCard],[CreatureCard])
        p1.field.cards[1].die()
        self.assertEquals(type(p1.field.cards[1]), EmptyField)
        self.assertEquals(len(p1.field.cards[0].effects),2)
        self.assertEquals(p1.field.cards[0].get_hp(),7)

    def test_keep_track_of_dmg(self):
        self.assertEquals(CreatureCard.hp_lost, 0)

    def test_card_hierarchy(self):
        c = DefensiveCard(None)
        self.assertTrue(isinstance(c, CreatureCard))
        self.assertTrue(isinstance(c, CreatureCard))
        self.assertTrue(isinstance(c, DefensiveCard))
        self.assertFalse(type(c)==CreatureCard)
        self.assertFalse(type(c)==CreatureCard)
        self.assertTrue(type(c)==DefensiveCard)
        self.assertTrue(issubclass(DefensiveCard, CreatureCard))

    def test_spell_card(self):
        p1, p2 = self._game_factory([],[])
        p1.deck.cards.extend([CreatureCard for i in range(5)])
        p1.field.add(DrawCardsCard, 0)
        self.assertEquals(len(p1.hand), 3)
        self.assertEquals(type(p1.field.cards[0]),EmptyField)

    def test_discard_pile(self):
        p1, p2 = self._game_factory([], [])
        self.assertEquals(p1.discard_pile, [])
        p1.field.add(CreatureCard, 0)
        p1.field.cards[0].die()
        self.assertEquals(len(p1.discard_pile), 1) 
        self.assertEqual(p1.discard_pile, [CreatureCard])
        p1.field.add(DefensiveCard, 0)
        p1.field.add(CreatureCard, 0)
        self.assertEqual(p1.discard_pile, [CreatureCard, DefensiveCard])


unittest.main()