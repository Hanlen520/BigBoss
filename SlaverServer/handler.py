from tornado.web import RequestHandler
from config import *
from utils import *
from scanner import device_dict
from device import *


class BaseHandler(RequestHandler):
    def end_with_json(self, code, data=None, message=None):
        request_url = self.request.uri
        result_dict = {
            'code': code,
            'data': data or {},
            'message': message or {},
        }
        # RESULT_DICT 在linux上偶现问题，属于structlog的原生问题
        # logger.info('REQUEST END', request_url=request_url, **result_dict)

        logger.info('REQUEST END', request_url=request_url, **result_dict)
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


class ScriptHandler(BaseHandler):
    """ receive script and run script """

    def get(self, *args, **kwargs):
        task_id = self.get_argument('task_id', default=None)
        script_content = self.get_argument('script_content', default=None)
        temp_python_file_path = write_script(task_id, script_content)
        start_failed = run_script(task_id, temp_python_file_path)
        # TODO 规范返回
        if start_failed:
            self.end_with_json(GlobalConf.RESULT_ERROR, message=start_failed)
        else:
            self.end_with_json(GlobalConf.RESULT_OK, message='running')


class ConfHandler(BaseHandler):
    """ update conf """

    # TODO 根据参数修改配置
