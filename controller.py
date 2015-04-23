import sys
from game import *
class Game(object):
    player1 = Player("one")
    player2 = Player("two")
    

    def draw(self):
        for player in [self.player1, self.player2]:
            print player.hp, 
            print "|", 
            print player.field, 
            print map(lambda x: x.strname, player.hand),
            print "|", 
            print "Deck:", len(player.deck.cards)

    def command(self, player):
        comm = raw_input(player.name+":").split(" ")
        if comm[0] == 'p':
            card = player.hand.pop(int(comm[1]))
            player.field.add(card, int(comm[2]))
        elif comm[0] == 'x':
            return
        elif comm[0] == 'q':
            sys.exit(0)
        self.draw()
        self.command(player)

    def play(self):
        attacking, defending = self.player1, self.player2
        try:
            while True:
                attacking.draw()
                self.draw()
                self.command(attacking)
                attacking.attack(defending)
                attacking, defending = defending, attacking
        except GameOver, e:
            print "Game over", e 
game = Game()
game.play()

