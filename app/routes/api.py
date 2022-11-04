from flask import Blueprint, request, jsonify, session # request and session are global objects (like g)
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required
import sys 

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    db = get_db()
    
    try: # This is very similar to try .. catch in JS, but it's try .. except
        # attempt to create a new user
        newUser = User(
            username = data['username'], # username inside of data is not an object like in JavaScript. Instead it is a "dictionary", and this is the syntax for retrieving it
            email = data['email'],
            password = data['password']
        )

        # save in database
        db.add(newUser) # Here, you add and then commit. Kinda like how committing/pushing works with git
        db.commit()
    except:
        print(sys.exc_info()[0]) # This makes the error print (it will not print otherwise; I guess try/except prevents an actual error from printing)
        # AssertionError appears when a custom validation fails, like @ in an email or username length
        # sqlalchemy.exc.IntegrityError appears when it's an error specific to MySQL, like email needing to be UNIQUE

        # Keep in mind that if db.commit() fails, the connection will remain in a pending state. This doesn't seem to have any negative effects during local testing.
        # You can try to sign up again on the front end, and the next attempt will go through just fine. In a production environment, however, 
        # those pending database connections can result in app crashes. Fix this by using rollback() BELOW vvv

        #insert failed, so rollback and send error to front end
        db.rollback()
        return jsonify(message = 'Signup failed'), 500

    session.clear() # NOTE: you can only create sessions in Flask if you have a secret key defined, which I do in app/__init__.py
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204 # status code 204 means there is no content

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
        # Note that data['password'] becomes the second parameter in the verify_password() method of the class, because the first parameter is reserved for self.

    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return jsonify(id = user.id)

@bp.route('/comments', methods=['POST'])
@login_required
def comment():
    data = request.get_json()
    db = get_db()

    try:
        # create a new comment
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newComment)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback() # discards the pending commit if it fails
        return jsonify(message = 'Comment failed'), 500

    return jsonify(id = newComment.id)


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
        return jsonify(message = 'Upvote failed'), 500

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
        return jsonify(message = 'Post failed'), 500

    return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
    data = request.get_json()
    db = get_db()

    try:
        # retrieve post and update title property
        post = db.query(Post).filter(Post.id == id).one()
        post.title = data['title']
        db.commit()
        # Above ^^
        # The data variable is a dictionary—hence, the bracket notation of data['title']. The post variable, contrastingly, is an object created from the User class—so it uses dot notation.
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404

    return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
    db = get_db()

    try:
        # delete post from db
        db.delete(db.query(Post).filter(Post.id == id).one())
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404

    return '', 204