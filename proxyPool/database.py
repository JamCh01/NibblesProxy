# -*- coding: utf-8 -*-
from config import Config
from tables import ProxyTemplate
from sqlalchemy import create_engine, func, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database(object):
    def __init__(self):
        engine = create_engine(Config.MYSQL_CONNECTION, echo=True)
        Base = declarative_base()
        self.proxy_table = type('proxy', (Base, ProxyTemplate),
                                {'__tablename__': 'proxy'})
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def insert_models(self, model):
        self.session.add(
            self.proxy_table(
                ip=model.get_attr(name='ip'),
                port=model.get_attr(name='port'),
                protocal=model.get_attr(name='protocal'),
                area=model.get_attr(name='area'),
                anonymity=model.get_attr(name='anonymity')))
        self.session.commit()

    def count(self):
        _count = self.session.query(func.count(self.proxy_table.id)).scalar()
        return _count

    def random(self):
        res = self.session.query(self.proxy_table).order_by(
            func.rand()).first()
        return res

    def fail(self, ip):
        if ip is not None:
            row = self.session.query(ip=ip).first()
            fail_times = row.failed_count
            if fail_times > 3:
                row.delete()
            else:
                row.failed_count += 1
            self.session.commit()
        else:
            pass
