from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import User, Base, engine, Cliente, Venda
from sqlalchemy.orm import sessionmaker
from main import app, session
from sqlalchemy.exc import IntegrityError
from flask_login import login_required

@app.route('/cliente/list', methods=['GET','POST'])
@login_required
def list_clientes():
    filtro = Cliente(nome='', cpf='')
    if request.method == 'GET':
        clientes = session.query(Cliente).all()

    if request.method == 'POST':
        cpf = request.form['cpf']
        nome = request.form['nome']
        filtro = Cliente(nome=nome, cpf=cpf)
        clientes = session.query(Cliente).filter(Cliente.nome.like(f'%{nome}%'), Cliente.cpf.like(f'%{cpf}%')).all()
    return render_template('clientes/list_clientes.html', clientes=clientes, filtro=filtro)

@app.route('/cliente/new', methods=['GET'])
@login_required
def new_cliente():
    return render_template('clientes/new_clientes.html')

@app.route('/cliente/save', methods=['POST'])
@login_required
def save_cliente():
    try:
       
        id = request.form['id']
        if (id):
            cliente = session.query(Cliente).filter_by(id=id).first()
            cliente.nome = request.form['nome']
            cliente.cpf = request.form['cpf']
            cliente.endereco = request.form['endereco']
            cliente.telefone = request.form['telefone']
            cliente.email = request.form['email']
            session.commit()
            msg= "Cliente atualizado com sucesso!"
            return redirect(url_for('list_clientes', mesg=msg))
        else:
            nome = request.form['nome']
            cpf = request.form['cpf']
            endereco = request.form['endereco']
            telefone = request.form['telefone']
            email = request.form['email']
            cliente = Cliente(nome=nome, cpf=cpf, endereco=endereco, telefone=telefone, email=email)
            session.add(cliente)
            session.commit()
            msg= "Cliente salvo com sucesso!"
    except IntegrityError as e:
        session.rollback()
        msg= f"Erro ao salvar o cliente: {str(e)}"

    return redirect(url_for('list_clientes', mesg=msg))

@app.route('/cliente/delete/<int:id>', methods=['GET'])
@login_required
def delete_cliente(id):
    cliente = session.query(Cliente).filter_by(id=id).first()
    if not cliente:
        msg= "Cliente não encontrado"
        return redirect(url_for('list_clientes',mesg=msg))
    try:
        session.delete(cliente)
        session.commit()
        msg= "Cliente deletado com sucesso!"
    except IntegrityError as e:
        session.rollback()
        msg= f"Erro ao deletar o cliente: {str(e)}"
    return redirect(url_for('list_clientes', mesg=msg)) 


@app.route('/cliente/edit/<int:id>', methods=['GET'])
@login_required
def edit_cliente(id):
    cliente = session.query(Cliente).filter_by(id=id).first()
    if not cliente:
        msg= "Cliente não encontrado"
        return redirect(url_for('list_clientes',mesg=msg))
    return render_template('clientes/new_clientes.html', cliente=cliente)