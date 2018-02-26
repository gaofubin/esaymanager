#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-14 0014 10:15
# @Author  : All is well
# @Site    : 
# @File    : urls.py.py
# @Software: PyCharm

from django.conf.urls import url,include
from deploy import views

urlpatterns = [
    #salt_key_list
    url(r'^salt_key_list/', views.salt_key_list,name='salt_key_list'),
    url(r'^salt_key_update/', views.salt_key_update,name='salt_key_update'),
    url(r'^salt_key_accept/', views.salt_key_accept,name='salt_key_accept'),
    url(r'^salt_key_delete/', views.salt_key_delete,name='salt_key_delete'),
    url(r'^salt_command/', views.salt_command,name='salt_command'),
]
