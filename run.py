from flask_restless import APIManager
from flask import Flask
from Database import db_session, Exame

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['DEBUG'] = True
crud = ['GET', 'POST', 'PATCH', 'DELETE']

manager = APIManager(app, session=db_session)
manager.create_api(Exame, methods=['GET'])


@app.teardown_appcontext
def cleanup(resp_or_exc):
    db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
