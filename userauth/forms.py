#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/3 10:14
# @Author  : Aries
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django import forms

from .models import UserInfo,UserGroup

class LoginForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control','placeholder':"Username"}),
        error_messages={'required': '账号不能为空'}
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control','placeholder':"Password"}),
        error_messages={'required': '密码不能为空'}
    )

class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('username', 'first_name', 'name', 'phone', 'qq', 'is_active')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名', 'required': 'required',
                                               'data-validate-length-range': '5,30'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'data-validate-length-range': '4,16'}),
            'qq': forms.TextInput(attrs={'class': 'form-control', 'data-validate-length': '11'}),
            'is_active': forms.CheckboxInput(attrs={'style': 'padding-top:5px;'})
        }


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = UserGroup
        fields = ('group_name','comment')
        widgets = {
            'group_name': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', 'data-validate-length-range': '2,20'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'})
        }


class ChangePassword(forms.Form):
    old_password = forms.CharField(label="原密码", max_length=128,
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                       'required': 'required',
                                   }))
    new_password = forms.CharField(label="新密码", max_length=128, min_length=6,
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                       'required': 'required',
                                   }))
    confirm_password = forms.CharField(label="重复密码", max_length=128, min_length=6,
                                       widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                       'required': 'required',
                                   }))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(ChangePassword, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('原密码不正确！')
        return old_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']
        if new_password != confirm_password:
            raise forms.ValidationError('两次输入新密码不一致！')
        return confirm_password

    def save(self):
        password = self.cleaned_data['new_password']
        self.instance.set_password(password)
        self.instance.save()
        return self.instance