import sys
import threading
import requests
from queue import Queue
from time import time

class Worker:
    def __init__(self, processes):

        self.mon = threading.Condition()
        self.queue = Queue()
        self.pool = list()
        self.subscribers = {
            'reporters': list(),
            'clients': list()
        }
        self.jobs = list()
        self.counter = 0
        self._init_thread(processes)

    def _init_thread(self, processes):
        for _ in range(processes):
            th = threading.Thread(target=self._do)
            th.daemon = True
            self.pool.append(th)

    def _start(self):
        with self.mon:
            self.counter += 1

    def _done(self):
        with self.mon:
            if self.counter == 0 and not self.jobs:
                self.mon.notify()

    def _do(self):
        while True:
            item = self.queue.get()
            try:
                if not item:
                    break
                func, args, kwargs = item
                try:
                    func(*args, **kwargs)
                except:
                    self.fatal_error(sys.exc_info())
                finally:
                    self._done()
            finally:
                self.queue.task_done()


    def start(self):
        for th in self.pool:
            th.start()

    def join(self):
        with self.mon:
            while self.counter > 0:
                self.mon.wait()
            for th in self.pool:
                if th.is_alive():
                    self.queue.put(None)
            for th in self.pool:
                if th.is_alive():
                    th.join()

    def _queue_job(self, job):
        self.publish('reporters', 'start', job)
        with self.mon:
            parent = job.parent
            if parent is not None:
                if parent in self.jobs:
                    parent.children.add(job)
                else:
                    job.parent = parent = None
        try:
            job.start(self)
        except:

            raise
    def job_done(self, job):
        self.publish('reporters', 'finished', job)
        with self.mon:
            parent = job.parent
            if parent is not None:
                parent.children.discard(job)
            for x in job.children:
                if x.parent is job:
                    x.parent = parent
            if self.counter == 0 and not self.jobs:
                self.mon.notify()

    def fatal_error(self, exc_info):
        self.publish('reporters', 'fatal_error', exc_info)

    def new_result(self, method, url, result, elapsed_time):
        self.publish('reporters', 'new_result', method, url, result, elapsed_time)

    def subscribe(self, channel, subscriber):
        self.subscribers[channel].append(subscriber)

    def unsubscribe(self, channel, subscriber):
        self.subscribers[channel].remove(subscriber)

    def publish(self, channel, *args, **kwargs):
        for subscriber in self.subscribers[channel]:
            job = subscriber.handle(self, *args, **kwargs)
            if job is not None:
                self._queue_job(job)

    def submit(self, func, args, kwargs):
        self._start()
        try:
            self.queue.put((func, args, kwargs))
        except:
            self._done()
            raise

    def new_task(self, method, host, success, stream, file=None):
        self.publish('clients', 'load', method, host, success, stream, file)

