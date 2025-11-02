from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#mysql
engine = create_engine('mysql+pymysql://root:@localhost:3306/pw2', echo=True)

#engine = create_engine('sqlite:///example.db', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,  primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(30), nullable=False)
    nome = Column(String(100), nullable=True)
    def to_dict(self):
        return {
            "id": self.id,
            "userName": self.username,
            "nome": self.nome,
        }

class Produtos(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False)
    descricao = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Float, nullable=False)


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    cpf = Column(String(11), nullable=False)
    nome = Column(String(100 ), nullable=False)
    endereco = Column(String(200), nullable=False)
    telefone = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    vendas = relationship("Venda")
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "endereco": self.endereco,
            "telefone": self.telefone,
            "cpf": self.cpf,
            "vendas": [venda.to_dict() for venda in self.vendas]
        }

class Venda(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    data = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String(1), nullable=False)
    itens = relationship("ItemVenda")
    user = relationship("User")
    cliente = relationship("Cliente")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "user_id": self.user_id,
            "data": self.data,
            "total": self.total,
            "status": self.status,
            "itens": [item.to_dict() for item in self.itens],
            "user": self.user.username if self.user else None,
            "cliente": self.cliente.nome if self.cliente else None
        }   
    
    

class ItemVenda(Base):
    __tablename__ = 'Iten_vendas'
    id = Column(Integer, primary_key=True)
    venda_id = Column(Integer, ForeignKey('vendas.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    qnt = Column(Float, nullable=False)
    preco = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    produto = relationship("Produtos")
    def to_dict(self):
        return {
            "id": self.id,
            "venda_id": self.venda_id,
            "produto_id": self.produto_id,
            "qnt": self.qnt,
            "preco": self.preco,
            "total": self.total,
            "produto": self.produto.descricao if self.produto else None
        }   
    
