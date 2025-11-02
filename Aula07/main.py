from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import User, Base, engine, Cliente, Venda
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'API para Programação Web II',
    'uiversion': 3
}

Session = sessionmaker(bind=engine)
session = Session()

from flasgger import Swagger
swagger = Swagger(app)


@app.route('/home')
def home():
  
    return "Hello, World!"

@app.route('/cliente/<int:id>', methods=['GET'])
def cliente_view(id):
    cliente = session.query(Cliente).filter_by(id=id).first()
    if not cliente:
        return "Cliente not found", 404
    return cliente.to_dict(), 200

@app.route('/venda/<int:id>', methods=['GET'])
def venda_by_id(id):
    venda = session.query(Venda).filter_by(id=id).first()
    if not venda:
        return "Venda not found", 404
    return venda.to_dict(), 200

@app.route('/')
def form():
    return render_template('form.html')

from controllers.UserController import *
from controllers.ClienteController import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True, port=5001)
