"""Defines an abstracted service model for interfacing to a WSGI request
"""

import pprint
import urlparse

class Service(object):
    def __init__(self):
        pass
        
    def _null(self, url, args):
        return ''
        
    def _root(self, url, args):
        return 'Here is the base.'

    def _help(self, url, args):
        return 'Here is some help!'
        
    def app(self, env, res):
        """Feed env parameters into urlparse object and query dictionary to 1)
           determine the appropriate operation to which those arguments will be
           forwarded to construct a response.
        """
        url = env['wsgi.url_scheme'] + '://' + env['HTTP_HOST'] + env['PATH_INFO']
        args = {}
        if len(env['QUERY_STRING']) > 0:
            url += '?' + env['QUERY_STRING']
            args = urlparse.parse_qs(env['QUERY_STRING'])
        o = urlparse.urlparse(url)
        paths = o.path.split('/')
        print(paths)
        if len(''.join(paths)) > 1 and len(paths) > 1:
            op = paths[1].lower()
        else:
            op = '_root'
        if op == 'favicon.ico':
            op = '_null'
        print('Generating response with operation "%s"' % op)
        m = getattr(self, op)
        try:
            rsp = [m(o, args)]
            res('200 OK', [('Content-Type', 'text/plain')])
        except:
            rsp = ['']
            res('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return rsp
