
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
import requests

def _make_test_web_server(name):
    from wood import Wood
    sev = Wood(name)
    return sev


s = _make_test_web_server(__name__)


def test_can_define_method():
    p = s.empty('/','TESTPAGE')
    @p.get
    def test(self):
        pass
    assert hasattr(p.handler,'get')


def test_can_override_method():
    p = s.empty('/1','TESTPAGE')
    @p.override('get_current_user')
    def test(self):
        pass
    assert hasattr(p.handler,'get_current_user')



