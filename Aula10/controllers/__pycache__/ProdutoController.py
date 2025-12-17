from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import User, Base, engine, Cliente, Venda
from sqlalchemy.orm import sessionmaker
from main import app, session
from sqlalchemy.exc import IntegrityError
from flask_login import login_required

@app.route('/produto/list', methods=['GET','POST'])
@login_required
def list_produtos():
    filtro = Produto(nome='', preco='')
    if request.method == 'GET':
        produtos = session.query(Produto).all()

    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        filtro = Produto(nome=nome, preco=preco)
        produtos = session.query(Produto).filter(Produto.nome.like(f'%{nome}%'), Produto.preco.like(f'%{preco}%')).all()
    return render_template('produtos/list_produtos.html', produtos=produtos, filtro=filtro)

@app.route('/produto/new', methods=['GET'])
@login_required
def new_produto():
    return render_template('produtos/new_produtos.html')

@app.route('/produto/save', methods=['POST'])
@login_required
def save_produto():
    try:
       
        id = request.form['id']
        if (id):
            produto = session.query(Produto).filter_by(id=id).first()
            produto.nome = request.form['nome']
            produto.preco = request.form['preco']
            produto.endereco = request.form['endereco']
            produto.telefone = request.form['telefone']
            produto.email = request.form['email']
            session.commit()
            msg= "Produto atualizado com sucesso!"
            return redirect(url_for('list_produtos', mesg=msg))
        else:
            nome = request.form['nome']
            preco = request.form['preco']
            endereco = request.form['endereco']
            telefone = request.form['telefone']
            email = request.form['email']
            produto = Produto(nome=nome, preco=preco, endereco=endereco, telefone=telefone, email=email)
            session.add(produto)
            session.commit()
            msg= "Produto salvo com sucesso!"
    except IntegrityError as e:
        session.rollback()
        msg= f"Erro ao salvar o produto: {str(e)}"

    return redirect(url_for('list_produtos', mesg=msg))

@app.route('/produto/delete/<int:id>', methods=['GET'])
@login_required
def delete_produto(id):
    produto = session.query(Produto).filter_by(id=id).first()
    if not produto:
        msg= "Produto não encontrado"
        return redirect(url_for('list_produtos',mesg=msg))
    try:
        session.delete(produto)
        session.commit()
        msg= "Produto deletado com sucesso!"
    except IntegrityError as e:
        session.rollback()
        msg= f"Erro ao deletar o produto: {str(e)}"
    return redirect(url_for('list_produtos', mesg=msg)) 


@app.route('/produto/edit/<int:id>', methods=['GET'])
@login_required
def edit_produto(id):
    produto = session.query(Produto).filter_by(id=id).first()
    if not produto:
        msg= "Produto não encontrado"
        return redirect(url_for('list_produtos',mesg=msg))
    return render_template('produtos/new_produtos.html', produto=produto)