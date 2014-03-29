#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

from flask import request
from wtforms import TextField, PasswordField, validators # @UnresolvedImport
from sqlalchemy import Column, String
from TTutil import BaseSCMD, BaseObjectDB, BaseObjectForm


class Form(BaseObjectForm): 
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class Data(BaseObjectDB):
    __tablename__='test'
    email = Column(String(128), unique=True)
    password = Column(String(128))
    
    def init(self,email,password):
        self.email=email
        self.password=password
    

class Main(BaseSCMD):
    def create(self,*args,**kwargs):
        form = Form(request.values)
        if form.validate():
            pass
        

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    