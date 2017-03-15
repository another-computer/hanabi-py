from Deck import Deck
from Card import Card
from Card import colors
from Player import Player

# TO-DO:
# Make interpreter class to replace interpret_string method
# Add wait state before game starts which allows clients to join and ready up
# Once all clients are ready the game will start (need at least 2 to start)
# Make a method to end the game and output desired info


class Lobby(object):
    def __init__(self):

        self.status = None

        self.clients = []

        # Want to add a state that the lobby sits in before starting the game, each player must ready to begin the game
        # Does not include observers

        self.players = {}

        for client in self.clients:
            self.players[client.name] = Player()

        # Need to figure this out
        # Also make it so that drawing from an empty deck yields nothing (empty string)

        self.difficulty = 'Normal'

        self.deck = Deck(self.difficulty)

        self.discard_pile = []

        self.clues = 8
        self.mistakes = 0

        self.foundations = {}

        for color in colors:
            if color not in self.deck.excluded_colors:
                self.foundations[color] = []

        self.score = 0

        self.turn_number = 1

    def client_join(self, client):
        self.clients.append(client)
        self.players[client.name] = Player()

    def client_leave(self, client):
        self.players.pop(client.name)
        self.clients.pop(client)

    def draw(self, name):
        new_card = self.deck.draw()

        self.players[name].draw(new_card)

    # input_string is 'client_name action arg1 (arg2)'
    def interpret_string(self, input_string):
        input_list = input_string.split()

        if input_list[1].lower() == 'help':
            print('Accepted commands include:\n '
                  'play card_location; location ranges from 1 - 5 for your hand(leftmost card is 1)\n '
                  'discard card_location; location ranges from 1-5 for your hand (leftmost card is 1)\n '
                  'clue recipient type; recipient is any other player\'s name; '
                  'type can be any number from 1-5 or any valid color\n')
            return False

        elif input_list[1].lower() == 'play':
            if input_list[2].isdigit() is True:
                if int(input_list[2]) < 1 or int(input_list[2]) > 5:
                    print('THE CARD LOCATION MUST BE IN YOUR HAND MY DUDE')
                    return False

                else:
                    self.play(input_list)
                    return True

            else:
                print('CARD LOCATION IS A NUMBER M\'DOOD')
                return False

        elif input_list[1].lower() == 'discard':
            if self.clues < 8:
                if input_list[2].isdigit() is True:
                    if int(input_list[2]) < 1 or int(input_list[2]) > 5:
                        print('THE CARD LOCATION MUST BE IN YOUR HAND MATE')
                        return False

                    else:
                        self.discard(input_list)
                        return True

                else:
                    print('CARD LOCATION IS A NUMBER M8')
                    return False

            else:
                print('YOU CAN\'T HAVE MORE THAN 8 CLUES')
                return False

        elif input_list[1].lower() == 'clue':
            if len(input_list) == 4:
                if self.clues > 0:
                    if input_list[0] == input_list[2]:
                        print('YOU CAN\'T CLUE YOURSELF BRAH')
                        return False

                    if input_list[2] not in self.players.keys():
                        print('THE PLAYER YOU\'RE CLUING NEEDS TO BE IN THE LOBBY HOMIE')
                        return False

                    if input_list[3].isdigit() is True:
                        if int(input_list[3]) < 1 or int(input_list[3]) > 5:
                            print('THE CLUE MUST BE 1, 2, 3, 4, OR 5 DOG')
                            return False

                    elif input_list[3] not in self.foundations.keys():
                        print('THE CLUED COLOR MUST BE IN THE GAME BOI')
                        return False

                    self.use_clue(input_list)
                    return True

                else:
                    print('not enough clues!')
                    return False

            else:
                print('clue needs 2 arguments')
                return False

        else:
            print('not a valid action. enter \'help\' for a list of commands')
            return False

    def play(self, input_list):
        card = self.players[input_list[0]].get_card(input_list[2])
        card.number_clue = True
        card.color_clue = True

        if len(self.foundations[card.color]) == int(card.number) - 1:
            self.foundations[card.color].append(card)
            self.score += 1

            if card.number == '5':
                self.clues += 1

        else:
            self.discard_pile.append(card)
            self.mistakes += 1

        self.draw(input_list[0])

    def discard(self, input_list):
        card = self.players[input_list[0]].get_card(input_list[2])
        card.number_clue = True
        card.color_clue = True

        self.clues += 1

        self.discard_pile.append(card)

        self.draw(input_list[0])

    def use_clue(self, input_list):

        self.clues -= 1

        self.players[input_list[2]].receive_clue(input_list[3])

    def start_game(self):

        total_players = len(self.clients)

        for name in self.players.keys():
            for count in range(5):
                self.draw(name)

        while True:
            active_player = self.clients[self.turn_number % total_players]

            accepted_action = False

            while accepted_action is False:
                input_string = active_player.name
                input_string += ' ' + input('What do?: ')
                accepted_action = self.interpret_string(input_string)

            if self.mistakes == 3:
                print('YOU LOSE FEELS BAD MAN')
                break

            if self.score == len(list(self.foundations.keys())) * 5:
                print('OH SNAP MAX SCORE')
                break

            if len(self.deck.cards) == 0:
                print('OUT OF CARDS SON')
                break

            self.turn_number += 1


# This is a placeholder and is only used to test the lobby
class Client(object):
    def __init__(self, name):
        self.name = name

if __name__ == '__main__':
    test = Lobby()
    print(test.deck.cards[0])
    print('')

    test.clients = [Client('Andy'), Client('Spencer')]
    test.players = {'Andy': Player(), 'Spencer': Player()}

    test.turn()
