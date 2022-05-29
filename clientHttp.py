import json
from urllib import request, parse



mensagem_descrip = "0104"

id = mensagem_descrip[0:2]
mensagem = mensagem_descrip[2:]
alterarEstado = False
alterarCapacidade = False


if mensagem == "01":
    capacidade = "Vazia"
    alterarCapacidade = True
elif mensagem == "02":
    capacidade = "Meio Cheio"
    alterarCapacidade = True
elif mensagem == "03":
    capacidade = "Cheio"
    alterarCapacidade = True


if mensagem == "04":
    aberta = True
    alterarEstado = True
elif mensagem == "05":
    aberta = False
    alterarEstado = True


if alterarEstado:
    data = {"aberta": aberta}
    encoded_data = json.dumps(data).encode()
    pathRequest = 'http://127.0.0.1:8080/estadoLixeiras/' + str(int(id))
    req = request.Request(pathRequest, data=encoded_data)
    req.add_header('Content-Type', 'application/json')
    response = request.urlopen(req)
    text = response.read()
    print(json.loads(text.decode('utf-8')))
elif alterarCapacidade:
    data = {"capacidade": capacidade}
    encoded_data = json.dumps(data).encode()
    pathRequest = 'http://127.0.0.1:8080/capacidadeLixeiras/' + str(int(id))
    req = request.Request(pathRequest, data=encoded_data)
    req.add_header('Content-Type', 'application/json')
    response = request.urlopen(req)
    text = response.read()
    print(json.loads(text.decode('utf-8')))

