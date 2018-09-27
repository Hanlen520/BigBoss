from tornado.web import RequestHandler
from config import *
from scanner import device_dict
from device import *


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


class DeviceStatusHandler(BaseHandler):
    """ get current device list in this PC """

    def get(self, *args, **kwargs):
        device_dict_json = {_: v.__dict__ for _, v in device_dict.items()}
        self.end_with_json(GlobalConf.RESULT_OK, data=device_dict_json)


class DeviceCommandHandler(BaseHandler):
    """ apply command on devices """

    def get(self, *args, **kwargs):
        cmd_str = self.get_argument('adb_cmd', default=None)
        if cmd_str:
            device = self.get_argument('device', default=None)
            on_shell = self.get_argument('shell', default=None)
            cmd_list = cmd_str.split(' ')
            exec_result = exec_adb_cmd(cmd_list, device, on_shell)
            self.end_with_json(GlobalConf.RESULT_OK, data=exec_result)
            return
        self.end_with_json(GlobalConf.RESULT_ERROR, message='invalid args')
