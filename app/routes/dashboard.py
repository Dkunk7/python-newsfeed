from flask import Blueprint, render_template, session
from app.models import Post
from app.db import get_db
from app.utils.auth import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
# url prefix makes it so the below routes are /dashboard and /dashboard/edit/<id> (it's a prefix to all the routes here)

@bp.route('/')
@login_required
def dash():
    db = get_db()
    posts = (
        db.query(Post)
        .filter(Post.user_id == session.get('user_id'))
        .order_by(Post.created_at.desc())
        .all()
    ) # This lengthy query is more readable when broken up into multiple lines, but to do so, we have to wrap the query in parentheses. 
      # Remember that Python cares about spacing. Without the parentheses, this would throw an indentation error.

    return render_template(
        'dashboard.html',
        posts=posts,
        loggedIn=session.get('loggedIn')
    )

@bp.route('/edit/<id>')
@login_required
def edit(id):
    # get single post by id
    db = get_db()
    post = db.query(Post).filter(Post.id == id).one()

    # render edit page
    return render_template(
        'edit-post.html',
        post=post,
        loggedIn=session.get('loggedIn')
    )
    # The edit() function is decorated (that is, wrapped) with another function called @bp.route(). 
    # The at-sign character (@) signifies that the function should be treated as a decorator—which passes the index() function to the route() function to be called at a later time.