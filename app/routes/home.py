from flask import Blueprint, render_template

from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')
# Blueprint() lets you consolidate routes onto a single bp object that the parent app can register later. This corresponds to using the Router middleware of Express.js.

@bp.route('/')
def index():
    # get all posts
    db = get_db()
    # The get_db() function returns a session connection that's tied to this route's context. 
    # We then use the query() method on the connection object to query the Post model for all posts in descending order, and we save the results in the posts variable.
    posts = db.query(Post).order_by(Post.created_at.desc()).all()

    return render_template(
        'homepage.html',
        posts=posts
    )

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/post/<id>')
def single(id):
    # get single post by id
    db = get_db()
    post = db.query(Post).filter(Post.id == id).one()

    # render single post template
    return render_template(
        'single-post.html',
        post=post
    )

