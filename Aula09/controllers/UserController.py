from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import User, Base, engine, Cliente, Venda
from sqlalchemy.orm import sessionmaker
from main import app, session
from sqlalchemy.exc import IntegrityError
from flasgger import swag_from

def consulta_banco(username, password):
    user =  session.query(User).filter_by(username=username, password=password).count()
    if user==0:
        return False
    return True
    
@app.route('/user/new', methods=['GET'])
def new_user():
    return render_template('/user/new_user.html')

@app.route('/user/create', methods=['GET'])
def create_user():
    users = session.query(User).all()
    return render_template('create_user.html', usuarios=users)

@app.route('/user/search', methods=['POST'])
def search_user():
    
    user = request.form['name']
    email = request.form['email']

    users = session.query(User).filter(User.nome.contains(user), User.username.contains(email)).all()
    return render_template('create_user.html', usuarios=users)
 
@app.route('/user/edit/<int:id>', methods=['GET'])
def editar_user(id):
    user = session.query(User).filter_by(id=id).first()
    if not user:
        msg= "Usuário não encontrado"
        return redirect(url_for('create_user',mesg=msg))
    return render_template('user/new_user.html', user=user)

@app.route('/user/delete/<int:id>', methods=['GET'])
def apagar_user(id):
    user = session.query(User).filter_by(id=id).first()
    msg = "Usuário apagado com sucesso!"
    if not user:
        msg= "Usuário não encontrado"
        return redirect(url_for('create_user',mesg=msg))
    try:
        session.delete(user)
        session.commit()
    except:   
        msg = "Erro ao apagar usuário"
        session.rollback()
    return redirect(url_for('create_user', msg=msg))


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

