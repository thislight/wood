
"""
Wood author: thislight

Copyright 2016 thislight

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Under License Apache v2, more information, see file 'LICENSE' in project root directory.
"""
import tornado.httpserver as _httpserver
import tornado.web as _web
import tornado.ioloop as _ioloop
import logging


class BaseTornadoView(_web.RequestHandler):
    pass

class RouteAllow(object):
    pass


class _PackedView(RouteAllow):
    def __init__(self,view,name='View',uri='/'):
        self._view = view
        self._view.__name__ = name
        self.__name__ = name + '_Packed'
        self._uri = uri
    
    @property
    def get(self):
        return self.override('get',back=True)
    
    @property
    def post(self):
        return self.override('post',back=True)
    
    @property
    def head(self):
        return self.override('head',back=True)
    
    @property
    def put(self):
        return self.override('put',back=True)
    
    @property
    def delete(self):
        return self.override('delete',back=True)
    
    @property
    def patch(self):
        return self.override('patch',back=True)
    
    @property
    def options(self):
        return self.override('options',back=True)
    
     
    def override(self,name,back=False):
        def override(func):
            setattr(self.handler,name,func)
            if back: return func
        return override
    
    @property
    def handler(self):
        return self._view
    
    @handler.setter
    def handler(self,value):
        self._view = value
    
    @property
    def uri(self):
        return self._uri


def _make_empty_view(name,uri,*parents):
    class View(BaseTornadoView,*parents):
        pass
    _packed = _PackedView(View,name=name,uri=uri)
    return _packed


def _make_uri_tuple(uri,handler,kargs=None):
    t = [uri,handler]
    if kargs: t.append(kargs)
    return tuple(t)


class Wood(object):
    def __init__(self,name=__name__,**config):
        self._app = _web.Application(**config)
        self._server = _httpserver.HTTPServer(self._app,xheaders=True)
        self._name = name
        self.prepare_funcs = []
    
    @property
    def server(self):
        return self._server
    
    @property
    def application(self):
        return self._app
    
    def handler(self,uri,handler,host='',**kargs):
        self.application.add_handlers(host,[_make_uri_tuple(uri,handler,kargs)])
    
    def empty(self,uri,name,*parents):
        """
        Return a empty TonradoView object.
        """
        v = _make_empty_view(uri=uri,name=name,*parents)
        self.route(v)
        return v
    
    def route(self,view):
        self.handler(uri=view.uri,handler=view.handler)
    
    def route_all(self,g):
        for k in g:
            o = g[k]
            if isinstance(o,RouteAllow):
                self.route(o)
    
    def bind(self,port):
        self.server.bind(port)
    
    def prepare(self,func):
        self.prepare_funcs.append(func)
        return func
    
    def call_prepare(self):
        for f in self.prepare_funcs:
            f(self)
    
    def _start(self):
        self.call_prepare()
        self.ioloop.start()
    
    def start(self,port=None,wokers=None):
        if port: self.bind(port)
        if not wokers:
            self.server.start()
        else:
            self.server.start(wokers)
        self._start()
    
    @property
    def ioloop(self):
        return _ioloop.IOLoop.current()
        
        
# The end of the file


