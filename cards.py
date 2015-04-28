from effects import *
from utils import color, colors
class Card(object):
    hp = 5
    hp_lost = 0
    att = 2
    strname = "C"

    def __init__(self, field):
        self.field = field
        self.effects = [Effect(self)]

    def die(self):
        index = self.field.cards.index(self)
        self.field.cards[index] = EmptyField(self.field)
        self.field.player.discard_pile.append(self.__class__)
        for card in self.field.cards:
            card.effects.append(FriendlyHasDiedEffect(card))
    
    def get_bonus_hp(self):
        return sum(map(lambda x:x.defense_modifier(),self.effects))

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
    
    def __str__(self):
        return "[%s%d/%d]" % (self.strname, self.get_att(), self.get_hp())

    
class EmptyField(Card):
    hp = 0
    att = 0
    strname = ""
    def get_hit(self, damage):
        if self.field.player:
            self.field.player.get_hit(damage)
    
    def attack(self, damage):
        pass

    def __str__(self):
        return "[ ]"


class CreatureCard(Card):
    pass

class SpellCard(Card):
    def __str__(self):
        return "[%s]" % (self.strname)



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

class DrawCardsCard(SpellCard):
    strname = "D3"
    def __init__(self, *args):
        super(DrawCardsCard, self).__init__(*args)
        self.effects = [DrawCardsEffect(self)]

class SpellThiefCard(CreatureCard):
    strname = "ST"
    def __init__(self, *args):
        super(SpellThiefCard, self).__init__(*args)
        self.effects = [SpellThiefEffect(self)]

