from flask import Blueprint, render_template, session, redirect
from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
  # get all posts
  db = get_db() # establishes database connection for this request to be made
  posts = db.query(Post).order_by(Post.created_at.desc()).all() # querying the Post table in the database for all posts in descending order by created_at date

  return render_template('homepage.html', posts=posts, loggedIn=session.get('loggedIn'))

@bp.route('/login')
def login():
  # not logged in yet
  if session.get('loggedIn') is None:
    return render_template('login.html')

  return redirect('/dashboard')

@bp.route('/post/<id>')
def single(id):
  # get single post by id
  db = get_db() # establish database connection for route
  post = db.query(Post).filter(Post.id == id).one() # querying the Post table in the database for a single Post that matches the id passed to the request.

  return render_template('single-post.html', post=post, loggedIn=session.get('loggedIn'))
