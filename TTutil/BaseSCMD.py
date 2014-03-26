#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

from BaseUtil import BasePage,IntersetingData
from flask import request
import json





class BaseSCMD(BasePage):
    """
        基本的增删改查页面
        
    """
    __field__=([],{})       #json字段到数据库字段的映射
    __can_modify__=True
    __can_search__=True
    __can_create__=True
    __can_delete__=True
    __can_batch__ =True
    __ajax_validate__=True
    
    def __init_route__(self):
        '''
            
        '''
        if self.__can_search__ :
            @self.__routeroot__.route \
            (self.__route_prefix__ + "/list")
            @self.__routeroot__.route \
            (self.__route_prefix__ + "/search",methods=['GET'])
            @self.update_func_name()
            def __search__():
                rule=self.getParamater('q')
                res=self.search(rule,
                                None,            #post
                                request.args,    #get
                                request.files)
                return json.dumps(res)
                        
        if self.__can_create__ :
            @self.__routeroot__.route \
            (self.__route_prefix__ +  "/add",methods=['GET', 'POST'])
            @self.__routeroot__.route \
            (self.__route_prefix__ +"/create",methods=['GET','POST'])
            @self.update_func_name()
            def __create__():
                
                
                
                return self.create(IntersetingData(),
                                   request.form,
                                   request.args)
        
        if self.__can_modify__ :
            @self.__routeroot__.route \
            (self.__route_prefix__ + "/edit",methods=['GET', 'POST'])
            @self.__routeroot__.route \
            (self.__route_prefix__ +"/modify",methods=['GET','POST'])
            @self.update_func_name()
            def __modify__():
                uuid=self.getParamater('uuid')
                #print request.file
                return self.modify(uuid,
                                   {},
                                   post=request.form,
                                   get=request.args,
                                   file=request.files)
        
        if self.__can_delete__ :
            @self.__routeroot__.route \
            (self.__route_prefix__ +"/remove",methods=['GET','POST'])
            @self.__routeroot__.route \
            (self.__route_prefix__ +"/delete",methods=['GET','POST'])
            @self.update_func_name()
            def __delete__():
                uuid=self.getParamater('uuid')
                return self.delete(uuid)
    
        if self.__can_batch__ :
            @self.__routeroot__.route \
            (self.__route_prefix__ +"/batch",methods=['GET','POST'])
            @self.__routeroot__.route \
            (self.__route_prefix__ +"/more",methods=['GET','POST'])
            @self.update_func_name()
            def __batch__():
                uuid    =self.getParamater('uuid')
                action  =self.getParamater('action')
                return self.batch(uuid,action)
    
    def __get_data__(self):
        errlist={}
        for s,v,m in filter(IntersetingData()):
            if s :
                pass
            else:
                False
                
    
    def filter(self,data):
        data=IntersetingData()
        yield data.validator('test').Not().isEmpty("hahah");
        
    
    def modify_filter(self,uuid,data,post=None,get=None,f=None):
        return self.filter(data)

    def search(self,rule,post=None,get=None,f=None):
        return "search!!"
    
    def modify(self,uuid,data,post=None,get=None,f=None):
        data=self.modify_filter(uuid,data)
        return "modify"
    
    def create(self,data,post=None,get=None,f=None):
        return "create"
    
    def delete(self,uuid):
        return "delete"

    def batch(self,uuids,action):
        return 'batch'
    
