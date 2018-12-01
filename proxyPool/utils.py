import requests
import threadpool
from config import Config
from requests.adapters import HTTPAdapter
from multiprocessing.dummy import Pool


class Requster(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.timeout = 5
        self.threadnum = Config.THREADPOOL_NUM
        self.validated_proxy_url = Config.VALIDATED_PROXY_URL

    def get(self, url, **kwargs):
        response = self.session.get(url=url, timeout=self.timeout, **kwargs)
        return response

    def filter_proxy(self, models):
        filters = Filter()
        pool = Pool(processes=Config.THREADPOOL_NUM)
        res = pool.map_async(filters.filter_func, models)
        res.wait()
        return filters.result

    def save_filter_proxy(self, request, filer_model):
        pass


class Filter(Requster):
    def __init__(self):
        super(Filter, self).__init__()
        self.collection = list()

    def filter_func(self, model):
        protocal = model.get_attr(name='protocal')
        ip = model.get_attr(name='ip')
        port = model.get_attr(name='port')
        proxies = dict(protocal='{protocal}://{ip}:{port}'.format(
            protocal=protocal.lower(), ip=ip, port=str(port)))
        res = self.get(url=self.validated_proxy_url, proxies=proxies)
        if res.status_code == 200:
            self.collection.append(model)

    @property
    def result(self):
        return self.collection


class Spider(object):
    headers = dict()
    url = str()
    requester = Requster()

    @classmethod
    def get_proxies(self):
        response = self.requester.get(url=self.url, headers=self.headers)
        return response