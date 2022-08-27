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
        self.logger.info('Job {0} started'.format(repr(job)))

    def on_finished(self, job):
        if job.exc_info[0] is not None:
            self.logger.error("Job %r errored", job, exc_info=job.exc_info)
        else:
            self.logger.info("Job %r finished", job, )

    def on_fatal_error(self, exc_info):
        self.logger.critical('FATAL ERROR', exc_info=exc_info)

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

