#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/3 21:56
# @Author  : Aries
# @Site    : 
# @File    : mytags.py
# @Software: PyCharm

from django import template
from django.contrib.auth.models import Group
from userauth.models import UserInfo
from django.db.models import Q
from django.shortcuts import get_object_or_404

register = template.Library()


@register.filter(name='all_users_num')
def all_users_num(user):
    userobj = UserInfo.objects.filter(username=user).first()
    if userobj:
        try:
            num = UserInfo.objects.all()
            return len(num)
        except Exception as e:
            return None
    else:
        return None


@register.filter(name='user_groups')
def all_user_groups(pk):
    """
        用户所属组
    :param pk:
    :return:
    """
    try:
        user_groups = [i.name for i in Group.objects.filter(user=pk)]
        return user_groups
    except Exception as e:
        return ''


@register.filter(name='is_super')
def user_is_super(pk):
    """
        用户是否是超级用户
    :param pk:
    :return:
    """
    if pk:
        return UserInfo.objects.get(pk=pk).is_superuser
    else:
        return None


@register.filter(name='list_item')
def show_item(value, arg):
    """
        获取列表中指定项
    :param value:
    :param arg:
    :return:
    """
    if value:
        return value[arg]
    else:
        return ''