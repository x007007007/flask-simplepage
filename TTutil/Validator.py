#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

from BaseUtil import getParamater,postParamater,paramater

class ValidatorMeta(type): 
    def __call__(cls,*args,**kwargs): # @NoSelf
        if cls not in cls._instances:
            cls._instances[cls] = \
            super(ValidatorMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
        
        
class BaseValidator(object):
    """
        没个域使用同一个Validator，
    """
    rawvalue=None #原始值
    value=None  #最终值
    field=None  #域名
    msg=""

    __is_list__=False
    __post__=True
    __get__=True
    __first_post__=True
    __post_get_marge__=True
    
    __continue__=True  #如果被设置为False停止方法链
    
    def __init__(self,field):
        self.field=field
        self.__reflash_value__()
    
    def __reflash_value__(self):
        if self.__post__ and self.__get__ :
            self.value=paramater(self.field,
                                 is_list=self.__is_list__,
                                 marge=self.__post_get_marge__,
                                 postfirst=self.__first_post__)
        elif self.__post__ :
            self.value=postParamater(self.field,
                                     is_list=self.__is_list__)
        else :
            self.value=getParamater(self.field,
                                     is_list=self.__is_list__)
        
        
    def foreach(self):
        if not self.__is_list__ :
            self.__is_list__=True
            self.__reflash_value__()
        
        
    def myself(self): return self
        
    def __str__(self): return str(self.value)
    def __bool__(self): return bool(self.value)
    def __int__(self): return int(self.value)
    def __float__(self): return float(self.value)
    
    