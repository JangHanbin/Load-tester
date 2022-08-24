class Subscriber:
    def handle(self, worker, name, *args, **kwargs):
        func = self.__class__.__dict__.get('on_' + name, None)
        if func is not None:
            return func(self, *args, **kwargs)