import random


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
        if not self.roles:
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
            print("active:", self.player_active)

    def init_cards(self):
        if not self.init and self.deck == []:
            self.deck.append(2)  # 2 = bombe
            for i in range(self.nbr_p):
                self.deck.append(1)  # 1 = fil désamorçable
            for i in range(0, ((self.nbr_p * 5) - (self.nbr_p + 1))):
                self.deck.append(0)  # 0 = fil sécurisé
            print("Init:", self.deck)
            self.init = True

    def shuffle(self):
        random.shuffle(self.deck)

    def play(self, p, id):
        print("play:", self.played_cards)
        if (p-1) != int(id)//(5-self.round) and (not int(id) in self.played_cards) and (self.cards_returned < self.nbr_p):
            self.player_active = (int(id)//(5-self.round))+1
            print("active:", self.player_active)
            self.played_cards.append(int(id))
            self.cards_returned += 1
            print("play:", self.played_cards)
            print("play:", id)
            if self.deck[int(id)] == 2:
                self.winner = "M"
            elif self.deck[int(id)] == 1:
                self.cut_wire += 1
                if self.cut_wire == self.nbr_p:
                    self.winner = "S"
        print("played")

    def next_round(self):
        print("Next round started")
        print(self.played_cards)
        if self.nbr_p == self.cards_returned and self.winner == "":
            self.round += 1
            if self.round == 4:
                self.winner = "M"
            else:
                iteration = 0
                self.played_cards.sort()
                for i in self.played_cards:
                    print(i)
                    temp = self.deck.pop(i-iteration)
                    iteration += 1
                print(self.deck)
                self.cards_returned = 0
                self.played_cards = []
                self.shuffle()
                print("Next round: ", self.round)

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


