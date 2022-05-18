from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

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
        return '<Lixeira %d>' % self.id


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
    res = {}
    for lixeira in lixeiras:
        res[lixeira.id] = {
            'localizacao': lixeira.localizacao,
            'capacidade': str(lixeira.capacidade),
        }
    return jsonify(res)


app.run(host='0.0.0.0', port=8080)
