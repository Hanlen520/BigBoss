import os
import structlog

logger = structlog.get_logger()


class GlobalConf:
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

    # SERVER SETTING
    SLAVER_SETTING = {
        'debug': True,
        'static_path': os.path.join(os.path.dirname(__file__), "static"),
        'template_path': os.path.join(os.path.dirname(__file__), "template"),
    }
    SLAVER_PORT = 9410

    # STATUS
    RESULT_OK = 1000
    RESULT_ERROR = 1001


__all__ = [
    'GlobalConf',
    'logger',
]
