from django.shortcuts import render,HttpResponse,redirect
from .models import Cloud,Project,DataBase,Server,Area
import json
from django.db.models import Q
from .forms import CloudForm,ServerForm,ProForm,SqlForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .collection_of_assets import get_asset_dict


# 云商
def cloud_list(request):
    nid = request.GET.get('id')
    cloud_obj = Cloud.objects.all()
    return render(request,'cmdb/cloud_list.html',{'cloud_obj':cloud_obj})

def cloud_add(request):

    if request.method == 'POST':
        form = CloudForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/cmdb/cloud_list/')
    else:
        form = CloudForm()
    return render(request,'cmdb/cloud_add.html',{'form':form})

def cloud_edit(request,nid):
    cld_obj = Cloud.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = CloudForm(request.POST,instance=cld_obj)
        if form.is_valid():
            form.save()
            return redirect("/cmdb/cloud_list/")
    form = CloudForm(instance=cld_obj)
    return render(request,'cmdb/cloud_edit.html',{'form':form})

def cloud_del(request):
    ret = {'status':True}
    try:
        nid = request.POST.getlist('nid[]')
        print(nid)
        obj = Cloud.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


# 主机
def host_list(request,**kwargs):

    verbose_dict = {}
    for ver in Server._meta.fields:
        verbose_dict[ver.name] = ver.verbose_name

    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            condition[k] = v
    # print(condition)
    # current_page = request.GET.get('page')
    # current_page = int(current_page)
    # per_page = 2
    #
    # start = (current_page-1) * per_page
    # end = current_page * per_page
    # 分页
    #django-pure-pagination

    keywords = request.GET.get("keywords","")

    if keywords:
        host_obj = Server.objects.filter(**condition).filter(
            Q(saltid__contains=keywords)\
            |Q(hostname__contains=keywords)\
            | Q(lan_ip__contains=keywords)\
            | Q(wan_ip__contains=keywords)\
            | Q(memory__contains=keywords)\
            | Q(disk__contains=keywords)\
            | Q(area__region__contains=keywords)
            )
    else:
        host_obj = Server.objects.filter(**condition)
    area_filter = Area.objects.all()
    cloud_filter = Cloud.objects.all()
    pro_filter = Project.objects.all()
    status_filter = Server.status_choice
    #分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(host_obj, 14, request=request)

    orgs = p.page(page)

    return render(request,'cmdb/host_list.html',
                  {'host_obj':orgs,
                   'cloud_filter':cloud_filter,
                   'pro_filter':pro_filter,
                   'status_filter':status_filter,
                   'area_filter':area_filter,
                   'kwargs':kwargs,
                   'verbose_dict':verbose_dict,
                   }
                  )

def host_edit(request,nid):
    host_obj = Server.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = ServerForm(request.POST,instance=host_obj)
        if form.is_valid():
            form.save()
            return redirect("/cmdb/host_list-0-0-0/")
    form = ServerForm(instance=host_obj)
    return render(request,'cmdb/host_edit.html',{'form':form})

def host_del(request):
    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        Server.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

