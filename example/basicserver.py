

from wood import Wood

w = Wood(__name__,debug=True)

IndexHandler = w.empty(uri='/',name='IndexHandler')

@IndexHandler.get
def index_page(self):
    self.write('滑稽，这里什么都没有\n(HuajiEnv)')

if __name__ == '__main__':
    w.start(port=6000)
    
    
    
    
    