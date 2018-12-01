# -*- coding: utf-8 -*-

import logging
from static import MYSQL_CONNECTION


class Config(object):
    THREADPOOL_NUM = 10
    MYSQL_CONNECTION = MYSQL_CONNECTION
    VALIDATED_PROXY_URL = 'https://www.baidu.com/'
    IF_USE_PROXY = True


def get_log_config():
    LOG_LEVEL = logging.WARNING
    logging.getLogger("requests").setLevel(LOG_LEVEL)
