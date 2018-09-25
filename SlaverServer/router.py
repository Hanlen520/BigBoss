from handler import *


SLAVER_ROUTER = [
    (r"/", IndexHandler),
    (r"/api/device", DeviceHandler)
]
