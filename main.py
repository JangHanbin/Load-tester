import argparse
from worker import Worker
from reporter.logger import Logger
def main(args):
    if args.log_file is None:
        logger = Logger(args.log_options[0], args.log_options[1])
    else:
        logger = Logger(args.log_options[0], args.log_options[1], args.ㅣㅐㅎ_랴ㅣㄷ)

    if args.input_path is None and args.request_type == 'put':
        raise ValueError('PUT method needs --input-path option')


    worker = Worker(args.request_type, args.host, args.success, args.processes)
    worker.subscribe('reporters', logger)
    worker.start()

    worker.join()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--processes', dest='processes', type=int, default=1)
    parser.add_argument('--host', dest='host', type=str, required=True)
    parser.add_argument('--success', dest='success', type=list, default=[200])
    parser.add_argument('--input-path', dest='input_path', type=str)
    parser.add_argument('--request-type', dest='request_type', type=str, default='get')
    parser.add_argument('--log-file', dest='log_file', type=str, default=None)
    parser.add_argument('--log-options', dest='log_options', type=str,
                        metavar=('LOGGING_TYPE', 'LOG_LEVEL'),
                        help='[LOGGING_TYPE : c = console output, f = file output, cf = console & file output]\n'
                             '[LOG_LEVEL : DEBUG, INFO, WARN, ERR, CRITICAL]',
                        nargs=2, default=['c', 'INFO'])

    main(parser.parse_args())