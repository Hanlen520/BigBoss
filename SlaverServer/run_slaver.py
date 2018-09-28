from tornado.web import Application
from tornado.ioloop import IOLoop
import argparse

from config import *
from router import SLAVER_ROUTER


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='set port')
    args = parser.parse_args()
    port = getattr(args, 'port') or GlobalConf.SLAVER_PORT

    application = Application(SLAVER_ROUTER, **GlobalConf.SLAVER_SETTING)
    application.listen(port, address='0.0.0.0')
    IOLoop.instance().start()
