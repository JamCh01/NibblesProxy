# -*- coding: utf-8 -*-
import re
from worker import _worker


class ProxyMiddlewares(object):
    def process_request(self, request, spider):
        proxy_address = _worker().random_item()
        request.meta['proxy'] = proxy_address

    def process_exception(self, request, exception, spider):
        pass


class ExceptionMiddleware(object):
    def __init__(self):
        self.ip_regex = re.compile(
            r'((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))'
        )

    def process_exception(self, request, exception, spider):
        try:
            ip = self.ip_regex.search(string=request.meta['proxy']).group()
            _worker().fail(ip=ip)
        except Exception as e:
            print(e)

    def process_responce(self, request, response, spider):
        if response.staus < 200 or response.staus >= 400:
            try:
                ip = self.ip_regex.search(string=request.meta['proxy']).group()
                _worker().fail(ip=ip)
            except Exception as e:
                print(e)
        return response


class RetryMiddleware(object):
    def __init__(self):
        self.ip_regex = re.compile(
            r'((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))'
        )

    def process_exception(self, request, exception, spider):
        try:
            ip = self.ip_regex.search(string=request.meta['proxy']).group()
            _worker().fail(ip=ip)
        except Exception as e:
            print(e)

    def process_responce(self, request, response, spider):
        if response.staus < 200 or response.staus >= 400:
            try:
                ip = self.ip_regex.search(string=request.meta['proxy']).group()
                _worker().fail(ip=ip)
            except Exception as e:
                print(e)
        return response
