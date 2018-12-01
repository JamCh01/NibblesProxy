# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, BIGINT


class ProxyTemplate():
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(BIGINT, nullable=False, comment='代理IP地址')
    port = Column(Integer, nullable=False, comment='代理端口')
    protocal = Column(String(6), comment='代理协议')
    area = Column(String(256), comment='代理区域')
    anonymity = Column(String(25), comment='代理匿名性')
    failed_count = Column(Integer, default=0, comment='失效次数')

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
