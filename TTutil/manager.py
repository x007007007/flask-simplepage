#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

from flask import Flask,Blueprint
import simplepages


class Manager():
    def __init__(self,root):
        if not (isinstance(root,Flask) 
                or isinstance(root,Blueprint)):
            raise TypeError('not is Flask or Blueprint')
        else:
            self.__root__=root

        print simplepages
        
app=Flask(__name__)        
Manager(app)