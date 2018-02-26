#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-5 0005 15:42
# @Author  : All is well
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from django.conf.urls import url,include
from cmdb import views

urlpatterns = [
    #云商
    url(r'^cloud_list/', views.cloud_list,name='cloud_list'),
    url(r'^cloud_add/', views.cloud_add,name='cloud_add'),
    url(r'^cloud_edit-(\d+)/', views.cloud_edit,name='cloud_edit'),
    url(r'^cloud_del/', views.cloud_del,name='cloud_del'),
    #项目
    url(r'^pro_list/', views.pro_list,name='pro_list'),
    url(r'^pro_add/', views.pro_add,name='pro_add'),
    url(r'^pro_edit-(\d+)/', views.pro_edit,name='pro_edit'),
    url(r'^pro_del/', views.pro_del,name='pro_del'),

    #主机
    url(r'^host_list-(?P<cloud_name_id>\d+)-(?P<project_name_id>\d+)-(?P<status>\d+)/', views.host_list,name='host_list'),
    url(r'^host_edit-(\d+)/', views.host_edit,name='host_edit'),
    url(r'^host_del/', views.host_del,name='host_del'),
    url(r'^host_add/', views.host_add,name='host_add'),
    url(r'^host_select_update/', views.host_select_update,name='host_select_update'),

    #数据库
    url(r'^sql_list-(?P<cloud_name_id>\d+)-(?P<project_name_id>\d+)-(?P<status>\d+)/', views.sql_list,name='sql_list'),
    url(r'^sql_edit-(\d+)/', views.sql_edit,name='sql_edit'),
    url(r'^sql_del/', views.sql_del,name='sql_del'),
    url(r'^sql_add/', views.sql_add,name='sql_add'),
    url(r'^sql_select_update/', views.sql_select_update,name='sql_select_update'),

    #资产收集
    url(r'^update_asset/', views.update_asset,name='update_asset'),

    url(r'^test/', views.test,name='test'),
]
