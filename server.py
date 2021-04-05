import socket as sc
from _thread import *
from game import Game
import pickle

server = sc.gethostbyname(sc.gethostname())
port = int(input("Port: "))

s = sc.socket(sc.AF_INET, sc.SOCK_STREAM)  # Défini type de connexion

try:
    s.bind((server, port))  # Connecte au serveur
except sc.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "start":
                        game.ready = True
                        idCount = (gameId + 1) * 8
                    elif data == "init":
                        game.give_role()
                        game.init_cards()
                        game.shuffle()
                    elif data == "reset":
                        game.reset()
                    elif data == "nextRound":
                        game.next_round()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply, pickle.HIGHEST_PROTOCOL))

            else:
                break
        except:
            break

    # Quit game
    print("Lost connection")
    try:
        if not game.ready:
            games[gameId].nbr_p -= 1
            idCount -= 1
            if p == 1:
                try:
                    del games[gameId]
                    idCount -= idCount % 8
                    print("Closing game", gameId)
                except:
                    pass
        elif game.ready:
            try:
                del games[gameId]
                print("Closing game", gameId)
            except:
                pass
            if p == 1:
                idCount -= 8
    except:
        pass
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 1
    gameId = (idCount - 1) // 8

    try:
        while games[gameId].ready:
            idCount += 9 - (idCount % 8)
            print(idCount)
            gameId = (idCount - 1) // 8
    except:
        pass

    if idCount % 8 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game:", gameId)
    else:
        p = games[gameId].nbr_p + 1

    games[gameId].nbr_p = p

    print("ID:", idCount)
    print("P:", p)

    start_new_thread(threaded_client, (conn, p, gameId))
