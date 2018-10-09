from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Exame(db.Model):
    __tablename__ = 'exame'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    ac = db.Column(db.Boolean, nullable=False)


class ExameTag(db.Model):
    __tablename__ = 'exame_tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(255), nullable=False)
    id_exame = db.Column(db.Integer, db.ForeignKey(Exame.__tablename__ + '.id'))


class Restricao(db.Model):
    __tablename__ = 'restricao'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(255), nullable=False, unique=True)


class RestricaoMsg(db.Model):
    __tablename__ = 'restricao_msg'
    id_restricao = db.Column(db.Integer, db.ForeignKey(Restricao.__tablename__ + '.id'), primary_key=True)
    executar = db.Column(db.Boolean, nullable=False, primary_key=True)
    mensagem = db.Column(db.String(255), nullable=False)


class ExameRestricao(db.Model):
    __tablename__ = 'exame_restricao'
    id_exame = db.Column(db.Integer, primary_key=True)
    id_restricao = db.Column(db.Integer, primary_key=True)
    tempo_restricao = db.Column(db.Integer, nullable=False)
    executar = db.Column(db.Boolean, nullable=False)
    mensagem = db.relationship("RestricaoMsg", uselist=False, backref="restricao_msg")

    __table_args__ = (db.ForeignKeyConstraint([id_restricao, executar],
                                              [RestricaoMsg.id_restricao, RestricaoMsg.executar]),
                      {})
