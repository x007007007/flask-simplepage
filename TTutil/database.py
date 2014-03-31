#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

import time
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Boolean ,Integer
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

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


class TestConfigData(BaseConfigDB):
    __tablename__="test"
    data=Column(String())
    def __init__(self,data="helloworld",*args,**kwargs):
        super(BaseConfigDB,self).__init__(*args,**kwargs)
        self.data=data
    
data=TestConfigData("xxc")




def init_db():

    BaseDB.metadata.create_all(bind=engine)
    
    
#init_db()
data=TestConfigData("xxc")
db_session.add(data)
db_session.commit()