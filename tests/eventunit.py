from tcg.events import *
import unittest

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

