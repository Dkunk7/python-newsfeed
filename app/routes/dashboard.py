from flask import Blueprint, render_template

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
# url prefix makes it so the below routes are /dashboard and /dashboard/edit/<id> (it's a prefix to all the routes here)

@bp.route('/')
def dash():
    return render_template('dashboard.html')

@bp.route('/edit/<id>')
def edit(id):
    return render_template('edit-post.html')