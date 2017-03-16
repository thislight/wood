

class EventManager(object):
    callbacks = {}
    event_queue = []

    @classmethod
    def callback(cls,event,callback):
        if event not in cls.callbacks:
            cls.callbacks[event] = []

        cls.callbacks[event].append(callback)

    @classmethod
    def call(cls,event,*args,**kargs):
        cls.event_queue.append((event,args,kargs))

    @classmethod
    def finish_queue(cls):
        while len(cls.event_queue) > 0:
            name,args,kargs = cls.event_queue.pop()
            if name in cls.callbacks:
                for callback in cls.callbacks[name]:
                    callback(*args,**kargs)

    @classmethod
    def clean_env(cls):
        cls.callbacks = {}
        cls.event_queue = []


def event_callback(event):

    def set_callback(func):
        EventManager.callback(event,func)
        return func

    return set_callback


