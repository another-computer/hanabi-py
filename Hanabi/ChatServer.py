import select
import socket
import sys
import threading
from Lobby import Lobby

# Need to add a chat limit, lobby limit, and character limit


class ChatServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_address = ('localhost', 5000)
        print('starting up on {} port {}'.format(self.server_address[0], self.server_address[1]))

        self.server_socket.bind(self.server_address)

        self.backlog = 5
        self.data_size = 4096
        self.server_socket.listen(self.backlog)

        self.socket_list = [self.server_socket]
        self.running_status = True

        self.sock = None

        self.username_dictionary = {}
        self.lobby_dictionary = {}
        self.client_positions = {}

        self.commands = {'help': self.command_help, 'nick': self.command_nick, 'lobby': self.command_lobby,
                         'lobbies': self.command_lobbies, 'ready': self.command_ready, 'join': self.command_join}
        self.game_list = ['hanabi']

        while self.running_status is True:
            print('waiting for a connection')

            self.input_ready, self.output_ready, self.except_ready = select.select(self.socket_list, [], [])

            for self.sock in self.input_ready:

                if self.sock == self.server_socket:
                    # handle the server socket
                    client, address = self.server_socket.accept()

                    if client not in self.socket_list:
                        print('connection from {}'.format(address))
                        client.send('\r[Server] What is your username?'.encode())
                        self.socket_list.append(client)

                        name_thread = threading.Thread(target=self.name_client, args=[client, address])
                        name_thread.setDaemon(True)
                        name_thread.start()

                elif self.sock == sys.stdin:
                    # handle standard input
                    self.running_status = False

                else:

                    try:
                        # handle all other sockets
                        self.data = self.sock.recv(self.data_size).decode()
                        print('\r[' + str(self.sock.getpeername()) + '] ' + self.data)

                        if self.data:
                            if self.data[0] == '/':
                                self.data = self.data.lstrip('/')

                                command_thread = threading.Thread(target=self.interpret_command, args=[self.data])
                                command_thread.setDaemon(True)
                                command_thread.start()

                            else:
                                self.broadcast(self.server_socket, self.sock, '\r[' +
                                               self.username_dictionary[self.sock.getpeername()] + '] ' + self.data)

                        else:
                            if self.sock in self.socket_list:
                                self.socket_list.remove(self.sock)

                                self.broadcast(self.server_socket, self.sock, '\r[Server] {} left our chatting room'
                                               .format(self.username_dictionary[address]))
                            print('Client {} is offline'.format(address))

                    except:
                        self.broadcast(self.server_socket, self.sock, '\r[Server] {} left our chatting room'
                                       .format(self.username_dictionary[address]))
                        print('Client {} is offline'.format(address))
                        self.sock.close()
                        self.socket_list.remove(self.sock)
                        continue

        self.server_socket.close()

    def name_client(self, client, address):
        name = None

        try:
            while True:
                name = client.recv(self.data_size).decode()

                if name not in list(self.username_dictionary.values()) and len(name) <= 20:
                    self.username_dictionary[address] = name
                    self.client_positions[address] = None
                    break

                elif len(name) > 20:
                    client.send('\r[Server] username must be less than or equal to 20 characters'.encode())

                else:
                    client.send('\r[Server] username in use, try again'.encode())

        except:
            self.username_dictionary[address] = str(address)
            pass

        finally:
            print('{} registered'.format(name))

            self.broadcast(self.server_socket, client, '\r[Server] {} entered our chatting room'
                           .format(self.username_dictionary[address]))
            return

    def broadcast(self, server_socket, input_sock, message):
        for current_socket in self.socket_list:
            # send the message only to peer
            if current_socket != server_socket and current_socket != input_sock:
                try:
                    current_socket.send(message.encode())

                except:
                    # broken socket connection
                    current_socket.close()

                    # broken socket, remove it
                    if current_socket in self.socket_list:
                        self.socket_list.remove(current_socket)

    def interpret_command(self, command):
        command = command.split()

        if command[0] in self.commands.keys():
            valid_command = command[0]
            command.pop(0)

            if self.client_positions[self.sock.getpeername()] is not None:

                if valid_command in self.lobby_dictionary[self.client_positions
                                                          [self.sock.getpeername()]].commands.keys():

                    self.commands[valid_command](self.sock.getpeername(), command)

            else:
                self.commands[valid_command](command)

    def command_nick(self, new_username):
        """/nick changes the username a client uses. 
        Usage: /nick [new_username]"""

        if new_username == []:
            self.sock.send('\r[Server] /nick requires a name input'.encode())

        else:
            if new_username[0] in list(self.username_dictionary.values()):
                self.sock.send('\r[Server] username in use, try again'.encode())

            elif len(new_username[0]) > 20:
                self.sock.send('\r[Server] username must be less than or equal to 20 characters'.encode())

            old_name = self.username_dictionary[self.sock.getpeername()]
            self.username_dictionary[self.sock.getpeername()] = new_username[0]
            print('{} renamed'.format(self.sock.getpeername()))

            self.broadcast(self.server_socket, self.sock, '\r[Server] ' + old_name + ' changed to ' +
                           self.username_dictionary[self.sock.getpeername()])

    def command_help(self, requested_command):
        """/help provides a list of all available commands.
        A command can be input to provide additional info. 
        Usage: /help [optional_command]"""

        if requested_command == []:
            self.sock.send('\r[Server] Available commands include: {}'.format(list(self.commands.keys())).encode())

        elif requested_command[0] in list(self.commands.keys()):
            self.sock.send('\r[Server] {}'.format(self.commands[requested_command[0]].__doc__).encode())

    def command_lobby(self, game_type):
        """/lobby creates a new game lobby.
        It requires a game argument to function.
        Usage: /lobby [game]"""

        if game_type == []:
            self.sock.send('\r[Server] /lobby requires the desired game as an argument'.encode())

        elif game_type[0].lower() in self.game_list:
            game_type = game_type[0]
            lobby_name = '{}_{}'.format(game_type.lower(), len(self.lobby_dictionary.keys()) + 1)

            self.lobby_dictionary[lobby_name] = Lobby()
            self.lobby_dictionary[lobby_name].add_player(self.sock.getpeername())
            self.client_positions[self.sock.getpeername()] = lobby_name

            self.broadcast(self.server_socket, None,
                           '\r[Server] {} lobby started in {}'.format(game_type.lower(), lobby_name))

            self.commands = {**self.commands, **self.lobby_dictionary[lobby_name].commands}

            lobby_thread = threading.Thread(target=self.standby, args=[lobby_name])
            lobby_thread.setDaemon(True)
            lobby_thread.start()

        else:
            self.sock.send('\r[Server] The requested game is not supported'.encode())

    def command_lobbies(self, argument=None):
        """/lobbies lists the current running lobbies.
        Usage: /lobbies"""

        self.sock.send('\r[Server] {}'.format(list(self.lobby_dictionary.keys())).encode())

    def command_ready(self, argument=None):
        """/ready is used to ready up for an active lobby.
        Usage: /ready"""

        self.lobby_dictionary[self.client_positions[self.sock.getpeername()]].ready_players += 1

    def command_join(self, desired_lobby):
        """/join is used to join an existing lobby.
        Usage: /join [lobby_name]"""

        if desired_lobby[0] not in self.lobby_dictionary.keys():
            self.sock.send('\r[Server] lobby not found'.encode())

        else:
            print('{} entered {}'.format(self.sock.getpeername(), desired_lobby[0]))
            self.sock.send('\r[Server] You have entered {}'.format(desired_lobby[0]).encode())

            self.lobby_dictionary[desired_lobby[0]].add_player(self.sock.getpeername())
            self.client_positions[self.sock.getpeername()] = desired_lobby[0]

    def standby(self, lobby_name):
        lobby_obj = self.lobby_dictionary[lobby_name]

        while lobby_obj.ready_players < 2 or lobby_obj.ready_players < len(lobby_obj.players.keys()):
            pass

        self.turn_sequence(lobby_name)

    def turn_sequence(self, lobby_name):

        lobby_obj = self.lobby_dictionary[lobby_name]
        final_round = 0

        lobby_obj.prepare_game()

        while True:
            lobby_obj.clients = list(lobby_obj.players.keys())
            current_player = lobby_obj.clients[lobby_obj.turn_number % len(lobby_obj.clients)]
            lobby_obj.current_player = current_player

            self.sock.send('\r[{}] Your turn'.format(lobby_name).encode())

            while lobby_obj.accepted_action is not True:
                pass

            if lobby_obj.mistakes == 3:
                print('YOU LOSE FEELS BAD MAN')
                break

            if lobby_obj.score == len(list(lobby_obj.foundations.keys())) * 5:
                print('OH SNAP MAX SCORE')
                break

            if len(lobby_obj.deck.cards) == 0:
                final_round += 1

                if final_round == len(lobby_obj.players) + 1:
                    print('OUT OF CARDS SON')
                    break

            lobby_obj.turn_number += 1

        lobby_obj.end_game()

running_server = ChatServer()
