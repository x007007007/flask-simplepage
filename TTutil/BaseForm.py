#!/usr/bin/python2.7
# -*- coding:utf8 -*-
# vim : set fileencoding=utf8 :

from wtforms import Form as BaseForm ,validators,TextField,BooleanField# @UnresolvedImport


class BaseObjectForm(BaseForm): 
    uuid= TextField('uuid', [validators.Length(min=32, max=128)])
    alias= TextField('alias', [validators.Length(min=1, max=128)])
    

class BaseConfigForm(BaseObjectForm): 
    enable= BooleanField('enable')