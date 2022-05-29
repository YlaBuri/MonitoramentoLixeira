import json
from urllib import request, parse
import time

def xor_int_str(val, str):
    return val ^ int(str, 10)


def swap(a, b):
    t = S[a]
    S[a] = S[b]
    S[b] = t


def rc4(key, data):
    # KSA
    j = 0
    for i in range(0, 256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        swap(S[i], S[j])

    # PRGA
    i = j = 0
    for k in range(0, len(data)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        swap(S[i], S[j])

        val = ord(data[k]) ^ S[(S[i] + S[j]) % 256]
        has.append(chr(val))


while True:
    skey = "Topesp"
    S = [i for i in range(0, 256)]
    has = []
    mensagem_crip = input()
    rc4(skey, mensagem_crip)
    mensagem_descrip = has
    time.sleep(5)
    id = "".join(mensagem_descrip[0:2])
    mensagemCapacidade = "".join(mensagem_descrip[2:4])
    mensagemEstado = "".join(mensagem_descrip[4:])

    print(mensagemEstado)
    print(mensagemCapacidade)
    alterarEstado = False
    alterarCapacidade = False


    if mensagemCapacidade == '01':
        capacidade = "Vazia"

    elif mensagemCapacidade == '02':
        capacidade = "Meio Cheio"

    elif mensagemCapacidade == '03':
        capacidade = "Cheio"



    if mensagemEstado == '04':
        aberta = True

    elif mensagemEstado == '05':
        aberta = False




    data = {"capacidade": capacidade, "aberta": aberta}
    encoded_data = json.dumps(data).encode()
    pathRequest = 'http://127.0.0.1:8080/editar/' + str(int(id))
    req = request.Request(pathRequest, data=encoded_data)
    req.add_header('Content-Type', 'application/json')
    response = request.urlopen(req)
    text = response.read()
    print(json.loads(text.decode('utf-8')))


