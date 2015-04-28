import sys
from game import *

def get_colored_card(card):
    if type(card) == EmptyField:
        return "[ ]"
    else:
        return "[%s%d/%s]" % (
                card.strname,
                card.get_att(),
                get_colored_hp(card)
            )

def get_colored_hp(card):
    hp = str(card.get_hp())
    if card.hp_lost:
        if card.get_bonus_hp():
            return color(colors.WARNING, hp)
        else:
            return color(colors.FAIL, hp)
    else:
        if card.get_bonus_hp():
            return color(colors.OKGREEN, hp)
        else:
            return hp


class Game(object):
    player1 = Player("one")
    player2 = Player("two")
    

    def draw_board(self, player):
        return " ".join(get_colored_card(card) for card in player.board.cards)

    def draw(self):
        for player in [self.player1, self.player2]:
            print str(player.hp),
            print "|", 
            print self.draw_board(player),
            print "|", 
            print map(lambda x: x.strname, player.hand),
            print "|", 
            print "Deck:", len(player.deck.cards)

    def command(self, player):
        comm = raw_input(player.name+":").split(" ")
        if comm[0] == 'p':
            card = player.hand.pop(int(comm[1]))
            player.board.add(card, int(comm[2]))
        elif comm[0] == 'x':
            return
        elif comm[0] == 'q':
            sys.exit(0)
        self.draw()
        self.command(player)

    def play(self):
        attacking, defending = self.player1, self.player2
        self.overrides()
        try:
            while True:
                attacking.draw()
                self.draw()
                self.command(attacking)
                attacking.attack(defending)
                attacking, defending = defending, attacking
        except GameOver, e:
            print "Game over", e

    def overrides(self):
        self.player1.hand.append(DrawCardsCard)
        self.player1.hand.append(SpellThiefCard)

game = Game()
game.play()

