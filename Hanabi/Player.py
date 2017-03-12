

class Player(object):

    def __init__(self):

        self.name = None

        self.hand = []

    def associate_client(self, client_name):
        self.name = client_name

    def draw(self, drawn_card):
        self.hand.insert(0, drawn_card)

    def receive_clue(self, clue):
        for card in self.hand:
            if card.color == clue:
                card.color_clue = True

            elif card.number == clue:
                card.number_clue = True

if __name__ == '__main__':
    from Hanabi.Card import Card

    test = Player()
    print(test.hand)
    print('')

    test.hand = [Card('Blue', 1), Card('Red', 2), Card('Green', 5), Card('Yellow', 4), Card('White', 5)]
    print(test.hand)
    print('')

    test.receive_clue('Blue')
    print(test.hand)
    print('')

    test.receive_clue(5)
    print(test.hand)

