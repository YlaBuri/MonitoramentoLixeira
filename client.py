import socket
import json
import time

m = {"id": 2, "name": "abc"}
data = json.dumps(m)

HOST = "127.0.0.1"
PORT = 5000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino = (HOST, PORT)
tcp.connect(destino)


try:
    while True:

        mensagem = data
        if mensagem != "":
            tcp.send(mensagem.encode('utf-8'))
            time.sleep(5)
        else:
            break;
except KeyboardInterrupt:
    print("Cliente saiu")

tcp.close()
