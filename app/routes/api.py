from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys
from app.utils.auth import login_required

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

@bp.route('/comments', methods=['POST'])
@login_required
def comment():
    data = request.get_json() # gets submiited comment data from front end
    db = get_db() # opens connection to db

    try:
        # create a new comment
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id') # gets id of currently loggedIn user
        )

        db.add(newComment) # preps new record to be added to db
        db.commit() # acts as INSERT and attempts to add record to db
    except:
        print(sys.exc_info()[0]) # prints error

        db.rollback() # discards pending commit if it fails(i.e. validation error)
        return jsonify(message = 'Comment failed!'), 500
    
    return jsonify(id = newComment.id) # returns id of new comment to front end if created successfully. 

@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        # create a new vote with incoming id and session id
        newVote = Vote(
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Upvote failed!'), 500
    
    return '', 204

@bp.route('/posts', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    db = get_db()

    try:
        # create a new post
        newPost = Post(
            title = data['title'],
            post_url = data['post_url'],
            user_id = session.get('user_id')
        )

        db.add(newPost)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post failed!'), 500
    
    return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
    data = request.get_json()
    db = get_db()

    try: # retrieve post and update title property
        post = db.query(Post).filter(Post.id == id).one()
        post.title = data['title'] 
        # The post variable is an object created from the User class so it uses dot notation.
        # The data variable uses bracket notation because it is a python dictionary instead of an object. If the variable does not have its own methods, then it will be a dictionary. 
        db.commit()
    except: 
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found!'), 404
    
    return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
    db = get_db()

    try:
        db.delete(db.query(Post).filter(Post.id == id).one())
        db.commit()
        print('Post deleted!')
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found!'), 404

    print('Post deleted!')
    return '', 204

