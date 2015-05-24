from collections import defaultdict
class Events(object):

    def __init__(self):
        self.unsubscribe_all()
    
    def subscribe(self, event, handler):
        self.handlers[event].add(handler)
        
    def unsubscribe(self, obj):
        for key in self.handlers.iterkeys():
            self.handlers[key] = self.handlers[key] - \
            set(filter(lambda x: x.im_self == obj, self.handlers[key]))

    def unsubscribe_all(self):
        self.handlers = defaultdict(set)
            
    def emit(self, event):
        for handler in self.handlers[event]:
            handler(event)

events = Events()
