import threading
import requests
from queue import Queue
from time import time

class Worker:
    def __init__(self, method, host, success, processes):
        self.method = method
        self.url = host
        self.success = success
        self.mon = threading.Condition()
        self.queue = Queue()
        self.pool = list()
        self.subscribers = {
            'reporters': list()
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
        start = time()
        res = requests.request(method=self.method, url=self.url)
        end = time()
        self.publish('reporters','new_result', self.method, self.url,'success' if res.status_code in self.success else 'failed', end-start)

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
            print('RAISE')
            raise

    def subscribe(self, channel, subscriber):
        self.subscribers[channel].append(subscriber)

    def unsubscribe(self, channel, subscriber):
        self.subscribers[channel].remove(subscriber)

    def publish(self, channel, *args, **kwargs):
        for subscriber in self.subscribers[channel]:
            job = subscriber.handle(self, *args, **kwargs)
            if job is not None:
                self._queue_job(job)