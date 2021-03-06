import sys
from game import *

def get_colored_card(card):
    if type(card) == EmptyField:
        return "[     ]"
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


def print_buildings(player):
    bs = []
    for building in player.board.buildings:
        if building:
            bs.append( "[--" + color(colors.OKBLUE, building.strname) + "-]")
        else:
            bs.append("[     ]")
    return "       " + " ".join(bs)


class Game(object):

    def __init__(self):
        super(Game, self).__init__()
        self.player1 = Player("one", self)
        self.player2 = Player("two", self)

    def opponent(self, player):
        if player == self.player1:
            return self.player2
        return self.player1

    def draw_board(self, player):
        return " ".join(get_colored_card(card) for card in player.board.cards)

    def draw(self):
        print print_buildings(self.player1)
        for player in [self.player1, self.player2]:
            print str(player.hp),
            print str(player.ap),
            print "|", 
            print self.draw_board(player),
            print "|", 
            print map(lambda x: x.strname, player.hand),
            print "|", 
            print "Deck:", len(player.deck.cards)
        print print_buildings(self.player2)

    def command(self, player):
        comm = raw_input(player.name+":").split(" ")
        if comm[0] == 'p':
            card = player.hand[int(comm[1])]
            try:
                player.board.add(card, int(comm[2]))
                player.hand.pop(int(comm[1]))
            except OutOfAP:
                print "Not enough AP"
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
                attacking.start_turn()
                self.draw()
                self.command(attacking)
                attacking.attack(defending)
                attacking, defending = defending, attacking
        except GameOver, e:
            print "Game over", e

    def overrides(self):
        for _ in range(5):
            self.player1.draw()
            self.player2.draw()


if __name__ == '__main__':
    game = Game()
    game.play()



