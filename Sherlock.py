import pygame as pg
import random
import socket as sc
import pickle
pg.font.init()
pg.init()

screenInfo = pg.display.Info()
width = screenInfo.current_w
height = screenInfo.current_h

win = pg.display.set_mode((width, height))
pg.display.set_caption("Client")


class Game:
    def __init__(self, id):
        self.id = id
        self.ready = False

        self.nbr_p = 0
        self.player_active = None

        self.deck = []
        self.played_cards = []
        self.cards_returned = 0
        self.cut_wire = 0

        self.roles = []
        self.winner = ""
        self.init = False

        self.round = 0
        self.nextRound = False

    def connected(self):
        return self.ready

    def give_role(self):
        self.roles.append("M")
        self.roles.append("M")
        self.roles.append("S")
        self.roles.append("S")
        self.roles.append("S")

        if self.nbr_p >= 6:
            self.roles.append("S")

        if self.nbr_p >= 7:
            self.roles.append("M")
            self.roles.append("S")

        random.shuffle(self.roles)

        if self.nbr_p == 4 or self.nbr_p == 7:
            self.roles.pop(0)

        self.player_active = random.randint(1, self.nbr_p)

    def init_cards(self):
        if not self.init:
            self.deck.append(2)  # 2 = bombe
            for i in range(self.nbr_p):
                self.deck.append(1)  # 1 = fil désamorçable
            for i in range(0, ((self.nbr_p * 5) - (self.nbr_p + 1))):
                self.deck.append(0)  # 0 = fil sécurisé
            self.init = True

    def shuffle(self):
        random.shuffle(self.deck)

    def play(self, p, id):
        if (p-1) != int(id)//(5-self.round) and (not int(id) in self.played_cards) and (self.cards_returned < self.nbr_p):
            self.player_active = (int(id)//(5-self.round))+1
            self.played_cards.append(int(id))
            self.cards_returned += 1
            if self.deck[int(id)] == 2:
                self.winner = "M"
            elif self.deck[int(id)] == 1:
                self.cut_wire += 1
                if self.cut_wire == self.nbr_p:
                    self.winner = "S"

    def next_round(self):
        if self.nbr_p == self.cards_returned and self.winner == "":
            self.round += 1
            if self.round == 4:
                self.winner = "M"
            else:
                iteration = 0
                self.played_cards.sort()
                for i in self.played_cards:
                    temp = self.deck.pop(i-iteration)
                    iteration += 1
                self.cards_returned = 0
                self.played_cards = []
                self.shuffle()

    def end_round(self):
        if self.nbr_p == self.cards_returned and self.winner == "":
            return True
        else:
            return False

    def reset(self):
        self.init = False

        self.deck = []
        self.played_cards = []
        self.cards_returned = 0
        self.cut_wire = 0

        self.roles = []
        self.winner = ""
        self.init = False

        self.round = 0
        self.nextRound = False


class Network:
    def __init__(self):
        self.client = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.server = "83.202.30.83"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        self.client.send(str.encode(data))

        return pickle.loads(self.client.recv(2048))

    def disconnect(self):
        self.client.close()


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont("comicsans", 40)
        text = font.render(self.text, True, (0, 0, 0))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            pg.time.delay(1000)
            return True
        else:
            return False


class Card:
    def __init__(self, text, x, y, color, id):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.id = str(id)

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont("comicsans", 40)
        text = font.render(self.text, True, (0, 0, 0))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            pg.time.delay(1000)
            return True
        else:
            return False


def show(cards):
    win.fill((128, 128, 128))
    font = pg.font.SysFont("comicsans", 60)
    text = ""
    for i in range(len(cards)):
        if cards[i] == 0:
            text = "Safe"
        if cards[i] == 1:
            text = "Cut"
        if cards[i] == 2:
            text = "Bomb"
        text = font.render(text, True, (0, 0, 0))
        win.blit(text, (((width/(len(cards)+1))*(i+1)) - text.get_width()/2, height/2 - text.get_height()/2))
    pg.display.update()
    pg.time.delay(5000)


def end(team):
    win.fill((128, 128, 128))
    font = pg.font.SysFont("comicsans", 100)
    text = ""
    if team == "S":
        text = font.render("Sherlock have won the game", True, (0, 0, 0))
    elif team == "M":
        text = font.render("Moriarty have won the game", True, (0, 0, 0))
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    pg.display.update()
    pg.time.delay(5000)


def redraw_window(win, p, game, color_list, got_role, got_cards, deck):
    global btns

    win.fill((128, 128, 128))
    btns = []

    if not(game.connected()):
        font = pg.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", True, (255, 0, 0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

        font = pg.font.SysFont("comicsans", 30)
        text = font.render("{}/8".format(game.nbr_p), True, (0, 0, 0))
        win.blit(text, ((width/30)*28, height/30))

        btn_quit.draw(win)

        if p == 1 and game.nbr_p >= 4:
            btn_start.draw(win)

    elif got_role and got_cards:
        font = pg.font.SysFont("comicsans", 60)
        for i in range(0, game.nbr_p):
            # Show roles
            text = font.render(str(i+1), True, (color_list[i]))
            win.blit(text, ((i+1) * round(width/(game.nbr_p+1)) - text.get_width()/2,
                            round((height/7) * 6) - text.get_height()/2))
            if i+1 == game.player_active:
                pg.draw.circle(win, (0, 0, 0),
                               ((i+1) * round(width/(game.nbr_p+1)),
                                round((height/7) * 6)),
                               round(60 * 0.6), 3)

            # Show cards
            for k in range(i * (5 - game.round), (i+1) * (5 - game.round)):
                if k in game.played_cards and game.winner == "":
                    if deck[k] == 0:
                        text = "Safe"
                    elif deck[k] == 1:
                        text = "Cut"
                    else:
                        text = "Bomb"
                else:
                    text = "Wire"
                btn = Card(text,
                           (i+1) * round(width/(game.nbr_p+1)) - 75,
                           (k + 1 - (i * (5 - game.round))) * round((height / 7)),
                           (139, 69, 19), k)
                btns.append(btn)
                btn.draw(win)

        if game.end_round() and p == 1:
            btn_next_round.draw(win)

    pg.display.update()


btn_next_round = Button("Next Round", width/30, height/30, (255, 0, 0))
btn_start = Button("Start Game", width/2 - 75, height/1.5, (255, 0, 0))
btn_quit = Button("Quit Game", width/2 - 75, height/1.2, (255, 0, 0))
btns = []


def main():
    run = True
    clock = pg.time.Clock()
    n = Network()
    player = int(n.getP())
    got_role = False
    got_cards = False
    color_list = []
    deck = []
    round_ = -1
    game = None

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't find the game:", game)
            break

        if game.winner != "":
            end(game.winner)
            got_role = False
            got_cards = False
            color_list = []
            deck = []
            round_ = -1
            if player == 1:
                n.send("reset")

        if game.round != round_ and got_role:
            got_cards = False

        # Initialise la partie
        if game.connected() and not game.init:
            try:
                game = n.send("init")
            except:
                run = False
                print("Couldn't get game")
                break

        # Récupère role et cartes
        elif game.init and not got_role:
            for i in range(0, len(game.roles)):
                if i+1 == player:
                    if game.roles[i] == "M":
                        color_list.append((255, 0, 0))
                    else:
                        color_list.append((0, 0, 255))
                else:
                    color_list.append((0, 0, 0))
            got_role = True

        elif game.init and got_role and not got_cards:
            redraw_window(win, player, game, color_list, got_role, True, deck)
            pg.display.update()
            deck = game.deck
            cards = game.deck[(player - 1) * (5 - game.round):(player * (5 - game.round))]
            random.shuffle(cards)
            show(cards)
            round_ += 1
            got_cards = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if btn_start.click(pos):
                    if 8 >= game.nbr_p >= 4:
                        n.send("start")
                if btn_next_round.click(pos):
                    if player == 1:
                        n.send("nextRound")
                if btn_quit.click(pos):
                    n.disconnect()
                for btn in btns:
                    if btn.click(pos) and game.init and got_role and got_cards and player == game.player_active:
                        n.send(btn.id)

        redraw_window(win, player, game, color_list, got_role, got_cards, deck)


def menu_screen(win):
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pg.font.SysFont("comicsans", 60)
        text = font.render("Click to play!", True, (255, 0, 0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                run = False
    main()


while True:
    menu_screen(win)