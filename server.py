"""Provides the WSGI application entry point for Kepler services.
"""

import importlib
import os
import sys
from wsgiref import simple_server

def application(env, res):
    res('200 OK', [('Content-Type', 'text/plain')])
    return ['Farewell, cruel world!']

def main(ip='127.0.0.1', port=8000, app=application):
    httpd = simple_server.make_server(ip, port, app)
    print('Serving application with wsgiref.simple_server @ %s:%u' % (ip, port))
    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fqmn = sys.argv[1].split('.')
        m = importlib.import_module('.'.join(fqmn[:-1]))
        svc = getattr(m, fqmn[-1])()
        main(app=svc.app)
    else:
        main()
