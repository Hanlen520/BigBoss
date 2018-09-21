from tornado.web import RequestHandler
from config import *
from scanner import device_dict


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

    def get(self):
        device_dict_json = {_: v.__dict__ for _, v in device_dict.items()}
        self.end_with_json(GlobalConf.RESULT_OK, message='SERVER ALIVE :)', data=device_dict_json)
