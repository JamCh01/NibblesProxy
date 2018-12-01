# -*- coding: utf-8 -*-


class ProxyModel(object):
    def insert_attr(self, name, value):
        self.__dict__.setdefault(name, value)

    def update_attr(self, name, value):
        self.__dict__.update(name=value)

    def delete_attr(self, name):
        self.__dict__.pop(name)

    def has_attr(self, name):
        return True if name in self.__dict__.keys() else False

    def get_attr(self, name):
        return self.__dict__.get(name)