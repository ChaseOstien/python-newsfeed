from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json() # get data from signup form, creates a dictionary instead of an object(look into python data types)
    db = get_db() # open db connection
    
    try:
        # create a new user 
        newUser = User( 
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        # save new user in db
        db.add(newUser) # preps INSERT statement
        db.commit() # commit changes to db
    except:
        #  if insert fails, send error to front end
        print(sys.exe_info()[0])
        # insert failed, so rollback and send error to front end
        db.rollback()
        return jsonify(message = 'Signup Failed'), 500
    
    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return jsonify(id = newUser.id) # return json to the browser including the ID of the new user created in the database.

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])

        return jsonify(message = 'Incorrect credentials'), 400
    
    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400
    
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return jsonify(id = user.id)

