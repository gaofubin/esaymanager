#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/17 1:06
# @Author  : Aries
# @Site    : 
# @File    : collection_of_assets.py
# @Software: PyCharm

from deploy import saltapi
from esaymanager.settings import SALT_API

def get_asset_dict():
    info = {}
    sapi = saltapi.SaltAPI(url=SALT_API['url'], username=SALT_API['username'], password=SALT_API['password'])
    grains_obj = sapi.remote_noarg_execution('*','grains.items')
    for ret in grains_obj:
        saltid = ret['id']
        hostname = ret['host']
        os = ret['os']
        osversion = ret['osrelease']
        mem_total = ret['mem_total']
        memory = int(mem_total) / 1024
        cpu_model = ret['cpu_model']
        cpu_core = ret['num_cpus']
        disk = ret['capacity']
        kernel = ret['kernel']
        iptmp = ret['ip4_interfaces']
        if ret['kernel'] == 'Linux':
            iptmp.pop('lo')
            lan_ip = iptmp.get('eth0')[0]
        else:
            iptmp2 = iptmp.get('Red Hat VirtIO Ethernet Adapter #2')
            lan_ip = iptmp2[0]
        wan_ip=ret['wan']
        info[saltid]=[hostname,osversion,os,memory,cpu_model,cpu_core,disk,kernel,lan_ip,wan_ip]
    return info





