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

    def __str__(self, color_code):
        color_display = 'Unknown'
        number_display = ' '

        if self.color_clue is True:
            color_display = self.color

        if self.number_clue is True:
            number_display = self.number

        return '\x1b{}'.format(color_code[color_display]) + '{}'.format(number_display) + '\x1b[0m'

    def clue_check(self, clue):
        if clue == self.color:
            self.color_clue = True

        if clue == self.number:
            self.number_clue = True


if __name__ == '__main__':
    colors = {'Unknown': '[7;37;48m', 'Red': '[7;31;48m', 'Blue': '[7;34;48m', 'Green': '[7;32;48m',
              'Yellow': '[7;33;48m', 'White': '[7;30;48m'}

    test = Card('Blue', 5)
    print(test.__str__(colors))
    print('')

    test.clue_check('Blue')
    print(test.__str__(colors))
    print('')

    test.clue_check(5)
    print(test.__str__(colors))
