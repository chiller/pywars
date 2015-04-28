from tcg.events import *
import unittest
from unit import BaseTCGTest
from tcg.game import *
class Doge():
    h1 = 0
    h2 = 0
    def handler1(self, e):
        self.h1 += 1

    def handler2(self, e):
        self.h2 += 1

    def __init__(self):
        events.subscribe("a", self.handler1)
        events.subscribe("a", self.handler2)
        

class EventTest(unittest.TestCase):
    def setUp(self):
        events.unsubscribe_all()

    def test_assertion(self):
        self.assertFalse(events.handlers)
        doge = Doge()
        self.assertEquals(
            len(events.handlers.keys()), 1
        )        
        events.emit("a")
        self.assertEquals(doge.h1, 1)
        self.assertEquals(doge.h2, 1)

    def test_subscribe(self):
        self.assertFalse(events.handlers)
        doge1 = Doge()
        doge2 = Doge()  
        events.unsubscribe(doge2)
        self.assertEquals(len(events.handlers["a"]),2)

class EventIntegrationTest(BaseTCGTest):
    
    def test_spellthief(self):
        p1, p2 = self._game_factory([],[SpellThiefCard])
        stc = p2.board.cards[0]
        self.assertEquals(stc.get_att(), 2)
        p1.board.add(DrawCardsCard, 1)
        self.assertEquals(stc.get_att(), 3)
        p2.board.add(DrawCardsCard, 1)
        self.assertEquals(stc.get_att(), 4)
        #should not trigger if replaced
        self.assertEquals(len(p2.discard_pile), 1)
        p2.board.add(DefensiveCard, 0)
        self.assertEquals(len(p2.discard_pile), 2)
        self.assertEquals(len(events.handlers['spellcardplayed']), 0)
        self.assertEquals(stc.get_att(), 4)
        
