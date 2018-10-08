from flask_restless import APIManager
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from Processors import *
from database import db_session, Property, User, RealEstate

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['DEBUG'] = True
jwt = JWTManager(app)
crud = ['GET', 'POST', 'PATCH', 'DELETE']

manager = APIManager(app, session=db_session, preprocessors=preprocessor_default)
manager.create_api(Property, methods=crud)
manager.create_api(User, methods=crud)
manager.create_api(RealEstate, methods=crud, preprocessors=preprocessors_real_estate)


@app.teardown_appcontext
def cleanup(resp_or_exc):
    db_session.remove()


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is not None and password is not None:
        u = db_session.query(User).filter_by(username=username).filter_by(password=password).first()
        if u is not None:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
    return '{}'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
