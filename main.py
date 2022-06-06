import json
import os
import sqlite3

from flask import Flask, request, url_for, redirect, render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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

    @classmethod
    def find_by_email(cls, email):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        try:
            data = cursor.execute('SELECT * FROM Usuario WHERE email=?', (email,)).fetchone()
            if data:
                return cls(data[1], data[2], data[3])
        finally:
            connection.close()


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
# db.session.add(lixeira)
# db.session.add(lixeira2)
# db.session.commit()

S = [i for i in range(0, 256)]
has = []

def swap(a, b):
    global S
    t = S[a]
    S[a] = S[b]
    S[b] = t


def rc4(key, data):
    global S, has
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

@app.route('/', )
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global S, has
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        S = [i for i in range(0, 256)]
        has = []
        skey = "Topesp"

        email = request.form.get("email_login")
        senha = request.form.get("senha_login")
        rc4(skey, senha)
        senha_crip = "".join(has)

        user = Usuario.query.filter_by(email=email, senha=senha_crip).first()

        # if user and check_password_hash(user.senha, senha):
        #     print('message Password is correct')  # You'll want to return a token that verifies the user in the future
        # return print('error User or password are incorrect')

        if user:
            lixeiras = Lixeira.query.all()
            return render_template('index.html', lixeiras=lixeiras)
        else:
            return render_template('login.html')


@app.route('/cadastrarUsuario', methods=['GET', 'POST'])
def cadastrarUsuario():
    global S, has
    if request.method == 'GET':
        return render_template('cadastrarUsuario.html')
    elif request.method == 'POST':
        S = [i for i in range(0, 256)]
        has = []
        skey = "Topesp"
        nome = request.form.get("nome_cadastro")
        email = request.form.get("email_cadastro")
        senha = request.form.get("senha_cadastro")

        rc4(skey, senha)
        senha_crip = "".join(has)
        usuario = Usuario(nome, email, senha_crip)
        db.session.add(usuario)
        db.session.commit()
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


@app.route('/editar', methods=['GET', 'POST'])
def editarCapacidade():
    global S, has
    S = [i for i in range(0, 256)]
    has = []
    if request.method == 'POST':
        data_crip = {"data": request.json['mensagem_crip']}
        skey = "Topesp"
        rc4(skey, data_crip["data"])
        mensagem_descrip = has
        id = "".join(mensagem_descrip[0:2])
        mensagemCapacidade = "".join(mensagem_descrip[2:4])
        mensagemEstado = "".join(mensagem_descrip[4:6])
        # print(mensagem_descrip)
        # print(id)
        # print(mensagemEstado)
        # print(mensagemCapacidade)

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

        lixeira = Lixeira.query.filter_by(id=int(id)).first()
        lixeira.capacidade = capacidade
        lixeira.aberta = aberta
        db.session.commit()
        return jsonify(lixeira.to_dict())


app.run(host='0.0.0.0', port=8080)
