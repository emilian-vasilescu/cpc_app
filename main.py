from flask import Flask, request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from Models.User import User
from Services.Decorators.check_jwt_token import check_jwt_token
from app import app, db


@app.route('/user', methods=['GET'])
@check_jwt_token
def get_all_users(current_user):
    # querying the database
    # for all the entries in it
    users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append({
            'public_id': user.public_id,
            'name': user.name,
            'role': user.role,
            'email': user.email
        })

    return jsonify({
        'data': {
            'users': output
        }
    })


@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            {'error': 'Login email and password are required !!'},
            401
        )

    user = User.query \
        .filter_by(email=auth.get('email')) \
        .first()

    if not user:
        return make_response(
            {'error': 'User does not exist !!'},
            401
        )

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'data': {'token': token}}), 201)
    return make_response(
        {'error': 'Wrong Password !!'},
        403
    )


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.form

    name, email, role = data.get('name'), data.get('email'), data.get('role')
    password = data.get('password')

    # @todo Validate data
    if any(data is None for data in [name, email, role, password]):
        return make_response({'message': 'Name, role, email and password are mandatory.'}, 400)

    user = User.query \
        .filter_by(email=email) \
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            role=role,
            password=generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response({'message': 'Successfully registered.'}, 201)
    else:
        return make_response({'message': 'User already exists. Please Log in.'}, 202)


if __name__ == "__main__":
    app.run(debug=True)
