from flask import Blueprint

product_app = Blueprint('products_app', __name__)


@product_app.route('/', endpoint='products')
def products_page():
    return '<h1>Products Page!</h1>'


@product_app.route('/<int:product_id>', endpoint='product')
def product_page(product_id):
    return f'<h1>Products {product_id}!</h1>'
