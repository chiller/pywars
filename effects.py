from events import events

class Effect(object):
    
    def __init__(self, card):
        self.card = card

    def attack_modifier(self):
        return 0

    def defense_modifier(self):
        return 0


class FriendlyHasDiedEffect(Effect):
    pass

class SimpleAttackEffect(Effect):

    def attack_modifier(self):
        return len(self.card.board.get_friendly_cards_on_board()) - 1

class WoadAttackEffect(Effect):

    def attack_modifier(self):
        return 2

class NiceIceBabyEffect(Effect):

    def attack_modifier(self):
        opponent = self.card.board.player.game.opponent(self.card.board.player)
        index = self.card.board.cards.index(self.card)

        if opponent.board.cards[index].is_empty():
            return 3
        else:
            return 0

class SimpleDefensiveEffect(Effect):
    permanent = 0
    def defense_modifier(self):
        if filter(lambda x: type(x) == FriendlyHasDiedEffect, self.card.effects):
            self.permanent = 2
        return self.permanent

class DrawCardsEffect(Effect):
    def __init__(self,*args):
        super(DrawCardsEffect, self).__init__(*args)
        [self.card.board.player.draw() for _ in range(3)]

class SpellThiefEffect(Effect):
    permanent = 0
    def __init__(self, *args):
        super(SpellThiefEffect, self).__init__(*args)
        events.subscribe("spellcardplayed", self.handler)

    def handler(self, e):
        self.permanent += 1

    def attack_modifier(self):
        return self.permanent
