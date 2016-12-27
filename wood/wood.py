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
from .utils import functools

BASELOGTEMPLATE = '{method} {httpver} {path} {handler_name} {request_time}s'


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
            handler_name=self.__name__,
        )

    def __log__(self):
        info = self._get_info()
        return BASELOGTEMPLATE.format(**info)


class RegisterAllow(object):
    @property
    def uri(self):
        """
        Override to return a uri to register
        :return: str
        """
        return None

    @property
    def handler(self):
        """
        Override to return a handler to register
        :return: tornado.web.RequestHandler
        """
        return None


class PackedHandler(RegisterAllow):
    def __init__(self, view, uri='/'):
        self._view = view
        self.__name__ = self._view.__name__ + '_Packed'
        self._uri = uri

    @property
    def get(self):
        return self.override('get', back=True)

    @property
    def post(self):
        return self.override('post', back=True)

    @property
    def head(self):
        return self.override('head', back=True)

    @property
    def put(self):
        return self.override('put', back=True)

    @property
    def delete(self):
        return self.override('delete', back=True)

    @property
    def patch(self):
        return self.override('patch', back=True)

    @property
    def options(self):
        return self.override('options', back=True)

    def override(self, name, back=False):
        def override(func):
            setattr(self.handler, name, func)
            if back:
                return func

        return override

    @property
    def handler(self):
        return self._view

    @handler.setter
    def handler(self, value):
        self._view = value

    @property
    def uri(self):
        return self._uri


class PackedUIModlue(_web.UIModule):
    def render(self, *args, **kargs):
        result = functools.call_or_not(self._dyncall, self, *args, **kargs)
        if result:
            return result

    def js(self, code):
        self._jscode = code
        return self

    def jsfile(self, *paths):
        if not self._jsfiles:
            self._jsfiles = []
        for v in paths:
            if v not in self._jsfiles:
                self._jsfiles.append(v)
        return self

    def css(self, code):
        self._csscode = code
        return self

    def cssfile(self, *paths):
        if not self._cssfiles:
            self._cssfiles = []
        for v in paths:
            if v not in self._cssfiles:
                self._cssfiles.append(v)
        return self

    def embedded_javascript(self):
        return self._jscode

    def embedded_css(self):
        return self._csscode

    def javascript_files(self):
        return self._jsfiles

    def css_files(self):
        return self._cssfiles

    def prepare(self, f):
        f(self)
        return f

    def dynrender(self, f):
        self._dyncall = f
        return f


def _make_empty_view(uri, name='View', *parents):
    """
    a help function for make a empty view.
    :return: PackedHandler
    """
    view = type(name, (BaseTornadoView, *parents), {})
    _packed = PackedHandler(view, uri=uri)
    return _packed


def _make_uri_tuple(uri, handler, kargs=None):
    t = [uri, handler]
    if kargs: t.append(kargs)
    return tuple(t)


def _print_and_log(msg, logger=logging.getLogger()):
    """
    Print msg and log msg to logger
    :param msg: msg string
    :param logger: A logger from logging
    :return: None
    """
    print(msg)
    logger.info(msg)


def base_log_function(o):
    if hasattr(o, '__log__'):  #
        _print_and_log(o.__log__)
    elif isinstance(o, _web.ErrorHandler):
        _print_and_log(o)  # TODO: More simple and useful infomation
    else:
        _print_and_log(str(o))


class Wood(object):
    def __init__(self, name=__name__, **config):
        self._app_settings = config
        self._name = name
        self.prepare_funcs = []
        if 'log_function' not in self._app_settings:
            self._app_settings['log_function'] = base_log_function
        self._bind_ports = []
        self._ui_mods = []
        if 'ui_modules' not in self._app_settings:
            self._app_settings['ui_modules'] = {}

    @property
    def server(self):
        if not hasattr(self,'_server'):
            self._server = _httpserver.HTTPServer(self.application, xheaders=True)
        return self._server

    @property
    def application(self):
        if not hasattr(self,'_app'):
            self._app = _web.Application(**self._app_settings)
        return self._app

    def handler(self, uri, handler, host='', **kargs):
        self.application.add_handlers(host, [_make_uri_tuple(uri, handler, kargs)])

    def empty(self, uri, name, *parents):
        """
        :return: PackedHandler
        """
        v = _make_empty_view(uri=uri, name=name, *parents)
        self.register(v)
        return v

    def route(self, uri='/', method='get', *parents, **kargs):
        """
        Route a function to uri.
        :return: function
        """

        def route(f):
            """
            :return: PackedHandler
            """
            view = self.empty(uri, f.__name__, *parents)
            mstr = method.lower()
            view.override(mstr)(f)
            return view

        return route

    def register(self, view):
        if isinstance(view, RegisterAllow):
            self.handler(uri=view.uri, handler=view.handler)

    def register_all(self, g):
        for k in g:
            o = g[k]
            if isinstance(o, RegisterAllow):
                self.register(o)

    def _bind(self):
        """
        Bind all of ports in list self._bind_ports
        """
        for p in self._bind_ports:
            self.server.bind(p)

    def bind(self, port):
        self._bind_ports.append(port)

    def prepare(self, func):
        self.prepare_funcs.append(func)
        return func

    def call_prepare(self):
        for f in self.prepare_funcs:
            f(self)

    def _start(self):
        self.call_prepare()
        self.ioloop.start()

    def start(self, port=None, wokers=None):
        if port:
            self.bind(port)
        self._bind()  # Bind before start server.
        if not wokers:
            self.server.start()
        else:
            self.server.start(wokers)
        self._start()

    @property
    def ioloop(self):
        return _ioloop.IOLoop.current()

# The end of the file
