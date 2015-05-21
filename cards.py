from effects import *
from utils import color, colors
class Card(object):
    hp = 5
    hp_lost = 0
    att = 2
    strname = "C"
    cost = 0

    def __init__(self, field):
        self.field = field
        self.effects = [Effect(self)]
    
    def get_att(self):
        return 0
    
    def die(self):
        index = self.field.cards.index(self)
        self.field.cards[index] = EmptyField(self.field)
        self.field.player.discard_pile.append(self.__class__)
        for card in self.field.cards:
            card.effects.append(FriendlyHasDiedEffect(card))

    def __str__(self):
        return "[" + self.strname + "]"

class EmptyField(Card):
    hp = 0
    att = 0
    strname = ""
    def get_hit(self, damage):
        if self.field.player:
            self.field.player.get_hit(damage)
    
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
        card_index = self.field.cards.index(self)
        if self.field.cards[card_index]:
            return self.field.buildings[card_index]

class SpellCard(Card):
    cost = 1
    def __init__(self, field, position=None):
       super(SpellCard, self).__init__(field)
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

class GnomeSnot(SpellCard):
    strname = "D3"
    def __init__(self, *args):
        super(GnomeSnot, self).__init__(*args)
        self.effects = [DrawCardsEffect(self)]

class FieldOfNightmares(SpellCard):
    strname = "FN"
    def __init__(self, field, position=None):
        super(FieldOfNightmares, self).__init__(field)
        opponent = self.field.player.game.opponent(self.field.player)
        [opponent.get_hit(1) for card in opponent.hand]

class CelestialCastle(BuildingCard):
    strname = "CC"
    bonus_hp = 3

class CerebralBloodstorm(SpellCard):
    strname = "CB"
    def __init__(self, field, position=None):
        super(CerebralBloodstorm, self).__init__(field)
        opponent = self.field.player.game.opponent(self.field.player)
        for i in range(len(opponent.board.cards)):
            if isinstance(i, CreatureCard):
                opponent.board.cards[i].get_hit(1)

class WoadTalisman(SpellCard):
    strname = "WT"
    def __init__(self, field, position):
        super(WoadTalisman, self).__init__(field)
        card = self.field.cards[position]
        card.effects += [WoadAttackEffect(card)]