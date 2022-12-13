from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for
from utils import db
from models import Pizza
from flask_login import login_user, logout_user, login_required, current_user

bp_pizzas = Blueprint("pizzas", __name__, template_folder="templates")

@bp_pizzas.route('/create', methods=['GET', 'POST'])
def create():
  if request.method=='GET':
    return render_template('pizzas_create.html')

  if request.method=='POST':
    sabor = request.form.get('sabor')
    imagem = request.form.get('imagem')
    ingredientes = request.form.get('ingredientes')
    preco = request.form.get('preco')
    p = Pizza(sabor, imagem, ingredientes, preco)
    db.session.add(p)
    db.session.commit()
    flash('Dados cadastrados com sucesso!', 'success')
    return redirect(url_for('.recovery'))

@bp_pizzas.route('/recovery')
def recovery():
 
  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
 
  pizzas = Pizza.query.all()
  return render_template('pizzas_recovery.html', pizzas = pizzas)


@bp_pizzas.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
 
  p = Pizza.query.get(id)
 
  if request.method=='GET':
    return render_template('pizzas_update.html', p = p)

  if request.method=='POST':
    sabor = request.form.get('sabor')
    imagem = request.form.get('imagem')
    ingredientes = request.form.get('ingredientes')
    preco = request.form.get('preco')
    p.sabor = sabor
    p.imagem = imagem
    p.ingredientes = ingredientes
    p.preco = preco
    db.session.add(p)
    db.session.commit()
    flash('Dados atualizados com sucesso!','success')
    return redirect(url_for('.recovery'))

@bp_pizzas.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
 
  p = Pizza.query.get(id)
  if request.method=='GET':
    return render_template('pizzas_delete.html', p = p)

  if request.method=='POST':
    db.session.delete(p)
    db.session.commit()
    flash('Dados excluídos com sucesso!', 'success')
    return redirect(url_for('.recovery'))

@bp_pizzas.route('/cardapio')
def cardapio():
  pizzas = Pizza.query.all()
  return render_template('pizzas_cardapio.html', pizzas = pizzas)

@bp_pizzas.route('/pedirpizza')
def pedirpizza():
  pizzas = Pizza.query.all()
  return render_template('pedidos_create.html')