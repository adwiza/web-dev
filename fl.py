from flask import Flask, request
from werkzeug.exceptions import NotFound, InternalServerError

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT'])
def index_page():
    if request.method == 'GET':
        raise InternalServerError('Error saving your data')
        return 'Hello, world!', 200
    else:
        return f'Hello {request.method} Request!'


@app.route('/404/')
def not_found():
    raise NotFound


app.run('localhost', 8080, debug=True)