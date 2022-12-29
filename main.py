from flask import Flask, request, render_template
from products_views import product_app
from cart_views import cart_app

app = Flask(__name__)
app.register_blueprint(product_app, url_prefix='/products')
app.register_blueprint(cart_app, url_prefix='/cart')


# app.config.from_object('config.ProductionConfig')
# app.config.from_envvar('APP_SETTINGS')
#  $ APP_SETTINGS=/project/config.cfg python app.py
# app.config.update(
#     DEBUG=True,
#     SECRET_KEY='...',
#     DB_URL='sqlite',
# )


@app.route('/')
@app.route('/<name>/')
@app.route('/<int:user_id>/')
@app.route('/<float:user_id>/')
def index_page(name=None, user_id=None):

    if request.method == 'GET':
        request
        response = render_template(
            'index.html',
            name=name or 'World',
            products=['spam', 'eggs'],
            args=request.args,
            user_id=user_id
        )
        return response


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'


class Production(Config):
    DATABASE_URI = 'mysql://user@localhost:foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


app.run('localhost', 8080, debug=True)
