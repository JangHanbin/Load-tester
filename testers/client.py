from .base import Job
from reporters.base import Subscriber
from time import time
import requests

class BaseClient(Subscriber):


class Client(Job):

    def _run(self, worker, ):

        worker.new_result(self.method, self.url, 'success' if res.status_code in self.success else 'failed', end - start)

    def do(self):
        start = time()
        res = requests.request(method=self.method, url=self.url)
        end = time()
