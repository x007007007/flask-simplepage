#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 

import os,glob,importlib,flask,TTutil
importlib.sys.path.append(os.path.dirname(__file__))

blueprints=[]
classpage=[]

for filepath in glob.iglob(os.path.dirname(__file__)+"/*.py"):
    filename=".".join(os.path.basename(filepath).split('.')[:-1])
    if filename!="__init__":
        module=importlib.import_module(filename)
        if hasattr(module,"blueprint") and \
           isinstance(module.blueprint,flask.Blueprint):
            blueprints.append(module.blueprint)
        else:
            for attr in module:
                if isinstance(getattr(module,attr),TTutil.BaseDB):
                    classpage.append(getattr(module,attr))

        
        
