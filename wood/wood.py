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
from . import utils
import tornado.httpserver as _httpserver
import tornado.web as _web
import tornado.ioloop as _ioloop

BASELOGTEMPLATE = '{method} {httpver} {path} {handler_name} {request_time}s'


def _get_formated_log_string_from_handler(handler):
    return BASELOGTEMPLATE.format(**utils.get_info(handler))


class BaseTornadoView(_web.RequestHandler):
    def __log__(self):
        return _get_formated_log_string_from_handler(self)

    def get_upload_file(self,name,offest=0):
        f = self.request.files[name][offest]
        return utils.UploadedFile.from_reqfile(f)


class PackedHandler(utils.RegisterAllow):
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

    @property
    def uri(self):
        return self._uri


def make_empty_view(uri, name='View', *parents):
    """
    a help function for make a empty view.
    :return: PackedHandler
    """
    view = type(name, (BaseTornadoView, *parents), {})
    view.__name__ = name
    _packed = PackedHandler(view, uri=uri)
    return _packed


def base_log_function(o):
    if hasattr(o, '__log__'):  #
        utils.print_and_log(o.__log__())
    elif isinstance(o, _web.ErrorHandler):
        utils.print_and_log(_get_formated_log_string_from_handler(o))
    else:
        utils.print_and_log(str(o))


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
        if not hasattr(self, '_server'):
            self._server = _httpserver.HTTPServer(self.application, xheaders=True)
        return self._server

    @property
    def application(self):
        if not hasattr(self, '_app'):
            self._app = _web.Application(**self._app_settings)
        return self._app

    def handler(self, uri, handler, **kargs):
        """
        ADD handler to handle uri
        :param uri: URI for handler
        :param handler: handler
        :param kargs: arguments call handler.prepare (tornado feature)
        :return: None
        """
        self.application.add_handlers('.*$', [utils.make_uri_tuple(uri, handler, kargs)])

    def empty(self, uri, name, *parents):
        """
        :return: PackedHandler
        """
        v = make_empty_view(uri=uri, name=name, *parents)
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
        """
        Add handler from a RegisterAllow object
        :param view: utils.RegisterAllow
        :return:
        """
        if isinstance(view, utils.RegisterAllow):
            self.handler(uri=view.uri, handler=view.handler)

    def register_all(self, g):
        """
        Register all RegisterAllow object of a dict
        :param g: dict
        :return:
        """
        for k in g:
            o = g[k]
            if isinstance(o, utils.RegisterAllow):
                self.register(o)

    def uimod(self, name):
        """
        A dec to add ui_module
        :param name: Name of ui module
        :return: function
        """

        def register_uimod(cls):
            self.application.ui_modules.update({
                name: cls
            })
            return cls

        return register_uimod

    def websocket(self, uri):
        """
        A dec to add websocket handler
        :param uri: str
        :return: function
        """

        def register_websocket(cls):
            packed = PackedHandler(cls, uri)
            self.register(packed)
            return packed

        return register_websocket

    def _bind(self):
        """
        Bind all of ports in list self._bind_ports
        """
        for p in self._bind_ports:
            self.server.bind(p)

    def bind(self, port):
        """
        Bind a port
        :param port: int
        :return:
        """
        self._bind_ports.append(port)

    def prepare(self, func):
        """
        A dec to add function that called before ioloop start
        :param func: function
        :return:
        """
        self.prepare_funcs.append(func)
        return func

    def call_prepare(self):
        """
        Called before ioloop start
        :return:
        """
        for f in self.prepare_funcs:
            f(self)

    def _start(self):
        """
        Call parepre function and start ioloop
        :return:
        """
        self.call_prepare()
        try:
            self.ioloop.start()
        except Exception as e:
            self.server.stop()
            raise SystemExit from e

    def start(self, port=None, wokers=None):
        """
        Start server
        :param port: int, call self.bind
        :param wokers: int, how many workers you want to start
        :return:
        """
        if port:
            self.bind(port)
        self._bind()  # Bind before start server.
        if not wokers:
            self.server.start()
        else:
            self.server.start(wokers)
        self._start()

    def stop(self):
        """
        Stop server safely
        :return:
        """
        self.ioloop.stop()
        self.server.stop()

    @property
    def ioloop(self):
        """
        Get current ioloop
        :return: _ioloop.IOLOOP
        """
        return _ioloop.IOLoop.current()

# The end of the file
