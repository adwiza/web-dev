from server import Application


def contacts_handler(env):
    return {
        "json": {"city": "Moscow"},
    }


def index_handler(env):
    return {
        'text': 'Hello World',
        'extra_headers': {'Content-Type': 'text/plain'}
    }


application = Application()
application.add_handler('/', index_handler)
application.add_handler('/contacts/', contacts_handler)
