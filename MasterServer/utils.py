import requests
import threading
import json
import os
import uuid
from config import *


class SlaverServer(object):
    def __init__(self, ip, status, device_dict=None):
        self.ip = ip
        self.status = status
        self.device_dict = device_dict

    def __str__(self):
        return json.dumps(self.__dict__)

    __repr__ = __str__


# TODO 与device的关联
class Task(object):
    def __init__(self, task_id, ip, status, exec_result=None):
        self.task_id = task_id
        self.ip = ip
        self.status = status
        self.exec_result = exec_result


CURRENT_SLAVER_DICT = {
    # ip: SlaverServer Object
}

TASK_STATUS_DICT = {
    # task id: status
    # status should be 'running' or 'done'
}

URI_DICT = {
    # android device status
    'device': '/api/device/status',
    # server status, just confirm it is reachable
    'status': '/',
    # exec script
    'exec': '/api/script'
}


# --- tools ---

def set_task_status(task_id, exec_result, status):
    if task_id in TASK_STATUS_DICT:
        TASK_STATUS_DICT[task_id].exec_result = exec_result
        TASK_STATUS_DICT[task_id].status = status
        return True
    return False


def turn_ip_into_url(ip_address, request_type=None):
    result_url = 'http://{ip}:{port}'.format(
        ip=ip_address,
        port=GlobalConf.SLAVER_PORT,
    )
    if request_type in URI_DICT:
        return result_url + URI_DICT[request_type]
    return result_url


def turn_slaver_into_json(slaver_object):
    return json.loads(str(slaver_object))


def get_script_content(script_name):
    if script_name and script_name in os.listdir(GlobalConf.SCRIPT_DIR_PATH):
        script_path = os.path.join(GlobalConf.SCRIPT_DIR_PATH, script_name)
        with open(script_path, encoding='utf-8') as f:
            script_content = f.read()
        return script_content
    return None


def get_task_id():
    return str(uuid.uuid1().int)


# --- communication ---

def get_server_status(request_ip):
    """
    刷新单个server的状态

    :return: if this url available
    """
    request_url = turn_ip_into_url(request_ip, 'status')
    try:
        response = requests.get(request_url, timeout=2)
    except requests.ConnectionError:
        del CURRENT_SLAVER_DICT[request_ip]
        return False
    server_status = response.ok
    if request_ip in CURRENT_SLAVER_DICT:
        CURRENT_SLAVER_DICT[request_ip].status = server_status
    else:
        CURRENT_SLAVER_DICT[request_ip] = SlaverServer(request_ip, server_status)
    return turn_slaver_into_json(CURRENT_SLAVER_DICT[request_ip])


def get_connected_device(request_ip):
    """
    刷新单个server的设备连接状态

    :param request_ip:
    :return:
    """
    request_url = turn_ip_into_url(request_ip, 'device')
    try:
        response = requests.get(request_url, timeout=5)
    except requests.ConnectionError:
        if request_ip in CURRENT_SLAVER_DICT:
            del CURRENT_SLAVER_DICT[request_ip]
        return False
    device_dict = json.loads(response.text)
    if request_ip in CURRENT_SLAVER_DICT:
        CURRENT_SLAVER_DICT[request_ip].device_dict = device_dict
    else:
        CURRENT_SLAVER_DICT[request_ip] = SlaverServer(request_ip, response.ok, device_dict)
    return turn_slaver_into_json(CURRENT_SLAVER_DICT[request_ip])


def sync_all_device():
    """
    刷新所有slaver的设备连接状态

    :return:
    """
    thread_list = []
    for each_slaver in GlobalConf.SLAVER_PC_LIST:
        current_thread = threading.Thread(target=get_connected_device, args=(each_slaver,))
        current_thread.start()
        thread_list.append(current_thread)

    for each_thread in thread_list:
        each_thread.join()

    return CURRENT_SLAVER_DICT


def sync_slaver_status():
    """
    刷新所有slaver server的状态

    :return:
    """
    thread_list = []
    for each_slaver in GlobalConf.SLAVER_PC_LIST:
        current_thread = threading.Thread(target=get_server_status, args=(each_slaver,))
        current_thread.start()
        thread_list.append(current_thread)

    for each_thread in thread_list:
        each_thread.join()

    return CURRENT_SLAVER_DICT


def exec_script(request_ip, script_name):
    """
    send script and run it on slaver server

    :param request_ip:
    :param script_name:
    :return:
    """
    script_content = get_script_content(script_name)
    if not script_content:
        logger.warn('NO SCRIPT')
        return False
    request_url = turn_ip_into_url(request_ip, 'exec')

    # save task
    task_id = get_task_id()

    try:
        response = requests.get(
            request_url,
            params={
                'task_id': task_id,
                'script_content': script_content,
            },
            timeout=5
        )
    except requests.ConnectionError:
        logger.info('CONNECTION FAILED', ip=request_ip)
        del CURRENT_SLAVER_DICT[request_ip]
        return False
    exec_result = response.text
    # TODO: use json rather than str
    # TODO: different status
    if 'running' in exec_result:
        TASK_STATUS_DICT[task_id] = Task(task_id, request_ip, 'running')

    return task_id, exec_result


def get_task_status(task_id):
    print(TASK_STATUS_DICT)
    if task_id in TASK_STATUS_DICT:
        return TASK_STATUS_DICT[task_id].status
    return None


__all__ = [
    'turn_ip_into_url',
    'turn_slaver_into_json',
    'get_script_content',
    'get_task_status',
    'set_task_status',

    'get_connected_device',
    'get_server_status',
    'sync_slaver_status',
    'sync_all_device',
    'exec_script',
]
