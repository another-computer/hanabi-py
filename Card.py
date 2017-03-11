# The deck is a randomized list of cards
# 5 colors
# 1 five, 2 fours/threes/twos, 3 ones per color
# Total 50 cards

# Hands are lists of 5 cards each
# Discard pile is a list of all cards that have been removed from a hand through discard

# Cards have color, number, and clue status for both


class Card(object):
    def __init__(self, color, number):
        self.color = color
        self.number = number

        self.color_clue = False
        self.number_clue = False

    def __str__(self):
        return '{}, {}'.format(self.color, self.number)

    def clue_check(self, clue):
        if clue == self.color:
            self.color_clue = True

        if clue == self.number:
            self.number_clue = True

test = Card('Blue', 5)
print(test)
