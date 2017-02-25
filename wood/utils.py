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
