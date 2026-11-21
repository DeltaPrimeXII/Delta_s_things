
import pyglet
import socket
import pickle
import threading

from time import time, sleep

from enum import Enum
from game import Board
#==================================================
class Text:
    def __init__(self, text, x=0, y=0, color=(255,255,255,255)):
        self.text = text
        self.x = x
        self.y = y
        self.color = color

    def render(self):
        pyglet.text.Label(self.text, self.x, self.y, color=self.color, font_size=32).draw()
#----------
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
        pyglet.text.Label(self.name, self.x, self.y, color=(0,0,0,255), font_size=32).draw()

    def is_clicked(self, x, y) -> bool:
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def update_coord(self, x, y):
        self.x = x
        self.y = y
#==================================================
class State(Enum):
    HOME = 0
    HOST = 1
    JOIN = 2
    CHESS = 3
    WAITING = 4
#----------
dico_ui = {
    State.HOME: [Button("join", 0, 0, 200, 100),
                 Button("host", 0, 200, 200, 100),
                 Button("test", 0, 400, 200, 100),],

    State.HOST: [Button("home", 0, 0, 200, 100),
                 Button("chess", 0, 200, 200, 100),],

    State.JOIN: [Button("home", 0, 0, 200, 100),
                 Button("chess", 0, 200, 200, 100),],

    State.CHESS: [Button("home", 0, 700, 200, 100),],

    State.WAITING: [Text("waiting for connection", 300, 300),],
    }

#----------
class App:
    def __init__(self, w, h):
        self.state = State.HOME
        self.ui = dico_ui[self.state]
        self.after_wait = State.HOME
        self.game = None
        self.data = None
        self.width = w
        self.height = h
        self.lock = threading.Lock()

    def main(self):
        for ui in self.ui:
            ui.render()
        if self.state == State.CHESS and self.game:
            self.lock.acquire()#lock
            self.game.render()
            self.lock.release()#unlock

    def clicked(self, x, y, button, modifiers) -> None:
        print("app c")
        for ui in self.ui:
            if hasattr(ui, "is_clicked") and ui.is_clicked(x, y):
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
                            threading.Thread(target=self.host_game, args=("192.168.42.27",), daemon=True).start()
                        else:
                            self.game = Board(1)
                            threading.Thread(target=self.join_game, args=("192.168.42.27",), daemon=True).start()
                        self.change_state(State.WAITING)
                        self.after_wait = State.CHESS
                        return
                    case _:
                        return
        if self.state == State.CHESS:
            print("board c")
            if self.game:
                self.game.clicked(x, y)

    def change_state(self, state):
        self.state = state
        self.ui = dico_ui[self.state]
    
    def update_size(self, w, h):
        self.width = w
        self.height = h






    def host_game(self, host, port=8080):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)
        client, addr = server.accept()

        threading.Thread(target=self.handle_connection, args=(client,), daemon=True).start()
        server.close()
    

    def join_game(self, host, port=8080):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        threading.Thread(target=self.handle_connection, args=(client,), daemon=True).start()
    

    def handle_connection(self, client):
        self.change_state(self.after_wait)
        self.after_wait = State.HOST
        while True:
            sleep(0.5)
            try:
                if self.game.turn_played:
                    print("have just played")
                    self.game.turn_played = False
                    client.send(pickle.dumps(self.game.last_move))

                elif (self.data is None) and (self.game.turn % 2 != self.game.player):
                    print("waiting for my turn")
                    print("turn: ", self.game.turn, "   player color:", self.game.player)
                    self.data = pickle.loads(client.recv(1024))
                    print(self.data)
            except socket.error as e:
                print(f"SOCKET ERROR: {e}")
                break

            if self.data:
                print("playing the turn")
                self.lock.acquire()#lock
                self.game.play(1-self.game.player, self.game[self.data[0].x][self.data[0].y], self.data[1])
                self.data = None
                self.lock.release()#unlock