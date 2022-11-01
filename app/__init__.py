from app.routes import home, dashboard # Home is bp, which was imported and renamed in routes/__init__.py
# app.routes grabs the __init__ in routes, similar to how index.js works (same goes for dashboard)

from flask import Flask

def create_app(test_config=None):
    # set up app config
    app =Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY='super_secret_key'
    )

    @app.route('/hello')
    def hello():
        return 'hello world'

    # N O T E: The below block of code is the Express.js equivalent of the @app.route block above
    # app.get('/hello', (req, res) => {
    # res.send('hello world');
    # });

    # register routes
    app.register_blueprint(home)
    app.register_blueprint(dashboard)

    return app