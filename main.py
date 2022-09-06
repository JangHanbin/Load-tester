import argparse
from worker import Worker
from reporters.logger import Logger
from testers.client import BaseClient
from pathlib import Path
import signal

num_of_task = 0
done = 0
def handler(signum, frame):
    print(worker)
    exit(signum)

def main(args):
    if args.log_file is None:
        logger = Logger(args.log_options[0], args.log_options[1])
    else:
        logger = Logger(args.log_options[0], args.log_options[1], args.log_file)

    if args.input_path is None and args.method == 'put':
        raise ValueError('PUT method needs --input-path option')
    global worker
    worker = Worker(args.processes)
    worker.subscribe('reporters', logger)
    worker.subscribe('clients', BaseClient(args.iterations))
    worker.start()

    # upload from input_path (PUT)
    global num_of_task
    global done
    if args.input_path:
        for path in Path(args.input_path).rglob('*'):
            if path.is_file() and not None:
                file_path ='/'.join(path.parts)
                host = args.host + '/' + file_path
                worker.new_task(args.method, host, args.success,args.stream, file_path)

                num_of_task += 1
                done = worker.num_of_done

    elif args.hosts_file:
        with open(args.hosts_file, 'r') as f:
            for url in f.readlines():
                worker.new_task(args.method, url.replace('\n',''), args.success,args.stream)
    else:
        for _ in range(args.processes):
            worker.new_task(args.method, args.host, args.success,args.stream)

    worker.join()



if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    host = parser.add_mutually_exclusive_group(required=True)
    host.add_argument('--hosts-file', dest='hosts_file', type=str)
    host.add_argument('--host', dest='host', type=str)

    parser.add_argument('--processes', dest='processes', type=int, default=1)
    parser.add_argument('--success', dest='success', type=list, default=[200])
    parser.add_argument('--input-path', dest='input_path', type=str)
    parser.add_argument('--input-type', dest='input_type', type=str)
    parser.add_argument('--method', dest='method', type=str, default='get')
    parser.add_argument('--iterations', dest='iterations', type=int, default=5)
    parser.add_argument('--stream', dest='stream', type=bool, default=False)
    parser.add_argument('--log-file', dest='log_file', type=str, default=None)
    parser.add_argument('--log-options', dest='log_options', type=str,
                        metavar=('LOGGING_TYPE', 'LOG_LEVEL'),
                        help='[LOGGING_TYPE : c = console output, f = file output, cf = console & file output]\n'
                             '[LOG_LEVEL : DEBUG, INFO, WARN, ERR, CRITICAL]',
                        nargs=2, default=['c', 'INFO'])

    main(parser.parse_args())