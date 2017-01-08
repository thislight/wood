
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

import time


def timeit(callback=None,num=4):
    """
    A function timer.
    arg callback: a function to rev. time result.
    arg num: ...example: 0.162839, num=4 -> callback('0.1628')
    Return: function
    """
     def timeit(f)
        if not callback: return f
        def mock_func(*args,**kargs):
            t1 = time.process_time()
            _r = f(*args,**kargs)
            t2 = time.process_time()
            template = '{0:.%if}' % num
            callback(template.format(t2-t1))
            return _r
       return mock_func
    return timeit

