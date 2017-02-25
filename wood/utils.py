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
import os
import time
import logging

def get_info(handler):
    _r = handler.request
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
        handler_name=getattr(handler, '__name__', str(handler)),
    )


def make_uri_tuple(uri, handler, kargs=None):
    t = [uri, handler]
    if kargs: t.append(kargs)
    return tuple(t)


def print_and_log(msg, logger=logging.getLogger()):
    """
    Print msg and log msg to logger
    :param msg: msg string
    :param logger: A logger from logging
    :return: None
    """
    print(msg)
    logger.info(msg)


class UploadedFile(object):
    def __init__(self, name, b):
        self.name = name
        self.body = b

    def one_name(self):
        return str(time.time()) + self.name

    def write_to(self, path):
        f = open(path, "w+b")
        f.write(self.body)

    def write_auto(self, basepath):
        self.write_to(os.path.join(basepath, self.one_name()))

    @classmethod
    def from_reqfile(cls, f):
        """
        Create object from file dict of tornado request
        :param f: dict
        :return: UploadedFile
        """
        return cls(f["filename"], f["body"])


class RegisterAllow(object):
    """
    Override all of methods to use for route handler
    """

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
