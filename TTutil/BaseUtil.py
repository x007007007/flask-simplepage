#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

from flask import Blueprint,Flask,request
#from validators import Validator


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
        
    def getValidator(self,feild,default=None,is_list=False):
        pass
 
    
    def postValidator(self):
        pass


def paramater(field,default=None,is_list=False,
              marge=True,postfirst=True):
    """
    
    """
    if postfirst:
        first=request.form;second=request.args
    else:
        first=request.args;second=request.form
    if is_list:
        if marge:
            if field in first:
                if field in second:
                    return first.getlist(field)+second.getlist(field)
                else:
                    return first.getlist(field)
            elif field in second:
                return second.getlist(field)
            else:
                return default
        else:
            return first.getlist(field) \
                   if field in first else default
    else:
        if field in first:
            return first[field]
        elif field in second:
            return second[field]
        else:
            return None
        
def getParamater(field,default=None,is_list=False):
    '''
        返回get数据
    '''
    if is_list: 
        return request.args.getlist(field) \
            if field in request.args else default
    return request.args[field] if field in request.args else default
    
def postParamater(field,default=None,is_list=False):
    '''
        返回get数据
    '''
    if is_list: 
        return request.form.getlist(field) \
            if field in request.form else default
    return request.form[field] if field in request.form else default


def classroute(url_prefix,app=None):
    def _classroute(cls):
        cls.__app__=app
        cls.__url_prefix__=url_prefix
        return cls
    return _classroute