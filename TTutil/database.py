#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

import time
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Boolean ,Integer
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid,json

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
BaseDB = declarative_base()
BaseDB.query = db_session.query_property()


class BaseObjectDB(BaseDB):
    __abstract__=True
    uuid = Column(String(128), primary_key=True)
    alias = Column(String(128))
    create_at = Column(Integer())
    modify_at = Column(Integer())
    
    def __init__(self,uuid_prefix=None,*args,**kwargs):
        if uuid_prefix is None:
            self.uuid="%s_%s%s"%(uuid_prefix,
                                 str(uuid.uuid1())[:8],
                                 str(uuid.uuid1())[:8])
        else:
            self.uuid="%s_%s%s"%(self.__tablename__[5:],
                                 str(uuid.uuid1())[:8],
                                 str(uuid.uuid1())[:8])
        self.create_at=time.time()
    
    def __repr__(self):
        return "<%s> %s:%s"%(self.__tablename__,self.uuid,self.alias)


class BaseConfigDB(BaseObjectDB):
    __abstract__=True
    enable= Column(Boolean())
    
    def __repr__(self):
        return "<%s> %s %s:%s"%(self.__tablename__,
                                str(self.enable),
                                self.uuid,self.alias)



class BaseGlobalDB(BaseDB):
    __abstract__=True
    name = Column(String(128), primary_key=True)
    value = Column(String)
    type = Column(String(16))
    modify_at = Column(Integer())
    def __init__(self,name,value=None,type='String'):
        self.name=name
        self.value=value
        self.type=type

        
class GlobalDB(BaseGlobalDB):
    __tablename__="the_test1"
    
class Row(object):
    inputtype={
        'Json':lambda x:json.dumps(x),
    }
    outputtype={
        'Int': lambda x:int(x) ,
        'Float': lambda x:float(x) ,
        "Double": lambda x:float(x) ,
        "Json": lambda x:json.loads(x),
        "Boolean": lambda x:bool(x)
    }
    
    def value2db(self):
        if self.type in self.inputtype:
            return self.inputtype[self.type](row.value)
        return str(value)
        return 
    
    def __init__(self,key,value=None,type="String"):
        self.key=key
        self.value=value
        self.type=type
        
    def __get__(self,obj,objtype):
        print self.key
        row=obj._table.query.get(self.key)
        if row:
            if self.type in self.outputtype:        #更具类型转化
                return self.outputtype[self.type](row.value)
            return row.value
        return self
    
    def __set__(self,obj,value):
        row=obj._table.query.get(self.key)
        if row:

        else:
            raise TypeError("%s not in db"%self.key)
    
class BaseGlobalConfig(object):
    _table=GlobalDB
    _session=db_session
    def Commit(self):
        self._session.commit()

    def Init_db(self):
        for attr in dir(self):
            if isinstance(getattr(self,attr),Row):
                row=self._table(getattr(self,attr).key,
                            getattr(self,attr).value,
                            getattr(self,attr).type)
                self._session.add(row)
        self.Commit()
    
        
class NetGlobalConfig(BaseGlobalConfig):
    primary_dns=Row('primary_dns')
    slave_dns=Row('slave_dns')
    test=Row('pptp_dns',type="Json")
    pptp=Row('pptp')


    
def init_db():

    BaseDB.metadata.create_all(bind=engine)
    
    
#init_db()
#data=GlobalDB('primary_dns')
#data1=GlobalDB('slave_dns')
#db_session.add(data)
#db_session.add(data1)
#db_session.commit()

a=NetGlobalConfig()

a.Init_db()

a.test=[{"hello":'word'}]
print a.test