# The deck is a randomized list of cards
# 5 colors
# 1 five, 2 fours/threes/twos, 3 ones per color
# Total 50 cards

# Hands are lists of 5 cards each
# Discard pile is a list of all cards that have been removed from a hand through discard

# Cards have color, number, and clue status for both

colors = {'unknown': '[7;37;48m', 'red': '[7;31;48m', 'blue': '[7;34;48m',
          'green': '[7;32;48m', 'yellow': '[7;33;48m', 'white': '[7;30;48m',
          'rainbow': '[0;35;48m'}

numbers = ['1', '2', '3', '4', '5']


class Card(object):

    def __init__(self, color, number):
        self.color = color
        self.number = number

        self.color_clue = False
        self.number_clue = False

    def __str__(self):
        color_display = 'unknown'
        number_display = '?'

        if self.color_clue is True:
            color_display = self.color

        if self.number_clue is True:
            number_display = self.number

        return '\x1b{}{}\x1b[0m'.format(colors[color_display], number_display)

    def __repr__(self):
        color_display = 'unknown'
        number_display = '?'

        # self.reveal()

        if self.color_clue is True:
            color_display = self.color

        if self.number_clue is True:
            number_display = self.number

        return '\x1b{}{}\x1b[0m'.format(colors[color_display], number_display)
    
    def clue_check(self, clue):
        if clue == self.color:
            self.color_clue = True

        if clue == self.number:
            self.number_clue = True

    def reveal(self):
        self.color_clue = True
        self.number_clue = True


if __name__ == '__main__':

    test = Card('blue', '5')
    print(test)
    print('')

    test.clue_check('blue')
    print(test)
    print('')

    test.clue_check('5')
    print(test)
