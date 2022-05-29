import json
from urllib import request, parse

data = { "localizacao": "banheiro2", "capacidade": "cheio"}

encoded_data = json.dumps(data).encode()

req = request.Request('http://127.0.0.1:8080/lixeiras', data=encoded_data)
req.add_header('Content-Type', 'application/json')
response = request.urlopen(req)

text = response.read()

print(json.loads(text.decode('utf-8')))