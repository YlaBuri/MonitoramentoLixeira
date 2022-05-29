import json
import os

from flask import Flask, request, url_for, redirect, render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

file_path = os.path.abspath(os.getcwd()) + "\database.db"

app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(50), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


class Lixeira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localizacao = db.Column(db.String(80), nullable=False)
    capacidade = db.Column(db.String(120), nullable=False)
    aberta = db.Column(db.Boolean, nullable=False)

    def __init__(self, localizacao, capacidade, aberta):
        self.localizacao = localizacao
        self.capacidade = capacidade
        self.aberta = aberta

    def __repr__(self):
        return 'lixeira'

    def convert(self):
        return Lixeira(self.localizacao, self.capacidade)

    def dump(self):
        return dict(lixeira={'id': self.id, 'localizacao': self.localizacao, 'capacidade': self.capacidade})

    def to_dict(self):
        return {"id": self.id, "localizacao": self.localizacao, "capacidade": self.capacidade}


db.create_all()

# session = Session()
# lixeira = Lixeira(localizacao='Banheiro feminino', capacidade='Cheia', aberta=True)
# lixeira2 = Lixeira(localizacao='Banheiro masculino', capacidade='Vazia', aberta=False)
# user1 = Usuario("Yla", "yla@email.com", "123")
# user2 = Usuario("Joaldo", "joaldo@email.com", "123")
# db.session.add(lixeira)
# db.session.add(lixeira2)
# db.session.add(user1)
# db.session.add(user2)
# db.session.commit()


@app.route('/', )
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get("email_login")
        senha = request.form.get("senha_login")

        user = Usuario.query.filter_by(email=email, senha=senha).first()
        if user:
            lixeiras = Lixeira.query.all()
            return render_template('index.html', lixeiras=lixeiras)
        else:
            return render_template('login.html')


@app.route('/lixeiras', methods=['GET'])
def getLixeira():
    lixeiras = Lixeira.query.all()
    return render_template('index.html', lixeiras=lixeiras)


@app.route('/lixeiras', methods=['POST'])
def salvar():
    lixeira = {"localizacao": request.json['localizacao'],
               "capacidade": request.json['capacidade'],
               "aberta": request.json['aberta']}
    db.session.add(Lixeira(localizacao=lixeira["localizacao"], capacidade=lixeira["capacidade"], aberta=lixeira["aberta"]))
    db.session.commit()
    return jsonify(lixeira)


# @app.route('/capacidadeLixeiras/<int:id>', methods=['GET', 'POST'])
# def editarEstado(id):
#     lixeira = Lixeira.query.filter_by(id=id).first()
#     if request.method == 'POST':
#         l = { "capacidade": request.json['capacidade']}
#         lixeira.capacidade = l["capacidade"]
#         db.session.commit()
#         return jsonify(l)
#
#
# @app.route('/estadoLixeiras/<int:id>', methods=['GET', 'POST'])
# def editarCapacidade(id):
#     lixeira = Lixeira.query.filter_by(id=id).first()
#     if request.method == 'POST':
#         l = { "aberta": request.json['aberta']}
#         lixeira.aberta = l["aberta"]
#         db.session.commit()
#         return jsonify(l)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editarCapacidade(id):
    lixeira = Lixeira.query.filter_by(id=id).first()
    if request.method == 'POST':
        l = {"capacidade": request.json['capacidade'],
             "aberta": request.json['aberta']}
        lixeira.capacidade = l["capacidade"]
        lixeira.aberta = l["aberta"]
        db.session.commit()
        return jsonify(l)


app.run(host='0.0.0.0', port=8080)
