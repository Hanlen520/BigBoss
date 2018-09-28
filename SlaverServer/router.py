from handler import *


SLAVER_ROUTER = [
    (r"/", IndexHandler),
    (r"/api/device/status", DeviceStatusHandler),
    (r"/api/device/command", DeviceCommandHandler),
    (r"/api/script", ScriptHandler),
    (r"/api/configure", ConfHandler),
]
