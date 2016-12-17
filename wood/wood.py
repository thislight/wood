
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
from .timeit import timeit
import logging
import time


BASELOGTEMPLATE = '{method} {httpver} {path} {handler_name} {request_time}s/{timeit}s'


class BaseTornadoView(_web.RequestHandler):
    def _get_info(self):
        _r = self.request
        return dict(
        method=_r.method,
        path=_r.path,
        httpver=_r.version,
        cliip=_r.remote_ip,
        p=_r.protocol,
        issec=True if _r.protocol.endswith('s') else False,
        host=_r.host,
        args=_r.arguments,
        request_time=_r.request_time(),
        timeit=self._time,
        handler_name=self.__name__,
        )
    
    def __log__(self):
        info = self._get_info()
        return BASELOGTEMPLATE.format(**info)
    
    def timeit_callback(self,s):
        self._time = s
        

class RegisterAllow(object):
    pass


class OverrideObject(object):
    def override(self,name,back=False):
        def override(func):
            setattr(self.handler,name,func)
            if back: return func
        return override


class _PackedView(RegisterAllow,OverrideObject):
    def __init__(self,view,uri='/'):
        self._view = view
        self.__name__ = self._view.__name__ + '_Packed'
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
    
    @property
    def handler(self):
        return self._view
    
    @handler.setter
    def handler(self,value):
        self._view = value
    
    @property
    def uri(self):
        return self._uri
    
    def _timeit(self,f):
        return timeit(callback=self. handler.timeit_callback,num=2)(f)
    
    
    def override(self, back=False):
        def override(func):
            setattr(self.handler,name,func)
            if back: self._timeit(return func)
    return override    


def _make_empty_view(name='View',uri,*parents):
    """
    a help function for make a empty view.
    Return: _PackedView
    """
    view = type(name,(BaseTornadoView,*parent),{})
    _packed = _PackedView(view,uri=uri)
    return _packed


def _make_uri_tuple(uri,handler,kargs=None):
    t = [uri,handler]
    if kargs: t.append(kargs)
    return tuple(t)



def _print_and_log(logger=logging.getLogger(),*args):
    print(*args)
    logger.info(*args)


def base_log_function(o):
    if hasattr(o,'__log__'):# 
        _print_and_log(o.__log__)
    elif isinstance(o,_web.ErrorHandler):
        _print_and_log(o)# TODO: More simple and useful infomation
    else:
        _print_and_log(o)   
        

class Wood(object):
    def __init__(self,name=__name__,**config):
        self._app = _web.Application(**config)
        self._server = _httpserver.HTTPServer(self._app,xheaders=True)
        self._name = name
        self.prepare_funcs = []
        if 'log_function' not in self.application.settings:
            self.application.settings['log_function'] = base_log_function
        
    
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
        Return: _PackedView
        """
        v = _make_empty_view(uri=uri,name=name,*parents)
        self.register(v)
        return v
    
    def route(self,uri,method='get',*parents,**kargs):
        """
        Route a function to uri.
        arg method: method for function
        Return: function
        """
        def route(f):
            """
            Return: function
            """
            view = self.empty(uri,f.__name__,*parents)
            method = method.lower()
            return view.override(method)(f,back=True)
        return route
    
    def register(self,view):
        self.handler(uri=view.uri,handler=view.handler)
    
    def register_all(self,g):
        for k in g:
            o = g[k]
            if isinstance(o,RegisterAllow):
                self.register(o)
    
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

