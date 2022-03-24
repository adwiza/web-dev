import json
from http.client import responses


class Application:

    redirect_if_no_trailing_slash = True

    def __init__(self):
        self.handlers_map = {}

    def add_handler(self, path, handler_callable):
        self.handlers_map[path] = handler_callable

    def __call__(self, env, start_response):
        # print(env)
        path = env['PATH_INFO']
        if not path.endswith('/') and self.redirect_if_no_trailing_slash:
            handler = self.redirect_trailing_slash_handler
        else:
            handler = self.handlers_map.get(path, self.not_found_handler)
        response = handler(env)

        response_headers = {'Content-Type': 'text/html'}
        response_body = ''
        if 'text' in response:
            response_body = response['text']
        elif 'json' in response:
            response_body = json.dumps(response['json'])
            response_headers = {'Content-Type': 'text/json'}

        status_code = response.get('status_code', 200)
        extra_header = response.get('extra_headers', {})

        response_headers.update(extra_header)
        start_response(f'{status_code} {responses[status_code]}', list(response_headers.items()))
        return [response_body.encode('utf-8')]

    @staticmethod
    def not_found_handler(env):
        return {
            'text': 'Not found',
            'status_code': 404
        }

    @staticmethod
    def redirect_trailing_slash_handler(env):
        path = env['PATH_INFO'] + '/'
        return {
            'status_code': 301,
            'extra_headers': {'location': path}
        }


