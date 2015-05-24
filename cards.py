from effects import *
from utils import color, colors
class Card(object):
    hp = 5
    hp_lost = 0
    att = 2
    strname = "C"
    cost = 0

    def __init__(self, board):
        self.board = board
        self.effects = [Effect(self)]

    def discard(self):
        self.board.player.discard_pile.append(self.__class__)
        events.unsubscribe(self)
        for effect in self.effects:
            events.unsubscribe(effect)
    
    def get_att(self):
        return 0
    
    def die(self):
        index = self.board.cards.index(self)
        self.board.cards[index] = EmptyField(self.board)
        for card in self.board.cards:
            card.effects.append(FriendlyHasDiedEffect(card))
        self.discard()

    def is_empty(self):
        return isinstance(self, EmptyField)

    def __str__(self):
        return "[" + self.strname + "]"

class EmptyField(Card):
    hp = 0
    att = 0
    strname = ""
    def get_hit(self, damage):
        if self.board.player:
            self.board.player.get_hit(damage)
    
    def attack(self, damage):
        pass




class CreatureCard(Card):
    
    cost = 1

    def __str__(self):
        return "[%s%d/%d]" % (self.strname, self.get_att(), self.get_hp())

    def get_hp(self):
        return self.hp + \
            self.get_bonus_hp() -\
            self.hp_lost
    
    def get_att(self):
        return self.att + sum(map(lambda x: x.attack_modifier(), self.effects))
    
    def get_hit(self, damage):
        self.hp_lost += damage
        if self.get_hp() <= 0:
            self.die()

    def attack(self, card):
        card.get_hit(self.get_att())
        self.get_hit(card.get_att())
       
    def get_bonus_hp(self):
        sum_from_effects = sum(map(lambda x:x.defense_modifier(),self.effects))
        if self.get_building():
            from_building = self.get_building().bonus_hp
        else:
            from_building = 0
        return from_building + sum_from_effects
    
    def get_building(self):
        card_index = self.board.cards.index(self)
        if self.board.cards[card_index]:
            return self.board.buildings[card_index]

class SpellCard(Card):
    cost = 1
    def __init__(self, board, position=None):
       super(SpellCard, self).__init__(board)
    def __str__(self):
        return "[%s]" % (self.strname)

class BuildingCard(Card):
    cost = 1



class CardWithEffect(CreatureCard):
    strname = "CA"
    def __init__(self, *args):
        super(CardWithEffect, self).__init__(*args)
        self.effects = [SimpleAttackEffect(self)]


class DefensiveCard(CreatureCard):
    strname = "CD"
    def __init__(self, *args):
        super(DefensiveCard, self).__init__(*args)
        self.effects = [SimpleDefensiveEffect(self)]

class NiceIceBaby(CreatureCard):
    strname = "NB"
    hp = 2
    att = 1
    def __init__(self, *args):
        super(NiceIceBaby, self).__init__(*args)
        self.effects = [NiceIceBabyEffect(self)]

class GnomeSnot(SpellCard):
    strname = "D3"
    def __init__(self, *args):
        super(GnomeSnot, self).__init__(*args)
        self.effects = [DrawCardsEffect(self)]

class SpellThiefCard(CreatureCard):
    strname = "ST"
    def __init__(self, *args):
        super(SpellThiefCard, self).__init__(*args)
        self.effects = [SpellThiefEffect(self)]

class FieldOfNightmares(SpellCard):
    strname = "FN"
    def __init__(self, board, position=None):
        super(FieldOfNightmares, self).__init__(board)
        opponent = self.board.player.game.opponent(self.board.player)
        [opponent.get_hit(1) for card in opponent.hand]

class CelestialCastle(BuildingCard):
    strname = "CC"
    bonus_hp = 3

class CerebralBloodstorm(SpellCard):
    strname = "CB"
    def __init__(self, board, position=None):
        super(CerebralBloodstorm, self).__init__(board)
        opponent = self.board.player.game.opponent(self.board.player)
        for i in range(len(opponent.board.cards)):
            if isinstance(i, CreatureCard):
                opponent.board.cards[i].get_hit(1)

class WoadTalisman(SpellCard):
    strname = "WT"
    cost = 0
    def __init__(self, board, position):
        super(WoadTalisman, self).__init__(board)
        card = self.board.cards[position]
        card.effects += [WoadAttackEffect(card)]

