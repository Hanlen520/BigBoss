from tornado.web import RequestHandler
from config import *
from utils import *


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def end_with_json(self, code, data=None, message=None):
        request_url = self.request.uri
        result_dict = {
            'code': code,
            'data': data or {},
            'message': message or {},
        }
        # RESULT_DICT 在linux上偶现问题，属于structlog的原生问题
        # logger.info('REQUEST END', request_url=request_url, **result_dict)

        logger.info('REQUEST END', request_url=request_url)
        self.finish(result_dict)

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class IndexHandler(BaseHandler):
    """ default """

    def get(self, *args, **kwargs):
        self.end_with_json(GlobalConf.RESULT_OK, message='SERVER ALIVE :)')


class DeviceHandler(BaseHandler):
    """ get connected devices from different PC """

    def get(self, *args, **kwargs):
        current_device_dict = sync_slaver_server()
        self.end_with_json(GlobalConf.RESULT_OK, data=current_device_dict)