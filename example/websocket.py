"""
Wood author: thislight

Copyright 2016 thsilight

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Under License Apache v2, more infomation, see file 'LICENSE' in project root directory.
"""

from wood import Wood
from tornado.websocket import WebSocketHandler

app = Wood(__name__, debug=True)


@app.websocket(r"/websocket")
class SelfWebSocketHandler(WebSocketHandler):
    def open(self):
        print("WebSocket Opened")

    def on_message(self, message):
        self.write_message("{}, Hello!".format(message))

    def close(self):
        print("WebSocket closed.")


if __name__ == "__main__":
    app.start(6000)
