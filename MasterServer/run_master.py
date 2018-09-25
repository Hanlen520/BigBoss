from tornado.web import Application
from tornado.ioloop import IOLoop

import time
import requests
import threading

from config import *
from router import SLAVER_ROUTER


def ping(delay):
    time.sleep(delay)
    response = requests.get(
        url='http://localhost:{}'.format(GlobalConf.MASTER_PORT),
    )
    if response.ok:
        return
    raise ConnectionError('server start failed :(')


if __name__ == "__main__":
    # stable check
    logger.info('STARTING MASTER ...')
    threading.Thread(target=ping, args=(3,)).start()

    application = Application(SLAVER_ROUTER, **GlobalConf.MASTER_SETTING)
    application.listen(GlobalConf.MASTER_PORT, address='0.0.0.0')
    IOLoop.instance().start()
