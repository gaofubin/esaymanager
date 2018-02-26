#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 0006 15:12
# @Author  : All is well
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from .models import Cloud,Server,Project,DataBase


class CloudForm(forms.ModelForm):
    class Meta:
        model= Cloud
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required','placeholder': '必填'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': 'required','placeholder': '必填'}),
            'people': forms.TextInput(attrs={'class': 'form-control', 'required': 'required','placeholder': '必填'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'required','placeholder': '必填'}),
            'QQ_group': forms.TextInput(attrs={'class': 'form-control', 'required': 'required','placeholder': '必填'}),
            'comment': forms.Textarea(attrs={'class': 'form-control','required': 'required','placeholder': '选填'}),
        }

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = [
            'saltid','hostname','lan_ip','wan_ip',
            'osversion','memory','disk','cpu_model',
            'cpu_core','kernel','area','status','project_name','cloud_name',]

        widgets = {
            'saltid': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'lan_ip': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'wan_ip': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'osversion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '选填'}),
            'memory': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'disk': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'cpu_model': forms.TextInput(attrs={'class': 'form-control','placeholder': '选填'}),
            'cpu_core': forms.TextInput(attrs={'class': 'form-control',  'placeholder': '选填'}),
            'kernel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '选填'}),
            'area': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'cloud_name': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'project_name':forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
        }

class ProForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'area': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'people': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
        }

class SqlForm(forms.ModelForm):
    class Meta:
        model = DataBase
        fields = [
            'sql_name','ip','memory','disk',
            'type','area','status','project_name','cloud_name',]

        widgets = {
            'sql_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'ip': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'memory': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'disk': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': '选填'}),
            'area': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'cloud_name': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
            'project_name':forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': '必填'}),
        }
