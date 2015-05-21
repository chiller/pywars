import unittest
from controller import Game
from game import *

class TCGTest(unittest.TestCase):
        
    def test_empty_field_attacks_player(self):
        p1 = Player("one", None)
        p2 = Player("two", None)
        p1.board.add(CreatureCard, 1)
        p1.attack(p2)
        self.assertEquals(p2.hp, 18)

    def test_deck(self):
        p1 = Player("one", None)
        self.assertTrue(p1.deck)
        cards_cnt = len(p1.deck.cards)
        [p1.draw() for i in range(cards_cnt)]
        from excepts import OutOfCards
        with self.assertRaises(OutOfCards):
            p1.draw()
        self.assertEquals(len(p1.hand),cards_cnt)

    def _game_factory(self, field_config1, field_config2):
        game = Game()
        p1 = game.player1
        p2 = game.player2
        p1.ap, p2.ap = 200, 200
        for card_class, i in zip(field_config1, range(len(field_config1))):
            p1.board.add(card_class, i)
        for card_class, i in zip(field_config2, range(len(field_config2))):
            p2.board.add(card_class, i)
        return p1, p2

    def test_simple_effect(self):
        p1, p2 = self._game_factory([],[CreatureCard, CardWithEffect, CreatureCard])
        p2.attack(p1)
        cwe = p2.board.cards[1]
        self.assertEquals(type(p2.board.cards[3]),EmptyField)
        self.assertEquals(p1.hp, 12)

    def test_defense_modifier(self):
        p1, p2 = self._game_factory([DefensiveCard, CreatureCard],[CreatureCard])
        p1.board.cards[1].die()
        self.assertEquals(type(p1.board.cards[1]), EmptyField)
        self.assertEquals(len(p1.board.cards[0].effects),2)
        self.assertEquals(p1.board.cards[0].get_hp(),7)

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
        p1.board.add(GnomeSnot, 0)
        self.assertEquals(len(p1.hand), 3)
        self.assertEquals(type(p1.board.cards[0]),EmptyField)

    def test_discard_pile(self):
        p1, p2 = self._game_factory([], [])
        self.assertEquals(p1.discard_pile, [])
        p1.board.add(CreatureCard, 0)
        p1.board.cards[0].die()
        self.assertEquals(len(p1.discard_pile), 1) 
        self.assertEqual(p1.discard_pile, [CreatureCard])
        p1.board.add(DefensiveCard, 0)
        p1.board.add(CreatureCard, 0)
        self.assertEqual(p1.discard_pile, [CreatureCard, DefensiveCard])

    def test_building_card(self):
        p1, p2 = self._game_factory([], [])
        self.assertFalse(issubclass(CelestialCastle, CreatureCard))
        p1.board.add(CelestialCastle, 0)
        self.assertFalse(p1.board.cards[0].__class__ == CelestialCastle)
        self.assertTrue(p1.board.buildings)
        self.assertTrue(p1.board.buildings[0].__class__ == CelestialCastle)
        p1.board.add(CelestialCastle, 0)
        self.assertEqual(p1.discard_pile, [CelestialCastle])
        p1.board.add(CreatureCard, 0)
        self.assertEqual(p1.board.cards[0].get_building().__class__, CelestialCastle)
        self.assertEquals(p1.board.cards[0].get_hp(), 8)

    def test_FieldOfNightmares(self):
        p1, p2 = self._game_factory([], [])
        p2.hand.extend([CreatureCard for i in range(5)])
        p1.board.add(FieldOfNightmares, 0)
        self.assertEqual(p1.hp, 20)
        self.assertEqual(p2.hp, 15)

    def test_action_points(self):
        p1, p2 = self._game_factory([], [])
        p1.ap, p2.ap = 2, 2
        self.assertTrue(p1.ap)
        self.assertEqual(p1.ap, 2)
        p1.hand.append(CreatureCard)
        p1.board.add(CreatureCard, 0)
        self.assertEqual(p1.ap, 1)
        p1.board.add(CelestialCastle, 1)
        self.assertEqual(p1.ap, 0)
        with self.assertRaises(OutOfAP):
            p1.board.add(CelestialCastle, 2)
        self.assertEqual(p1.ap, 0)
        self.assertFalse(p1.board.buildings[2].__class__ == CelestialCastle )

    def test_CerebralBloodstorm(self):
        p1, p2 = self._game_factory([], [])
        self.assertTrue(CerebralBloodstorm)
        p2.board.add(CreatureCard,0)
        p2.board.add(CreatureCard,1)
        p2.board.add(CreatureCard,2)
        p1.board.add(CerebralBloodstorm, 0)
        for i in range(len(p2.board.cards)):
            if isinstance(i, CreatureCard):
                self.assertEqual(p2.board.cards[i].hp_lost, 1)
        self.assertEqual(p2.hp, 20)

    def test_WoadTalisman(self):
        p1, p2 = self._game_factory([], [])
        self.assertTrue(WoadTalisman)
        p1.board.add(CreatureCard,0)
        p1.board.add(WoadTalisman, 0)
        self.assertEqual(p1.board.cards[0].get_att(), 4)


if __name__ == '__main__':
    unittest.main()