def host_add(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/cmdb/host_list-0-0-0/")
    else:
        form = ServerForm()
    return render(request,'cmdb/host_add.html',{'form':form})

def host_select_update(request):

    ret = {'status': True}
    try:
        edit_num = request.POST.getlist('edit_num[]',"")
        cloud_id = request.POST.get("cloud_id","")
        pro_id = request.POST.get("pro_id","")
        status_id = request.POST.get("status_id","")
        area_id = request.POST.get("area_id","")
        host_obj = Server.objects.filter(id__in=edit_num)
        if cloud_id:
            host_obj.update(cloud_name_id=cloud_id)
        if pro_id:
            host_obj.update(project_name_id=pro_id)
        if area_id:
            host_obj.update(area_id=area_id)
        if status_id:
            host_obj.update(status=status_id)

    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

# 项目
def pro_list(request):
    pro_obj = Project.objects.all()
    return render(request,'cmdb/pro_list.html',{'pro_obj':pro_obj})

def pro_add(request):
    if request.method == 'POST':
        form = ProForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/cmdb/pro_list/')
    else:
        form = ProForm()
    return render(request,'cmdb/pro_add.html',{'form':form})

def pro_edit(request,nid):

    pro_obj = Project.objects.filter(id=nid).first()
    if request.method == "POST":
        form = ProForm(request.POST,instance=pro_obj)
        if form.is_valid():
            form.save()
            return redirect("/cmdb/pro_list/")
    form = ProForm(instance=pro_obj)
    return render(request,'cmdb/pro_edit.html',{'form':form})

def pro_del(request):
    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        Project.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

#数据库

def sql_list(request,**kwargs):
    verbose_dict = {}
    for ver in DataBase._meta.fields:
        verbose_dict[ver.name] = ver.verbose_name

    # for i in range(1,20):
    #     DataBase.objects.create(
    #         sql_name='test' + str(i),
    #         ip='66.66.66.' + str(i),
    #         memory='32',
    #         disk='122',
    #         type=1
    #     )
    # print(kwargs)
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            condition[k] = v

    keywords = request.GET.get("keywords","")
    print(keywords)

    if keywords:
        sql_obj = DataBase.objects.filter(**condition).filter(
            Q(sql_name=keywords)\
            |Q(ip=keywords)\
            | Q(memory=keywords)\
            | Q(disk=keywords)\
            | Q(area__region=keywords)
            )
        print(sql_obj)
    else:
        sql_obj = DataBase.objects.filter(**condition)
    area_filter = Area.objects.all()
    cloud_filter = Cloud.objects.all()
    pro_filter = Project.objects.all()
    status_filter = DataBase.status_choice
    #分页

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(sql_obj, 13, request=request)

    orgs = p.page(page)


    return render(request,'cmdb/sql_list.html',
                  {'sql_obj':orgs,
                   'cloud_filter':cloud_filter,
                   'pro_filter':pro_filter,
                   'status_filter':status_filter,
                   'area_filter':area_filter,
                   'kwargs':kwargs,
                   'verbose_dict':verbose_dict,
                   }
                  )

def sql_edit(request,nid):

    host_obj = DataBase.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = SqlForm(request.POST,instance=host_obj)
        if form.is_valid():
            form.save()
            return redirect("/cmdb/sql_list-0-0-0/")
    form = SqlForm(instance=host_obj)
    return render(request,'cmdb/sql_edit.html',{'form':form})

def sql_del(request):

    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        DataBase.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

def sql_add(request):

    if request.method == 'POST':
        form = SqlForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/cmdb/sql_list-0-0-0/")
    else:
        form = SqlForm()
    return render(request,'cmdb/sql_add.html',{'form':form})

def sql_select_update(request):

    ret = {'status': True}
    try:
        edit_num = request.POST.getlist('edit_num[]',"")
        cloud_id = request.POST.get("cloud_id","")
        pro_id = request.POST.get("pro_id","")
        status_id = request.POST.get("status_id","")
        area_id = request.POST.get("area_id","")
        sql_obj = DataBase.objects.filter(id__in=edit_num)
        if cloud_id:
            sql_obj.update(cloud_name_id=cloud_id)
        if pro_id:
            sql_obj.update(project_name_id=pro_id)
        if area_id:
            sql_obj.update(area_id=area_id)
        if status_id:
            sql_obj.update(status=status_id)

    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


def update_asset(request):

    ret = {'status': True}
    try:
        asset_obj = get_asset_dict()
        for k, v in asset_obj.items():
            Server.objects.update_or_create(
                saltid=k,
                hostname=v[0],
                osversion=v[1],
                os=v[2],
                memory="%s GB" %(int(v[3]+1)),
                cpu_model=v[4],
                cpu_core=v[5],
                disk="%s GB" %v[6],
                kernel=v[7],
                lan_ip=v[8],
                wan_ip=v[9]
            )
    except Exception as e:
            ret['status'] = False
    return HttpResponse(json.dumps(ret))

    # return redirect("/cmdb/host_list-0-0-0/")















def test(request):
        asset_obj = get_asset_dict()
        for k,v in asset_obj.items():

                Server.objects.update_or_create(
                            saltid=k,
                            hostname=v[0],
                            osversion=v[1],
                            os=v[2],
                            memory=v[3],
                            cpu_model=v[4],
                            cpu_core=v[5],
                            disk=v[6],
                            kernel=v[7],
                            lan_ip=v[8],
                            wan_ip=v[9]
                )

        return redirect("/cmdb/host_list-0-0-0/")
