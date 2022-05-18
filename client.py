import socket


HOST = "localhost"
PORT = 8080
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino = (HOST, PORT)
tcp.connect(destino)


try:
    while True:

        mensagem = input('Digite a mensagem: ')
        if mensagem != "":
            tcp.send(mensagem.encode('utf-8'))
        else:
            break;
except KeyboardInterrupt:
    print("Cliente saiu")

tcp.close()
