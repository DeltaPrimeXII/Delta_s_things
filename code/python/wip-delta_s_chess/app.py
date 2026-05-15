
import pyglet
import socket
import pickle
import threading

from time import time

from enum import Enum
from game import Board
#==================================================
class Button:
    def __init__(self, name, x=0, y=0, width=50, height=50):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.color = color

    def render(self):
        pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, color=(255,255,255,255)).draw()
        pyglet.shapes.Rectangle(self.x+5, self.y+5, self.width-10, self.height-10, color=(200,200,200,255)).draw()
        pyglet.text.Label(self.name, self.x, self.y, self.width, self.height, color=(0,0,0,255), font_size=32).draw()

    def is_clicked(self, x, y) -> bool:
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

#==================================================
class State(Enum):
    HOME = 0
    HOST = 1
    JOIN = 2
    CHESS = 3
#----------
dico_ui = {
    State.HOME: [Button("join", 0, 0, 200, 100),
                 Button("host", 0, 200, 200, 100),],

    State.HOST: [Button("home", 0, 0, 200, 100),
                 Button("chess", 0, 200, 200, 100),],

    State.JOIN: [Button("home", 0, 0, 200, 100),
                 Button("chess", 0, 200, 200, 100),],

    State.CHESS: [Button("home", 0, 0, 200, 100),],
    }
#----------
class App:
    def __init__(self):
        self.state = State.HOME
        self.ui = dico_ui[self.state]
        self.game = None
        self.data = None

    def main(self):
        for ui in self.ui:
            ui.render()
        if self.game:
            if self.data:
                self.game = self.data
                self.game.player = 1-self.game.player
                self.data = None
            self.game.render()

    def clicked(self, x, y, button, modifiers) -> None:
        for ui in self.ui:
            if ui.is_clicked(x, y):
                match ui.name:
                    case "home":
                        self.change_state(State.HOME)
                        return
                    case "host":
                        self.change_state(State.HOST)
                        return
                    case "join":
                        self.change_state(State.JOIN)
                        return
                    case "chess":
                        if self.state == State.HOST:
                            self.game = Board(0)
                            self.host_game("192.168.1.129")
                        else:
                            self.game = Board(1)
                            self.join_game("192.168.1.129")
                        self.change_state(State.CHESS)
                        return
                    case _:
                        pass
        if self.state == State.CHESS:
            if self.game:
                self.game.clicked(x, y)

    def change_state(self, state):
        self.state = state
        self.ui = dico_ui[self.state]






    def host_game(self, host, port=8080):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)
        client, addr = server.accept()

        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()
    

    def join_game(self, host, port=8080):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        threading.Thread(target=self.handle_connection, args=(client,)).start()
    

    def handle_connection(self, client):
        # print("color: ", self.game.player)
        # delay = time()
        while True:
            if self.game.turn % 2 == self.game.player:
                # if time() - delay >= 1:
                print("my turn")
                    # delay = time()
                if self.game.turn_played:
                    print("have just played")
                    self.game.turn_played = False
                    client.send(pickle.dumps(self.game))
            elif self.data is None:
                print("waiting for my turn")
                print("turn: ", self.game.turn)
                self.data = pickle.loads(client.recv(2**14))#TODO reduce the quantity of sent informations