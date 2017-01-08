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


class functools(object):
    @staticmethod
    def pass_func(func):
        def hook(self, *args, **kargs):
            print('Wraning: a passed function was called,name {}'.format(func.__name__))
            return

        return hook

    @staticmethod
    def call_or_not(f, *args, **kargs):
        if f:
            return f(*args, **kargs)
        else:
            return None


class LazyProxy(object):
    def __init__(self, cls):
        self._cls = cls
        self._mocks = {}

    def __call__(self, *args, **kargs):
        self._obj = self._cls(*args, **kargs)

    def mock(self, name, value):
        self._mocks[name] = value

    def __getattr__(self, item):
        if item in self._mocks:
            return self._mocks[item]
        elif self._obj and hasattr(self._obj, item):
            return getattr(self._obj, item)
        else:
            return getattr(self._cls, item)

    def __setattr__(self, name, value):
        if name in self._mocks:
            self._mocks[name] = value
        elif not self._obj:
            setattr(self._cls, name, value)
        else:
            setattr(self._obj, name, value)
