from tornado.web import RequestHandler
from config import *
from utils import *


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
    """ get connected devices, from all server or one """

    def get(self, *args, **kwargs):
        target_server_ip = self.get_argument('target_ip', default=None)
        if target_server_ip:
            device_result = get_connected_device(target_server_ip)
            self.end_with_json(GlobalConf.RESULT_OK, data=device_result)
            return
        current_device_dict = {_: turn_slaver_into_json(v) for _, v in sync_all_device().items()}
        self.end_with_json(GlobalConf.RESULT_OK, data=current_device_dict)


class SlaverServerHandler(BaseHandler):
    """ get slaver server status, all or one """

    def get(self, *args, **kwargs):
        target_server_ip = self.get_argument('target_ip', default=None)
        if target_server_ip:
            server_result = get_server_status(target_server_ip)
            self.end_with_json(GlobalConf.RESULT_OK, data=server_result)
            return
        current_slaver_dict = {_: turn_slaver_into_json(v) for _, v in sync_slaver_status().items()}
        self.end_with_json(GlobalConf.RESULT_OK, data=current_slaver_dict)


class TaskHandler(BaseHandler):
    """ send task (runnable python script) to slaver """
    # TODO unittest

    def get(self, *args, **kwargs):
        """ get task status """
        task_id = self.get_argument('task_id', default='INVALID_TASK_ID')
        task_status = get_task_status(task_id)
        if task_status:
            self.end_with_json(GlobalConf.RESULT_OK, data=task_status)
            return
        self.end_with_json(GlobalConf.RESULT_ERROR, message='task id not found')

    def post(self, *args, **kwargs):
        """ new task and run """
        script_name = self.get_argument('script_name', default=None)
        target_server_ip = self.get_argument('target_ip', default=None)

        task_id, exec_result = exec_script(target_server_ip, script_name)
        result_dict = {
            'result': exec_result,
            'task_id': task_id,
        }
        self.end_with_json(GlobalConf.RESULT_OK, data=result_dict)
