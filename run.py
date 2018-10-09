from flask_restless import APIManager
from flask import Flask, jsonify
from Database import db_session, Exame

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['DEBUG'] = True
crud = ['GET', 'POST', 'PATCH', 'DELETE']


@app.teardown_appcontext
def cleanup(resp_or_exc):
    db_session.remove()


@app.route('/api/exame')
def rest_exame():
    dt = db_session.query(Exame.id, Exame.nome, Exame.ac).all()
    dt = [{'id': d[0], 'name': d[1], 'ac': bool(d[2])} for d in dt]
    return jsonify(dt)


@app.route('/api/roteiro')
def roteiro():
    dt = db_session.query(Exame).all()
    for d in dt:
        print(d)
    return 'teste'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
