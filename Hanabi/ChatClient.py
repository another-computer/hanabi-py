import sys
import socket
import select
import threading
from PyQt5 import QtWidgets
from ChatUILayout import Ui_MainWindow


class ClientUI(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(ClientUI, self).__init__(parent)

        self.setupUi(self)

        self.actionConnect.triggered.connect(self.connection_prompt)

        self.input_box.returnPressed.connect(self.send_message)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2)

        self.connection_thread = None

        self.socket_list = None

    def connection_prompt(self):
        input_connection, confirmation = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
                                                                        'Enter the desired address and port')

        if confirmation:
            self.connect_host(input_connection)

    def connect_host(self, desired_connection):

        desired_connection = desired_connection.split()

        address = (desired_connection[0], int(desired_connection[1]))

        # connect to remote host
        try:
            self.client.connect(address)

            self.chat_log.addItem('[Server] Connected to remote host. You can start sending messages')
            self.address_label.setText('Connected on {} port {}'.format(desired_connection[0], desired_connection[1]))

            self.connection_thread = threading.Thread(target=self.active_connection)
            self.connection_thread.setDaemon(True)
            self.connection_thread.start()

        except:
            print('Unable to connect')
            sys.exit()

    def scroll_position_check(self):
        if self.chat_log.verticalScrollBar().value() == self.chat_log.verticalScrollBar().maximum():
            self.chat_log.scrollToBottom()

    def active_connection(self):

        while True:
            self.socket_list = [self.client]

            # Get the list sockets which are readable
            ready_to_read, ready_to_write, in_error = select.select(self.socket_list, [], [])

            for sock in ready_to_read:
                if sock == self.client:
                    # incoming message from remote server, sock
                    data = sock.recv(4096)

                    if not data:
                        print('\nDisconnected from chat server')
                        sys.exit()

                    else:
                        # print data
                        self.chat_log.addItem(data.decode())

                        self.scroll_position_check()

                else:
                    print('WHY IS THIS HAPPENING')
                    # user entered a message
                    msg = sys.stdin.readline()
                    self.client.send(msg)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

    def send_message(self):
        message = self.input_box.text()

        if len(message) == 0:
            pass

        elif message[0] == '/':
            self.client.send(message.encode())
            self.chat_log.scrollToBottom()

        else:
            self.chat_log.addItem('[Me] {}'.format(message))
            self.client.send(message.encode())

            self.scroll_position_check()

        self.input_box.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = ClientUI()
    form.show()
    app.exec_()
