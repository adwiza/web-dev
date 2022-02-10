from werkzeug import Response, Request


def application(environ, start_response):
    response = Response('Hello world!', mimetype='text/plain')
    return response(environ, start_response)


def application2(environ, start_response):
    request = Request(environ)
    text = 'Query param is %s' % request.args.get('q', '')
    return Response(text, mimetype='text/plain')(environ, start_response)


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = application2()
    run_simple(
        '127.0.0.1', 9090, app,
        use_debugger=True, use_reloader=True, processes=2,
    )
