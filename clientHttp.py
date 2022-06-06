import json

from urllib import request, parse
import time



while True:
    mensagem_crip = input()
    time.sleep(2)

    data = {"mensagem_crip": mensagem_crip}

    encoded_data = json.dumps(data).encode()
    pathRequest = 'http://127.0.0.1:8080/editar'
    req = request.Request(pathRequest, data=encoded_data)
    req.add_header('Content-Type', 'application/json')

    response = request.urlopen(req)
    text = response.read()
    print(encoded_data)
    print(json.loads(text.decode('utf-8')))