@app.route('/home', methods=['POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    msgReponse = ""
    if consulta_banco( user, password ):
        msgReponse = "Login Successful"
        return render_template('/home/dashboard.html', msg=msgReponse  )
    else:
        msgReponse = "Login Failed"
    return render_template('form.html', msg=msgReponse  )

@app.route('/user/create', methods=['POST'])
def create_user_do():
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    id = request.form['id']
    if not id:
      new_user = User(username=username, password=password, nome=name)
      session.add(new_user)
      session.commit()
    else:
      user = session.query(User).filter_by(id=id).first()
      if not user:
          msg= "Usuário não encontrado"
          return redirect(url_for('create_user',mesg=msg))
      user.username = username
      user.password = password
      user.nome = name
      session.commit()
    return redirect(url_for('create_user'))


@app.route('/v1/users', methods=['POST'])
def create_r():
    """Example endpoint creating a user
    This is using docstrings for specifications.
    ---
    tags:
      - Users
    summary: Cria um novo usuário
    description: Cria um novo usuário com os dados fornecidos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - name
          properties:
            nome:
              type: string
              description: The product's name.
              default: "Guarana"
            username:
              type: string
              description: The product's name.
              default: "Guarana"
            password:
              type: string
              description: The product's name.
              default: "Guarana"
    definitions:
      User:
        type: object
        properties:
          nome:
            type: string
          username:
            type: string
          password:
            type: string
    responses:
      200:
        description: A user saved 
        schema:
          $ref: '#/definitions/User'
        examples:
            application/json: { "nome": "Guarana", "username": "user1", "password": "pass" }
      400:    
        description: Bad Request
        schema:
          id: Error
          properties:
            error:
              type: string
              description: "Erro de banco de dados"
    """
    try:
        data = request.json  # or data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if (not username) or (not password):
            return {"error": "username and password are required"}, 400
        name = data.get('name')
        new_user = User(username=username, password=password, nome=name)
        session.add(new_user)
        session.commit()
        return new_user.to_dict(), 201
    except IntegrityError as e:
        return {"error": "erro no banco de dados"}, 400  
    except Exception as e:
        return {"error": str(e)}, 400  
    
@app.route('/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    """Example endpoint returning a user by id
    This is using docstrings for specifications.
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        schema:
          id: User
          required:
            - name
          properties:
            nome:
              type: string
              description: The product's name.
              default: "Guarana"
            username:
              type: string
              description: The product's name.
              default: "Guarana"
            password:
              type: string
              description: The product's name.
              default: "Guarana"
    definitions:
      User:
        type: object
        properties:
          nome:
            type: string
          username:
            type: string
          password:
            type: string
    responses:
      200:
        description: A user by id 
        schema:
          $ref: '#/definitions/User'
        examples:
            application/json: { "nome": "Guarana", "username": "user1", "password": "pass" }
      400:    
        description: Bad Request
        schema:
          id: Error
          properties:
            error:
              type: string
              description: "Erro de banco de dados"
    400:    
        description: Bad Request
        schema:
          id: Error
          properties:
            error:
              type: string
              description: "Erro de banco de dados"
    404:
        description: Not Found
        schema:
          id: Error
          properties:
            error:
              type: string
              description: "User not found" 
    """
    try:
        user = session.query(User).filter_by(id=id).first()
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200
    except IntegrityError as e:
        return {"error": "erro no banco de dados"}, 400  
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/v1/users', methods=['GET'])
def get_users():    
    """Example endpoint returning a list 
    of users  This is using docstrings for specifications.
    ---
    tags:
      - Users
    definitions:
      User:
        type: object
        properties:
          nome:
            type: string
          username:
            type: string
          password:
            type: string
    responses:
      200:
        description: A user by id 
        schema:
          $ref: '#/definitions/User'
        examples:
            application/json: [{ "nome": "Guarana", "username": "user1", "password": "pass" }, { "nome": "Coca", "username": "user2", "password": "pass2" }]
      400:    
        description: Bad Request
        schema:
          id: Error
          properties:
            error:
              type: string
              description: "Erro de banco de dados"
    400:    
        description: Bad Request
        schema:
          id: Error
          properties:
            error:
              type: string
              description: "Erro de banco de dados"
    404:
        description: Not Found
        schema:
          id: Error
          properties:
            error:
              type: string
              description: "User not found" 
    """
    try:
        users = session.query(User).all()
        return [user.to_dict() for user in users], 200
    except IntegrityError as e:
        return {"error": "erro no banco de dados"}, 400  
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/v1/users/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Excluir um usuário',
    'description': 'Remove permanentemente um usuário do sistema',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário a ser excluído',
            'example': 1
        }
    ],
    'responses': {
        204: {
            'description': 'Usuário excluído com sucesso',
            'examples': {
                'application/json': {
                    'message': 'User deleted successfully'
                }
            }
        },
        400: {
            'description': 'Erro na requisição ou violação de integridade',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'erro no banco de dados'}
                }
            },
            'examples': {
                'application/json': {
                    'error': 'erro no banco de dados'
                }
            }
        },
        404: {
            'description': 'Usuário não encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'User not found'}
                }
            },
            'examples': {
                'application/json': {
                    'error': 'User not found'
                }
            }
        }
    },
    'produces': ['application/json']
})
def delete_user(id):
    try:
        user = session.query(User).filter_by(id=id).first()
        if not user:
            return {"error": "User not found"}, 404
        session.delete(user)
        session.commit()
        return {"message": "User deleted successfully"}, 204
    except IntegrityError as e:
        return {"error": "erro no banco de dados"}, 400  
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/v1/users/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Atualizar um usuário',
    'description': 'Atualiza os dados de um usuário existente',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário a ser atualizado',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Usuário atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'username': {'type': 'string', 'example': 'joao_silva'},
                    'name': {'type': 'string', 'example': 'João Silva'},
                    # Adicione outras propriedades conforme seu modelo User
                }
            },
            'examples': {
                'application/json': {
                    'id': 1,
                    'username': 'joao_silva',
                    'name': 'João Silva'
                }
            }
        },
        400: {
            'description': 'Erro na requisição ou violação de integridade',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'erro no banco de dados'}
                }
            },
            'examples': {
                'application/json': {
                    'error': 'erro no banco de dados'
                }
            }
        },
        404: {
            'description': 'Usuário não encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'User not found'}
                }
            },
            'examples': {
                'application/json': {
                    'error': 'User not found'
                }
            }
        }
    },
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Nome de usuário único',
                        'example': 'novo_username'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Senha do usuário',
                        'example': 'nova_senha123'
                    },
                    'name': {
                        'type': 'string',
                        'description': 'Nome completo do usuário',
                        'example': 'Novo Nome'
                    }
                },
                'additionalProperties': False
            }
        }
    ]
})
def update_user(id):    
    try:
        user = session.query(User).filter_by(id=id).first()
        if not user:
            return {"error": "User not found"}, 404
        data = request.json  # or data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        if username:
            user.username = username
        if password:
            user.password = password
        if name:
            user.nome = name
        session.commit()
        return user.to_dict(), 200
    except IntegrityError as e:
        return {"error": "erro no banco de dados"}, 400  
    except Exception as e:
        return {"error": str(e)}, 400   

