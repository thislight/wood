# wood
The faster way to build web application by tornado.

>Wood is grow fast.API maybe change a lot in untest branch.

## Quick Start
>If you want to use the latest version, you can try to use 'untest' branch.

>wood is alpha now, you only can install wth code.

1.Install `git`.

with apt:
````
apt install git
````

with dnf:
````
dnf install git
````

2.Clone & Install wood
````
cd ~
git clone https://github.com/thislight/wood.git
cd wood
python setup.py install
# Or you can use 'pip install .'
````

## How to use
>Tips: After start develop by wood,you should know something about tornado.

Wood is very easy for make a web app:

````
from wood import Wood # First, import wood is important!

w = Wood(__name__,debug=True,log_function=print) # Make a new 'Wood' object with debug mode, and log to print.

IndexHandler = w.empty(uri='/',name='IndexHandler') # Make a empty handler

@IndexHandler.get
def index_page(self): # Will be called when get '/'
    self.write('滑稽，这里什么都没有\n(HuajiEnv)')

if __name__ == '__main__':
    w.start(port=6000)# Start server now!
````

Then, open 127.0.0.1:6000 to see the result.

More infomation, see Wiki.

## Talk
Talk something about wood & tornado.
Telegram Group:
>Wood
Language(语言): 中文(简/繁) / English

>Wood, a small project for tornado.
A faster way to make web app by tornado.
GitHub repo: https://github.com/thislight/wood
https://telegram.me/woodproject

## License
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