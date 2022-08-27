import sys

class Job:
    def __init__(self, args, kwargs, parent=None):
        self.args = args
        self.kwargs = kwargs
        self.parent = parent
        self.children = set()
        self.cancelled = False
        self.exc_info = None, None, None

    def start(self, worker):
        worker.submit(self._invoke, (worker,), {})

    def _invoke(self, worker):
        try:
            self._run(worker, *self.args, **self.kwargs)
        except:
            self.exc_info = sys.exc_info()
        finally:
            worker.job_done(self)