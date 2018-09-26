from tornado.web import Application
from tornado.ioloop import IOLoop

import time
import requests
import threading
import argparse

from config import *
from router import SLAVER_ROUTER


def test_ping(delay, target_port):
    time.sleep(delay)
    response = requests.get(
        url='http://localhost:{}'.format(target_port),
    )
    if response.ok:
        return
    raise ConnectionError('server start failed :(')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='set port')
    args = parser.parse_args()
    port = getattr(args, 'port') or GlobalConf.SLAVER_PORT

    # stable check
    logger.info('STARTING SLAVER ...')
    threading.Thread(target=test_ping, args=(2, port)).start()

    application = Application(SLAVER_ROUTER, **GlobalConf.SLAVER_SETTING)
    application.listen(port, address='0.0.0.0')
    IOLoop.instance().start()
