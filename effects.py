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
        return len(self.card.field.get_friendly_cards_on_field()) - 1

class WoadAttackEffect(Effect):

    def attack_modifier(self):
        return 2

class NiceIceBabyEffect(Effect):

    def attack_modifier(self):
        opponent = self.card.field.player.game.opponent(self.card.field.player)
        index = self.card.field.cards.index(self.card)

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
        [self.card.field.player.draw() for i in range(3)]