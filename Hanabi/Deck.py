from Hanabi.Card import Card
from random import shuffle


class Deck(object):
    def __init__(self, multi_color):
        self.deck = []
        self.colors = {'Unknown': '[7;37;48m', 'Red': '[7;31;48m', 'Blue': '[7;34;48m', 'Green': '[7;32;48m',
                       'Yellow': '[7;33;48m', 'White': '[7;30;48m'}

        if multi_color is True:
            self.colors['Rainbow'] = '[0;35;48m'

        self.numbers = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]

        for color in self.colors.keys():
            if color != 'Unknown':
                for number in self.numbers:
                    self.deck.append(Card(color, number))

        shuffle(self.deck)

        self.cards_remaining = len(self.deck)

    def draw(self):
        drawn_card = self.deck[0]

        del self.deck[0]

        self.cards_remaining -= 1

        return drawn_card


test = Deck(False)

for card in test.deck:
    print(card.__str__(test.colors))
print(test.cards_remaining)

print('')
print(test.deck[0].__str__(test.colors))
card = test.draw()
print(card.__str__(test.colors))
print(test.cards_remaining)
