from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import User, Base, engine, Cliente, Venda
from sqlalchemy.orm import sessionmaker
from main import app, session


def consulta_banco(username, password):
    user =  session.query(User).filter_by(username=username, password=password).first()
    if not user:
        return False
    return True

@app.route('/user/create', methods=['GET'])
def create_user():
    return render_template('create_user.html')
 
@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = session.query(User).filter_by(id=id).first()
    if not user:
        return "User not found", 404
    return user.to_dict(), 200

@app.route('/user/delete/<int:id>', methods=['GET'])
def delete_user_by_id(id):
    user = session.query(User).filter_by(id=id).first()
    if not user:
        return "User not found", 404
    session.delete(user)
    return "Usuário deletado com sucesso!", 204

@app.route('/user/all', methods=['GET'])
def get_all_user():
    users = session.query(User).all()
    if not users:
        return "User not found", 404
    return [user.to_dict() for user in users], 200

@app.route('/user/save', methods=['POST'])
def saveForm():
    user = request.form['username']
    password = request.form['password']
    msgReponse = ""
    if consulta_banco( user, password ):
        msgReponse = "Login Successful"
    else:
        msgReponse = "Login Failed"
    
    return render_template('form.html', msg=msgReponse  )

@app.route('/user/create', methods=['POST'])
def create_user_do():
    username = request.form['username']
    password = request.form['password']
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    return redirect(url_for('form'))