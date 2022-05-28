from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
import os
import json

from sqlalchemy.orm import Session

file_path = os.path.abspath(os.getcwd()) + "\database.db"

app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

db = SQLAlchemy(app)


class Lixeira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localizacao = db.Column(db.String(80), nullable=False)
    capacidade = db.Column(db.String(120), nullable=False)

    def __init__(self, localizacao, capacidade):
        self.localizacao = localizacao
        self.capacidade = capacidade

    def __repr__(self):
        return 'lixeira'

    def dump(self):
        return dict(lixeira={'id': self.id, 'localizacao': self.localizacao, 'capacidade': self.capacidade})

    def to_dict(self):
        return {"id": self.id, "localizacao": self.localizacao, "capacidade": self.capacidade}


db.create_all()


# session = Session()
# lixeira = Lixeira(localizacao='Banheiro feminino', capacidade='Cheia')
# lixeira2 = Lixeira(localizacao='Banheiro masculino', capacidade='Vazia')
# db.session.add(lixeira)
# db.session.add(lixeira2)
# db.session.commit()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/lixeiras')
def getLixeira():
    lixeiras = Lixeira.query.paginate().items

    json_string = json.dumps([ob.to_dict() for ob in lixeiras])
    json_string = json_string.replace("[", "")
    json_string = json_string.replace("]", "")

    print(type(json_string))
    print(json_string)

    return Response(json_string, mimetype='application/json')




app.run(host='0.0.0.0', port=8080)
