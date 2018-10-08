from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session

Model = declarative_base()


class Exame(Model):
    __tablename__ = 'exame'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    duracao = Column(Integer, nullable=False)


class Restricao(Model):
    __tablename__ = 'restricao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(255), nullable=False, unique=True)


class RestricaoMsg(Model):
    __tablename__ = 'restricao_msg'
    id_restricao = Column(Integer, primary_key=True, autoincrement=True)
    executar = Column(Boolean, nullable=False)
    mensagem = Column(String(255), nullable=False)


class ExameRestricao(Model):
    __tablename__ = 'exame_restricao'
    id_exame = Column(Integer, primary_key=True, autoincrement=True)
    id_restricao = Column(Integer, primary_key=True, autoincrement=True)
    tempo_restricao = Column(String(255), nullable=False)
    executar = Column(Boolean, nullable=False)


engine = create_engine('sqlite:///database.db')
Model.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
