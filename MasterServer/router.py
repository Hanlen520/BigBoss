from handler import *


MASTER_ROUTER = [
    (r"/", IndexHandler),
    # connected devices
    (r"/api/device", DeviceHandler),
    # available slaver server
    (r"/api/slaver", SlaverServerHandler),
]
