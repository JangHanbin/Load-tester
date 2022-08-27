from .base import Job
from reporters.base import Subscriber
from time import time
import requests


class BaseClient(Subscriber):
    def __init__(self, iterations):
        self.iterations = iterations


    def on_load(self, method, host, success):
        return Client((method, host, success, self.iterations), {})


class Client(Job):
    def _run(self, worker, method, host, success, iterations):

        for _ in range(iterations):
            start = time()
            res = requests.request(method=method, url=host)
            end = time()
            worker.new_result(method, host, 'success' if res.status_code in success else 'failed',
                              end - start)


    # def _invoke(self, worker):
    # def do(self):

