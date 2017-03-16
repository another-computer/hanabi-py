from Card import Card
from Card import colors
from Card import numbers
from random import shuffle


class Deck(object):

    def __init__(self, difficulty):
        self.cards = []
        self.frequencies = [3, 2, 2, 2, 1]
        self.excluded_colors = ["unknown"]

        if difficulty == "Normal":
            self.excluded_colors.append("rainbow")

        elif difficulty == "Difficult":
            self.frequencies = [1, 1, 1, 1, 1]

        for color in colors.keys():
            if color not in self.excluded_colors:
                for number in numbers:
                    for x in range(self.frequencies[int(number) - 1]):
                        self.cards.append(Card(color, number))

        shuffle(self.cards)

        self.cards_remaining = len(self.cards)

    def draw(self):
        drawn_card = self.cards.pop()
        self.cards_remaining = len(self.cards)

        return drawn_card

if __name__ == '__main__':
    test = Deck("Normal")

    for card in test.cards:
        print(card)
    print(test.cards_remaining)

    print('')
    print(test.cards[-1])
    card = test.draw()
    print(card)
    print(test.cards_remaining)
