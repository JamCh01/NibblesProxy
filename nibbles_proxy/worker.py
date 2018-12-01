# -*- coding: utf-8 -*-
import random
import importlib
from functools import wraps
from utils import Requster
from spiders import __spiders__
from apscheduler.schedulers.background import BackgroundScheduler
from database import Database


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


@singleton
class Worker(object):
    __MIN_PROXY_NUM = 15

    def __init__(self):
        self.requster = Requster()
        self.database = Database()

    def start_work(self):
        pass

    def import_spider(self, class_name):
        return getattr(importlib.import_module('spiders'), class_name)

    def crawl(self):
        spider_name = random.choice(__spiders__)
        spider = self.import_spider(class_name=spider_name)
        crawl_result = spider.parse()
        filtered_models = self.requster.filter_proxy(models=crawl_result)
        for item in filtered_models:
            self.database.insert_models(model=item)

    def random_item(self):
        proxy = self.database.random()
        return '{protocal}://{ip}:{port}'.format(
            protocal=proxy.protocal, ip=proxy.ip, port=proxy.port)

    def fail(self, ip):
        self.database.fail(ip=ip)

    def stop(self):
        self.database.close()


def _worker():
    return Worker()
