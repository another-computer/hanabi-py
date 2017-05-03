from Deck import Deck
from Card import Card
from Card import colors
from Player import Player
import threading

# TO-DO:
# Replace the interpret_string method because there has to be a better way to handle that
#
# Add wait state before game starts which allows clients to join and ready up
# Once all clients are ready the game will start (need at least 2 to start)
#
# Make a method to end the game and output desired info, and clean up the lobby in whatever way is needed
# Possibly a segment where it waits for players to agree to rematch or all disconnect
# Then it resets the lobby as needed, with a rematch method preserving the players and clients
#
# Possibly add a true_print to Card so that we can easily print the true value without changing it's
# clue status
#
# Should I make variables like accepted_action and active_player a part of __init__ and self?


class Lobby(object):
    def __init__(self):

        self.commands = {'play': self.play, 'clue': self.use_clue, 'discard': self.discard}

        self.clients = []

        self.players = {}
        self.ready_players = 0

        self.current_player = None
        self.accepted_action = False

        self.difficulty = 'Normal'

        self.deck = Deck(self.difficulty)

        self.discard_pile = {}
        self.foundations = {}

        for color in colors:
            if color not in self.deck.excluded_colors:
                self.foundations[color] = Card(color, '0')
                self.foundations[color] = self.foundations[color].reveal()
                self.discard_pile[color] = []

        self.clues = 8
        self.mistakes = 0
        self.score = 0

        self.turn_number = 1

    def add_player(self, client):
        self.players[client] = Player()

    def remove_player(self, client):
        self.players.pop(client.name)
        self.clients.pop(client)

    def draw(self, name):
        new_card = self.deck.draw()

        self.players[name].draw(new_card)

    # input_string is 'client_name action arg1 (arg2)'
    '''def interpret_string(self, active_player, input_string):
        input_list = input_string.split()
        input_list[0] = input_list[0].lstrip('/')
        print(input_list)

        if input_list[0].lower() == 'help':
            print('Accepted commands include:\n '
                  'play card_location; location ranges from 1 - 5 for your hand(leftmost card is 1)\n '
                  'discard card_location; location ranges from 1-5 for your hand (leftmost card is 1)\n '
                  'clue recipient type; recipient is any other player\'s name; '
                  'type can be any number from 1-5 or any valid color\n')
            return False

        elif input_list[0].lower() == 'play':
            if input_list[1].isdigit() is True:
                if int(input_list[1]) < 1 or int(input_list[1]) > len(self.players[active_player].hand):
                    print('THE CARD LOCATION MUST BE IN YOUR HAND MY DUDE')
                    return False

                else:
                    self.play(active_player, input_list)
                    return True

            else:
                print('CARD LOCATION IS A NUMBER M\'DOOD')
                return False

        elif input_list[0].lower() == 'discard':
            if self.clues < 8:
                if input_list[1].isdigit() is True:
                    if int(input_list[1]) < 1 or int(input_list[1]) > len(self.players[active_player].hand):
                        print('THE CARD LOCATION MUST BE IN YOUR HAND MATE')
                        return False

                    else:
                        self.discard(active_player, input_list)
                        return True

                else:
                    print('CARD LOCATION IS A NUMBER M8')
                    return False

            else:
                print('YOU CAN\'T HAVE MORE THAN 8 CLUES')
                return False

        elif input_list[0].lower() == 'clue':
            if len(input_list) == 3:
                if self.clues > 0:
                    if active_player == input_list[1]:
                        print('YOU CAN\'T CLUE YOURSELF BRAH')
                        return False

                    if input_list[1] not in self.players.keys():
                        print('THE PLAYER YOU\'RE CLUING NEEDS TO BE IN THE LOBBY HOMIE')
                        return False

                    if input_list[2].isdigit() is True:
                        if int(input_list[2]) < 1 or int(input_list[2]) > 5:
                            print('THE CLUE MUST BE 1, 2, 3, 4, OR 5 DOG')
                            return False

                    elif input_list[2].lower() not in self.foundations.keys():
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
            return False'''

    def play(self, active_player, input_list):

        if active_player != self.current_player:
            print('It\'s not your turn')
            return False

        if input_list[0].isdigit() is True:
            if int(input_list[0]) < 1 or int(input_list[0]) > len(self.players[active_player].hand):
                print('THE CARD LOCATION MUST BE IN YOUR HAND MY DUDE')
                return False

            else:
                pass

        else:
            print('CARD LOCATION IS A NUMBER M\'DOOD')
            return False

        card = self.players[active_player].get_card(input_list[0])
        card.reveal()

        if int(self.foundations[card.color].number) == int(card.number) - 1:
            self.foundations[card.color] = card
            self.score += 1

            if card.number == '5' and self.clues < 8:
                self.clues += 1

        else:
            self.discard_pile[card.color].append(card)
            self.mistakes += 1

        self.draw(active_player)

        return True

    def discard(self, active_player, input_list):

        if active_player != self.current_player:
            print('It\'s not your turn')
            return False

        if self.clues < 8:
            if input_list[0].isdigit() is True:
                if int(input_list[0]) < 1 or int(input_list[0]) > len(self.players[active_player].hand):
                    print('THE CARD LOCATION MUST BE IN YOUR HAND MATE')
                    return False

                else:
                    pass

            else:
                print('CARD LOCATION IS A NUMBER M8')
                return False

        else:
            print('YOU CAN\'T HAVE MORE THAN 8 CLUES')
            return False

        card = self.players[active_player].get_card(input_list[0])
        card.reveal()

        self.clues += 1

        self.discard_pile[card.color].append(card)

        self.draw(active_player)

        return True

    def use_clue(self, active_player, input_list):

        if active_player != self.current_player:
            print('It\'s not your turn')
            return False

        if len(input_list) == 3:
            if self.clues > 0:
                if active_player == input_list[1]:
                    print('YOU CAN\'T CLUE YOURSELF BRAH')
                    return False

                if input_list[1] not in self.players.keys():
                    print('THE PLAYER YOU\'RE CLUING NEEDS TO BE IN THE LOBBY HOMIE')
                    return False

                if input_list[2].isdigit() is True:
                    if int(input_list[2]) < 1 or int(input_list[2]) > 5:
                        print('THE CLUE MUST BE 1, 2, 3, 4, OR 5 DOG')
                        return False

                elif input_list[2].lower() not in self.foundations.keys():
                    print('THE CLUED COLOR MUST BE IN THE GAME BOI')
                    return False

                pass

            else:
                print('not enough clues!')
                return False

        else:
            print('clue needs 2 arguments')
            return False

        self.clues -= 1

        self.players[input_list[0]].receive_clue(input_list[1].lower())

        return True

    '''def start_game(self):
        final_round = 0

        for name in self.players.keys():
            for count in range(5):
                self.draw(name)

        while True:
            self.clients = list(self.players.keys())
            active_player = self.clients[self.turn_number % len(self.clients)]

            accepted_action = False

            while accepted_action is False:

                input_string = active_player
                input_string += ' ' + input('What do?: ')
                accepted_action = self.interpret_string(input_string)

            if self.mistakes == 3:
                print('YOU LOSE FEELS BAD MAN')
                break

            if self.score == len(list(self.foundations.keys())) * 5:
                print('OH SNAP MAX SCORE')
                break

            if len(self.deck.cards) == 0:
                final_round += 1

                if final_round == len(self.players) + 1:
                    print('OUT OF CARDS SON')
                    break

            self.turn_number += 1

        self.end_game()'''

    def prepare_game(self):
        for name in self.players.keys():
            for count in range(5):
                self.draw(name)

    def end_game(self):
        print(self.score)
        print(self.foundations)
        print(self.discard_pile)


# This is a placeholder and is only used to test the lobby
class Client(object):
    def __init__(self, name):
        self.name = name

if __name__ == '__main__':
    print('neat')
