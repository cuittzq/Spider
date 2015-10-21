# coding=utf-8
__author__ = 'tzq'

class MBaseModel(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
