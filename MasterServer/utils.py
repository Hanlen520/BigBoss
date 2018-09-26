import requests
import threading
import json
from config import *


class SlaverServer(object):
    def __init__(self, ip, status, device_dict=None):
        self.ip = ip
        self.status = status
        self.device_dict = device_dict

    def __str__(self):
        return json.dumps(self.__dict__)

    __repr__ = __str__


CURRENT_SLAVER_DICT = {
    # ip: SlaverServer Object
}

URI_DICT = {
    'device': '/api/device',
    'status': '/',
}


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


def get_server_status(request_ip):
    """
    刷新单个server的状态

    :return: if this url available
    """
    request_url = turn_ip_into_url(request_ip, 'status')
    try:
        response = requests.get(request_url, timeout=2)
    except requests.ConnectionError:
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
        response = requests.get(request_url, timeout=2)
    except requests.ConnectionError:
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


__all__ = [
    'turn_ip_into_url',
    'turn_slaver_into_json',

    'get_connected_device',
    'get_server_status',
    'sync_slaver_status',
    'sync_all_device',
]
