from flask import Flask, render_template
from utils import db, lm
from flask_migrate import Migrate
from controllers.usuarios import bp_usuarios
from controllers.pizzas import bp_pizzas
from controllers.pedidos import bp_pedidos
from flask_login import current_user
from flask import render_template, redirect, flash

app = Flask(__name__)

conexao = "sqlite:///meubanco.sqlite"

app.config['SECRET_KEY'] = 'minha-chave'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False
app.register_blueprint(bp_usuarios, url_prefix='/usuarios')
app.register_blueprint(bp_pizzas, url_prefix='/pizzas')
app.register_blueprint(bp_pedidos, url_prefix='/pedidos')

db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
  if current_user.is_authenticated:
    return render_template('dashboard.html')
  else:
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sqlite')
def sqlite():
    return render_template('sqlite.html')

@app.errorhandler(401)
def acesso_negado(e):
  #flash('Permissão negada')
  #return redirect('/login')
  return render_template('acesso_negado.html'), 401


app.run(host='0.0.0.0', port=81)

#def login_user(user):
#  current_user = user

#no terminal, digite
#$ export FLASK_APP=main:app
