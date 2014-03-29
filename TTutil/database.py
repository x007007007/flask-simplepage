#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

import time
from sqlalchemy import create_engine
from sqlalchemy import Column, String, TIMESTAMP, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
BaseDB = declarative_base()
BaseDB.query = db_session.query_property()


class BaseObjectDB(BaseDB):
    uuid = Column(String(128), primary_key=True)
    alias = Column(String(128))
    create_at = Column(TIMESTAMP())
    modify_at = Column(TIMESTAMP())
    
    def __init__(self,*args,**kwargs):
        self.uuid="..."
        self.create_at=time.time()


class BaseConfigDB(BaseObjectDB):
    enable= Column(Boolean())


def init_db():


    BaseDB.metadata.create_all(bind=engine)