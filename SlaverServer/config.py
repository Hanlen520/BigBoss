import os
import structlog

logger = structlog.get_logger()


class GlobalConf:
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

    # TEMP FILES ( some error happened when using module 'tempfile', in windows
    TEMP_PY_FILE = os.path.join(PROJECT_PATH, '_temp.py')

    # SERVER SETTING
    SLAVER_SETTING = {
        'debug': True,
        'static_path': os.path.join(os.path.dirname(__file__), "static"),
        'template_path': os.path.join(os.path.dirname(__file__), "template"),
    }
    SLAVER_PORT = 9410

    # MASTER SERVER SETTING ( can be overwrite by API )
    MASTER_IP = '127.0.0.1'
    MASTER_PORT = 9507

    # STATUS
    RESULT_OK = 1000
    RESULT_ERROR = 1001


__all__ = [
    'GlobalConf',
    'logger',
]
