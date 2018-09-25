import os
import structlog

logger = structlog.get_logger()


class GlobalConf:
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

    # SLAVER SETTING
    # CONFIGURE SLAVER IP HERE
    SLAVER_PC_LIST = [
        # TEST ONLY
        '127.0.0.1',

        # and so on
    ]
    SLAVER_PORT = 9410

    # MASTER SETTING
    MASTER_SETTING = {
        'debug': True,
        'static_path': os.path.join(os.path.dirname(__file__), "static"),
        'template_path': os.path.join(os.path.dirname(__file__), "template"),
    }
    MASTER_PORT = 9507

    # STATUS
    RESULT_OK = 1000
    RESULT_ERROR = 1001


__all__ = [
    'GlobalConf',
    'logger',
]
