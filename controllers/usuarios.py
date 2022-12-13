from flask import Blueprint, url_for
from flask import render_template, request, redirect, flash
from models import Usuario
from utils import db, lm
from flask_login import login_user, logout_user, login_required, current_user

bp_usuarios = Blueprint("usuarios", __name__, template_folder="templates")

@bp_usuarios.route('/create', methods=['GET', 'POST'])
@login_required
def create():

  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
 
  if request.method=='GET':
    return render_template('usuarios_create.html')

  if request.method=='POST':
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    csenha = request.form.get('csenha')
    admin = request.form.get('admin')
    u = Usuario(nome, email, senha, eval(admin))
    db.session.add(u)
    db.session.commit()
    flash('Dados cadastrados com sucesso!', 'success')
    return redirect(url_for('.recovery'))

@bp_usuarios.route('/')
@bp_usuarios.route('/recovery')
@login_required
def recovery():
 
  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
 
  usuarios = Usuario.query.all()
  return render_template('usuarios_recovery.html', usuarios=usuarios)


@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
   
  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
 
  u = Usuario.query.get(id)
   
  if request.method=='GET':
    return render_template('usuarios_update.html', u = u)

  if request.method=='POST':
    nome = request.form.get('nome')
    email = request.form.get('email')
    admin = request.form.get('admin')
    u.nome = nome
    u.email = email
    u.admin = eval(admin)
    db.session.add(u)
    db.session.commit()
    flash('Dados atualizados com sucesso!', 'success')
    return redirect(url_for('.recovery'))

@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
 
  u = Usuario.query.get(id)
  if request.method=='GET':
    return render_template('usuarios_delete.html', u = u)

  if request.method=='POST':
    db.session.delete(u)
    db.session.commit()
    flash('Dados excluídos com sucesso!', 'success')
    return redirect(url_for('.recovery'))


@lm.user_loader
def load_user(id):
  usuario = Usuario.query.filter_by(id=id).first()
  return usuario

@bp_usuarios.route('/autenticar', methods=['POST'])
def autenticar():
  email = request.form.get('email')
  senha = request.form.get('senha')
  usuario = Usuario.query.filter_by(email = email).first()

  if usuario and senha == usuario.senha:
    login_user(usuario)
    return redirect('/')
  else:
    flash('Dados incorretos', 'danger')
    return redirect('/login')

@bp_usuarios.route('/update-senha/<int:id>', methods=['GET', 'POST'])
@login_required
def updatesenha(id):
 
  u = Usuario.query.get(id)
  id = current_user.id

  if request.method=='GET':
    return render_template('usuarios_alterarsenha.html', u = u)

  if request.method=='POST':
    senha = request.form.get('senha')
    csenha = request.form.get('csenha')
   
    if senha != csenha:
      flash("Senhas diferentes", "warning")
      return redirect(url_for("usuarios.updatesenha", id=id))
     
    else:
      u.senha= senha
      u.csenha = csenha
    db.session.add(u)
    db.session.commit()
    flash('Dados atualizados com sucesso!', 'success')
    return redirect(url_for('pizzas.cardapio'))


@bp_usuarios.route('/logoff')
def logoff():
  logout_user()
  return redirect('/')