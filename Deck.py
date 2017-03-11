from Hanabi.Card import Card
from random import shuffle


class Deck(object):
    def __init__(self, multi_color):
        self.deck = []
        self.colors = ['Red', 'White', 'Yellow', 'Green', 'Blue']

        if multi_color is True:
            self.colors.append('Rainbow')

        self.numbers = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]

        for color in self.colors:
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
    print(card)
print(test.cards_remaining)

print('')
print(test.deck[0])
card = test.draw()
print(card)
print(test.cards_remaining)
