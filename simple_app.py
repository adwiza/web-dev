def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello world from a simpleff WSGI application!']


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    from werkzeug.testapp import test_app
    app = test_app()
    run_simple(
        'localhost', 9090, app,
        use_debugger=True, use_reloader=True, processes=2,
    )
