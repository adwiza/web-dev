from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index_page():
    if request.method == 'GET':
        request
        response = render_template('index.html', name='<s>World</s>', args=q)
        return response


app.run('localhost', 8080, debug=True)
