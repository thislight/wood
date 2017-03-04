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
from ..wood import make_empty_view, Wood

class Blueprint(object):
    def __init__(self):
        self.handlers = []

    def empty(self, uri, name, *parents):
        """
        Get a empty `PackedHandler`
        :param uri: str
        :param name: str, name of handler
        :param parents: parents of handler
        :return: PackedHandler
        """
        v = make_empty_view(uri=uri, name=name, *parents)
        self.handlers.append(v)
        return v

    def route(self, uri=r"/", method="get", *parents, **kargs):
        """
        Get a handler and add route
        :param uri: str
        :param method: str, method of function
        :param parents: parents of handler
        :param kargs:no use
        :return: function
        """
        def register_route(func):
            """
            :param func: function
            :return: PackedHandler
            """
            v = self.empty(uri,func.__name___,*parents)
            v.override(method.lower())(func)
            return v

        return register_route

    def to(self,w):
        for handler in self.handlers:
            w.register(handler)

    def get_wood(self,**kargs):
        w = Wood(**kargs)
        self.to(w)
        return w
