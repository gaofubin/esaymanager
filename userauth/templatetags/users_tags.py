#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/3 21:08
# @Author  : Aries
# @Site    : 
# @File    : users_tags.py
# @Software: PyCharm
from django.contrib.auth.models import Group, Permission
from django import template
from userauth.models import UserInfo,UserGroup
from django.db.models import Q

register = template.Library()

def show_permissions(aid, perm_type):
    """
        获取用户所有权限
    :param aid:
    :param perm_type:
    :return:
    """
    # print('show_permissions, aid', aid)
    select_permissions_dict = {}
    permissions = Permission.objects.filter(
        Q(content_type__app_label__exact='userauth') |
        Q(content_type__app_label__exact='cmdb')
    ).values('pk', 'name')
    permissions_dict = {i['pk']: i['name'] for i in permissions}

    if aid and perm_type == 'user':
        user = UserInfo.objects.get(pk=aid)
        select_permissions_dict = {i['pk']: i['name'] for i in user.user_permissions.values('pk', 'name')}
        select_permissions_group_dict = {
            str(i['pk']): '%s(继承组)'%i['name'] for g in user.groups.all() for i in g.permissions.values('pk', 'name')
            }
        print(select_permissions_group_dict)
        select_permissions_dict = dict(select_permissions_dict, **select_permissions_group_dict)
    elif aid and perm_type == 'user_group':
        group = Group.objects.get(pk=aid)
        select_permissions_dict = {i['pk']: i['name'] for i in group.permissions.values('pk','name')}

    for i in select_permissions_dict:
        if i in permissions_dict:
            del permissions_dict[i]
    # print(permissions_dict, select_permissions_dict)
    return {'permissions_dict': permissions_dict, 'select_permissions_dict': select_permissions_dict}

register.inclusion_tag('tags/tag_perssions.html')(show_permissions)

def show_users(aid, value):
    """
        获取用户
    :param aid:
    :param value:
    :return:
    """
    select_users_dict = {}
    users_dict = {i['pk']: i['name'] for i in UserInfo.objects.values('pk', 'name')}

    if aid and value == 'user_group':
        select_users_dict = {i['pk']: i['name'] for i in UserGroup.objects.get(pk=aid).user_set.values('pk', 'name') }
        # print(select_users_dict)
        for i in select_users_dict:
            if i in users_dict:
                del users_dict[i]
    return {'users_dict': users_dict, 'select_users_dict': select_users_dict}

register.inclusion_tag('tags/tag_users.html')(show_users)

def show_user_groups(aid):
    """
        获取用户组
    :param aid:
    :return:
    """
    select_user_groups_dict = {}
    user_groups_dict = {i['pk']: i['name'] for i in Group.objects.values('pk', 'name')}
    if aid:
        select_user_groups_dict = {i['pk']: i['name'] for i in UserInfo.objects.get(pk=aid).groups.values('pk','name')}
    for i in select_user_groups_dict:
        if i in user_groups_dict:
            del user_groups_dict[i]
    # print(user_groups_dict, select_user_groups_dict)
    return {'user_groups_dict': user_groups_dict, 'select_user_groups_dict': select_user_groups_dict}

register.inclusion_tag('tags/tag_user_groups.html')(show_user_groups)


