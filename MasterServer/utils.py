import requests
import threading
import json
from config import *


CURRENT_DEVICE_DICT = {
    # ip : device dict
}


def get_connected_device(request_ip, request_url):
    """
    get device list from slaver

    :param request_ip:
    :param request_url:
    :return:
    """
    logger.info('GET DEVICE', url=request_url)
    response = requests.get(request_url)
    device_dict = json.loads(response.text)
    logger.info('DEVICE DICT', ip=request_ip, device=device_dict)
    CURRENT_DEVICE_DICT[request_ip] = device_dict


def sync_slaver_server():
    request_url_template = 'http://{ip}:{port}/api/device'
    slaver_port = GlobalConf.SLAVER_PORT
    thread_list = []

    for each_slaver in GlobalConf.SLAVER_PC_LIST:
        request_url = request_url_template.format(
            ip=each_slaver,
            port=slaver_port,
        )
        current_thread = threading.Thread(target=get_connected_device, args=(each_slaver, request_url,))
        current_thread.start()
        thread_list.append(current_thread)

    for each_thread in thread_list:
        each_thread.join()

    logger.info('DEVICE DICT', device=CURRENT_DEVICE_DICT)
    return CURRENT_DEVICE_DICT


__all__ = [
    'sync_slaver_server',
]
