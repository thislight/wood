

class EventManager(object):
    callbacks = {}
    event_queue = []

    @classmethod
    def callback(cls,event,callback):
        if event not in cls.callbacks:
            cls.callbacks.extend({
                event:[]
            })

        cls.callbacks[event].append(callback)

    @classmethod
    def call(cls,event,*args,**kargs):
        cls.event_queue.append(tuple(event,args,kargs))

    @classmethod
    def finish_queue(cls):
        while len(cls.event_queue) > 0:
            name,args,kargs = cls.event_queue.pop()
            if name in cls.callbacks:
                for callback in cls.callbacks:
                    callback(*args,**kargs)


def event_callback(event):

    def set_callback(func):
        EventManager.callback(event,func)
        return func

    return func


