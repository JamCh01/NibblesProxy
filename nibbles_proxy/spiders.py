# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from lxml import etree
from model import ProxyModel
from utils import Spider
__spiders__ = ['Data5uSpider', 'XiciSpider', 'KuaidailiSpider']


class Data5uSpider(Spider):
    url = 'http://www.data5u.com/free/gngn/index.shtml'
    agent = "data5u"
    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language':
        'zh-CN,zh;q=0.8',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Referer':
        'http://www.data5u.com/free/gngn/index.shtml',
        'Content-Type':
        'text/html;charset=UTF-8',
        'Cache-Control':
        'no-cache',
        'Host':
        'www.data5u.com',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    @classmethod
    def parse(self):
        proxy_model_list = list()
        res = super(Data5uSpider, self).get_proxies().text
        soup = BeautifulSoup(markup=res, features='lxml')
        items = soup.find_all(name='ul', attrs={'class': 'l2'})
        for item in items:
            attrs = item.find_all(name='li')
            ip = attrs[0].text
            port = attrs[1].text
            anonymity = attrs[2].text
            protocal = attrs[3].text
            area = attrs[5].text
            speed = attrs[7].text
            if protocal in {'http', 'https'}:
                proxy = ProxyModel()
                proxy.insert_attr(name='ip', value=ip)
                proxy.insert_attr(name='port', value=port)
                proxy.insert_attr(name='anonymity', value=anonymity)
                proxy.insert_attr(name='protocal', value=protocal)
                proxy.insert_attr(name='area', value=area)
                proxy.insert_attr(name='speed', value=speed)
                proxy_model_list.append(proxy)
                # print(proxy.ip, proxy.port, proxy.anonymity, proxy.protocal,
                #       proxy.area, proxy.speed)

        return proxy_model_list


class KuaidailiSpider(Spider):
    url = 'http://www.kuaidaili.com/free'
    agent = "kuaidaili"
    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language':
        'zh-CN,zh;q=0.8',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Referer':
        'http://www.kuaidaili.com/free',
        'Content-Type':
        'text/html;charset=UTF-8',
        'Cache-Control':
        'no-cache',
        'Host':
        'www.kuaidaili.com',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
    pattern = re.compile(
        '<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>('
        '.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>',
        re.S)

    @classmethod
    def parse(self):
        proxy_model_list = list()
        res = super(KuaidailiSpider, self).get_proxies().text
        items = re.findall(self.pattern, res)
        for item in items:
            ip, port, anonymity, protocal, area, speed, _ = item
            if protocal.lower() in {'http', 'https'}:
                proxy = ProxyModel()
                proxy.insert_attr(name='ip', value=ip)
                proxy.insert_attr(name='port', value=port)
                proxy.insert_attr(name='anonymity', value=anonymity)
                proxy.insert_attr(name='protocal', value=protocal.lower())
                proxy.insert_attr(name='area', value=area)
                proxy.insert_attr(name='speed', value=speed)
                proxy_model_list.append(proxy)
        return proxy_model_list


class XiciSpider(Spider):
    url = 'http://www.xicidaili.com/wn/'
    agent = "xici"
    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language':
        'zh-CN,zh;q=0.8',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Referer':
        'http://www.xicidaili.com/wn',
        'Content-Type':
        'text/html;charset=UTF-8',
        'Cache-Control':
        'no-cache',
        'Host':
        'www.xicidaili.com',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    @classmethod
    def parse(self):
        proxy_model_list = list()
        res = super(XiciSpider, self).get_proxies().text
        selector = etree.HTML(res)
        items = selector.xpath('//tr[@class="odd"]')
        for item in items:
            ip = item.xpath('./td[2]/text()')[0]
            port = item.xpath('./td[3]/text()')[0]
            anonymity = item.xpath('./td[5]/text()')[0]
            protocal = item.xpath('./td[6]/text()')[0].lower()
            try:
                area = item.xpath('./td[4]/a/text()')[0]
            except Exception:
                area = None
            speed = item.xpath('./td[7]/div/@title')[0]
            if protocal in {'http', 'https'}:
                proxy = ProxyModel()
                proxy.insert_attr(name='ip', value=ip)
                proxy.insert_attr(name='port', value=port)
                proxy.insert_attr(name='anonymity', value=anonymity)
                proxy.insert_attr(name='protocal', value=protocal)
                proxy.insert_attr(name='area', value=area)
                proxy.insert_attr(name='speed', value=speed)
                proxy_model_list.append(proxy)
        return proxy_model_list
