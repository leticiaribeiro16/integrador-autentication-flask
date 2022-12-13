from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for
from utils import db
from models import Pedido, Usuario, Pizza
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user

bp_pedidos = Blueprint("pedidos", __name__, template_folder="templates")

@bp_pedidos.route('/create', defaults={'id':0}, methods=['GET', 'POST'])
@bp_pedidos.route('/create/<int:id>', methods=['GET', 'POST'])
@login_required
def create(id):
  usuarios = ''
  if request.method=='GET':
    if id == 0:
      pizzas = Pizza.query.all()
      usuarios = Usuario.query.all()
    else:
      pizzas = Pizza.query.filter_by(id = id)
    return render_template('pedidos_create.html', pizzas = pizzas, usuarios = usuarios)

  if request.method=='POST':
    usuario_id = current_user.id
    pizza_id = request.form.get('pizza_id')
    data = datetime.today()
    p = Pedido(usuario_id, pizza_id, data)
    db.session.add(p)
    db.session.commit()
    flash('Dados cadastrados com sucesso!', 'success')
    return redirect(url_for('.meuspedidos'))

@bp_pedidos.route('/recovery')
def recovery():
 
  pedidos = Pedido.query.all()
  return render_template('pedidos_recovery.html', pedidos = pedidos)

@bp_pedidos.route('/meuspedidos')
def meuspedidos():
  pedidos = Pedido.query.filter_by(usuario_id=current_user.id).all()
  return render_template('pedidos_recovery.html', pedidos = pedidos)

@bp_pedidos.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

  p = Pedido.query.get(id)
  pizzas = Pizza.query.all()
  usuarios = Usuario.query.all()
 
  if request.method=='GET':
    return render_template('pedidos_update.html', p = p, pizzas=pizzas, usuarios=usuarios)

  if request.method=='POST':
    p.pizza_id = request.form.get('pizza_id')
    db.session.add(p)
    db.session.commit()
    flash('Dados atualizados com sucesso!', 'success')
    return redirect(url_for('.meuspedidos'))

@bp_pedidos.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

  if not current_user.admin:
    flash("Acesso não permitido", "warning")
    return redirect(url_for('.meuspedidos'))
 
  p = Pedido.query.get(id)
  if request.method=='GET':
    return render_template('pedidos_delete.html', p = p)

  if request.method=='POST':
    db.session.delete(p)
    db.session.commit()
    flash('Dados excluídos com sucesso!', 'success')
    return redirect(url_for('.meuspedidos'))