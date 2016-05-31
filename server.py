"""Provides the WSGI application entry point for Kepler services.
"""

from wsgiref import simple_server

def application(env, res):
    res('200 OK', [('Content-Type', 'text/plain')])
    return ['Farewell, cruel world!']

def main(ip='127.0.0.1', port=8000):
    httpd = simple_server.make_server(ip, port, application)
    print('Serving application with wsgiref.simple_server @ %s:%u' % (ip, port))
    httpd.serve_forever()

if __name__ == '__main__':
    main()
