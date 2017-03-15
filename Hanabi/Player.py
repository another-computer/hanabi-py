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

    # This is for playing or discarding a card
    # The player will give the lobby the desired card and let the lobby figure out where to put it
    # I assume card_location is a string with a number since it will be received from the client
    # Also would the player use 0 to reference their first card or 1?
    def get_card(self, card_location):
        return self.hand.pop(int(card_location) - 1)

if __name__ == '__main__':
    from Hanabi.Card import Card

    test = Player()
    print(test.hand)
    print('')

    test.hand = [Card('Blue', '1'), Card('Red', '2'), Card('Green', '5'), Card('Yellow', '4'), Card('White', '5')]
    print(test.hand)
    print('')

    test.receive_clue('Blue')
    print(test.hand)
    print('')

    test.receive_clue('5')
    print(test.hand)
    print('')

    test.receive_clue('Green')
    test.receive_clue('1')
    print(test.hand)
    print('')

    play = test.get_card('2')
    print(test.hand)
    print(play)
    print('')

    test.draw(Card('White', '3'))
    test.receive_clue('Green')
    print(test.hand)
