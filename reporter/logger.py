import logging
from .base import Subscriber


class Logger(Subscriber):
    def __init__(self, type='c', level=logging.INFO, file_name='tester.log'):
        self.logger = logging.getLogger('test_logger')
        formatter = logging.Formatter('[ %(levelname)s | %(filename)s: %(lineno)s] %(asctime)s > %(message)s')

        if level == 'DEBUG':
            level = logging.DEBUG
        elif level == 'INFO':
            level = logging.INFO
        elif level == 'WARN':
            level = logging.WARN
        elif level == 'ERR':
            level = logging.ERROR
        elif level == 'CRITICAL':
            level = logging.CRITICAL
        else:
            raise NameError('Logging Level name error')

        self.logger.setLevel(level=level)

        if type == 'f':
            fh = logging.FileHandler(file_name)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        elif type == 'cf':
            sh = logging.StreamHandler()
            fh = logging.FileHandler(file_name)
            sh.setFormatter(formatter)
            fh.setFormatter(formatter)
            self.logger.addHandler(sh)
            self.logger.addHandler(fh)

        else:
            # console output
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)

    def on_start(self, job):
        pass

    def on_finished(self, job):
        pass

    def on_fatal_error(self, exc_cls, exc_val, exc_tb):
        pass

    def on_update(self, job):
        pass

    def on_scanned(self, agent, resource, no_more):
        pass

    def on_new_issue(self, agent, resource):
        pass

    def on_new_error(self, url, exception):
        pass

    def on_new_result(self, method, url, result, elapsed_time):
        self.logger.info('New result [{0} {1}] -> {2} time takes : {3}'.format(method.upper(), url, result, elapsed_time))

