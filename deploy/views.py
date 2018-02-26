from django.shortcuts import render,HttpResponse
from  esaymanager.settings import SALT_API
from deploy import saltapi
from deploy.models import SaltMinion
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe


def salt_key_update(request):

    ret = {'status': True}
    try:
        sapi = saltapi.SaltAPI(url=SALT_API['url'], username=SALT_API['username'], password=SALT_API['password'])
        minions, minions_pre = sapi.list_all_key()
        for accept_key in minions:
            SaltMinion.objects.get_or_create(name=accept_key,status=1)

        for deny_key in minions_pre:
            SaltMinion.objects.get_or_create(name=deny_key,status=2)
    except Exception as e:
        ret['status']=False
    return HttpResponse(json.dumps(ret))

def salt_key_list(request):
    key_list = SaltMinion.objects.all().order_by("-auth_date")
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(key_list, 13, request=request)

    key_list = p.page(page)

    return render(request,'deploy/salt_key_list.html',{'key_list':key_list})

def salt_key_accept(request):

    ret = {'status': True}
    try:
        salt_id = request.POST.get('id')
        salt_name = request.POST.get('username')
        sapi = saltapi.SaltAPI(url=SALT_API['url'], username=SALT_API['username'], password=SALT_API['password'])
        sapi.accept_key(salt_name)
        minion_obj = SaltMinion.objects.get(id=salt_id,name=salt_name)
        minion_obj.status = 1
        minion_obj.save()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

def salt_key_delete(request):
    ret = {'status': True}
    try:
        salt_id = request.POST.get('id')
        salt_name = request.POST.get('username')
        sapi = saltapi.SaltAPI(url=SALT_API['url'], username=SALT_API['username'], password=SALT_API['password'])
        sapi.delete_key(salt_name)
        minion_obj = SaltMinion.objects.get(id=salt_id,name=salt_name).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

def salt_command(request):

    if request.method == 'POST':
        a = request.POST.get('host')
        b = request.POST.get('command')
        c = request.POST.get('arg')
        sapi = saltapi.SaltAPI(url=SALT_API['url'], username=SALT_API['username'], password=SALT_API['password'])
        result = sapi.remote_execution(a,b,c)
        print(result)
        return render(request,'deploy/salt_command.html',{'result':result})

    return render(request,'deploy/salt_command.html')