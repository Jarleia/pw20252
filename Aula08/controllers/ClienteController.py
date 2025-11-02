from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import User, Base, engine, Cliente, Venda
from sqlalchemy.orm import sessionmaker
from main import app, session
from sqlalchemy.exc import IntegrityError


@app.route('/cliente/create', methods=['GET'])
def create_cliente():
    return render_template('create_cliente.html')