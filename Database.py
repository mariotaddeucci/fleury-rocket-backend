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
    ac = Column(Boolean, nullable=False)
    restricoes = relationship("ExameRestricao", back_populates="exame")


class Restricao(Model):
    __tablename__ = 'restricao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(255), nullable=False, unique=True)


class RestricaoMsg(Model):
    __tablename__ = 'restricao_msg'
    id_restricao = Column(Integer, ForeignKey(Restricao.__tablename__ + '.id'), primary_key=True)
    executar = Column(Boolean, nullable=False, primary_key=True)
    mensagem = Column(String(255), nullable=False)


class ExameRestricao(Model):
    __tablename__ = 'exame_restricao'
    id_exame = Column(Integer, ForeignKey(Exame.__tablename__ + '.id'))
    id_restricao = Column(Integer, primary_key=True)
    tempo_restricao = Column(Integer, nullable=False)
    executar = Column(Boolean, nullable=False)

    exame = relationship("Exame", back_populates="restricoes")

    __table_args__ = (
        ForeignKeyConstraint([executar, id_restricao], [RestricaoMsg.executar, RestricaoMsg.id_restricao]),
        UniqueConstraint('id_exame', 'id_restricao'),
        {})


engine = create_engine('sqlite:///databse.db')
Model.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
