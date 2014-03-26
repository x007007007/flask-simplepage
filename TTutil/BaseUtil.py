#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

from flask import Blueprint,Flask,request
from validators import Validator


class Singleton(type):
    '''
    实现单体模式
    '''
    _instances = {}
    def __call__(cls, *args, **kwargs): # @NoSelf
        if cls not in cls._instances:
            cls._instances[cls] = \
            super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    

class BasePage(object):
    __metaclass__ = Singleton
    __url_prefix__=''
    __route_prefix__=''
    
    def update_func_name(self,fn='_'):
        '''
        flask 根据函数名判断是否函数被多次调用，因而更具所属的类不同，动态的
        改变函数名，防止被flask拒绝注册
        '''
        def func1(f):
            f.__name__="_%s%s%s_"%(self.__class__.__name__,
                                   fn,
                                   f.__name__.strip("_"))
            return f
        return func1
    
    def __init__(self,app=None):
        """
        如果app为None先尝试读取全局变量app
        如果均为None则抛出异常
        如果app可为blueprint或app类型，非此类型直接抛出异常
        """
        if app is None:
            if not 'app' in globals() or globals()['app'] is None:
                raise TypeError('app is Not set')
            else:
                app=globals()['app']
        if isinstance(app,Flask) or isinstance(app,Blueprint):
            self.__routeroot__=app
        else:
            raise TypeError  \
                ('app must is a instance of Flask or Blueprint')
        if not self.__url_prefix__:
            self.__url_prefix__="/"+self.__class__.__name__.lower()
        self.__init_route__()


class IntersetingData():    
    '''
    三个方法返回一个Validator对象
    '''
    def validator(self,field,fields=[],*args,**kwargs):
        value=self.getParamater(field)
        values={}
        for f in fields:
            values[f]=getParamater(f)
        return Validator(value,
                         field_name=field,
                         values=values,*args,**kwargs)
        
    def getValidator(self):
        pass
    
    def postValidator(self):
        pass


def getParamater(name,default=None):
        '''
        优先使用post数据，如果post和get都没有，使用默认设置的值
        '''
        res=default
        if name in request.form:
            res=request.form['uuid']
        if name in request.args:
            if not 'uuid' in request.form:
                res=request.args['uuid']
        return res

def classroute(url_prefix,app=None):
    def _classroute(cls):
        cls.__app__=app
        cls.__url_prefix__=url_prefix
        return cls
    return _classroute