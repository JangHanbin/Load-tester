from .base import Job
from reporters.base import Subscriber
from time import time
import requests


class BaseClient(Subscriber):
    def __init__(self, iterations):
        self.iterations = iterations


    def on_load(self, method, host, success, stream, file):
        return Client((method, host, success, self.iterations, stream, file), {})


class Client(Job):
    def _run(self, worker, method, host, success, iterations, stream, file):

        for _ in range(iterations):
            data = None
            if file:
                with open(file, 'rb') as f:
                    data = f.read()

            # s = requests.Session()

            # with s.request(method=method, url=host, stream=True, data= data) as res:
            #     for content in res.iter_content(chunk_size=1024):
            #         if content:
            #             print(len(content))

            res = requests.request(method=method, url=host, stream=stream, data=data)
            worker.new_result(method, host, 'success' if res.status_code in success else 'failed status code : {0}, body : {1}'.format(res.status_code, res.text),
                              res.elapsed.total_seconds())
