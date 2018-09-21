from whenconnect import when_connect, when_disconnect, start_detect
from config import *
import warnings
import time


class AndroidDevice(object):
    """
    device item

    device id: primary key for this device
    device status: 'busy' or 'free'
    device info: relative info to describe this device
    """
    DEVICE_STATUS_DICT = {
        'busy': 'BUSY',
        'free': 'FREE',
    }

    def __init__(self, device_id: str, device_status: str, device_info: dict):
        self.device_id = device_id
        self.device_status = self.DEVICE_STATUS_DICT[device_status]
        self.device_info = device_info

    def __hash__(self):
        return hash(self.device_id)

    def __str__(self):
        return '<Android Device: {}>'.format(self.device_id)

    def set_status(self, target_status):
        if target_status not in self.DEVICE_STATUS_DICT:
            warnings.warn('status not supported: {}'.format(target_status))
            raise KeyError('error status')
        self.device_status = self.DEVICE_STATUS_DICT[target_status]


device_dict = dict()


def add_device(device: str):
    new_device = AndroidDevice(device, 'free', {'device_name': 'TEST ONLY'})
    device_dict[device] = new_device
    logger.info('ADD DEVICE', device=device)


def remove_device(device: str):
    del device_dict[device]
    logger.info('REMOVE DEVICE', device=device)


start_detect(with_log=False)
when_connect(device='any', do=add_device)
when_disconnect(device='any', do=remove_device)


if __name__ == '__main__':
    while True:
        time.sleep(1)
        print(device_dict)
