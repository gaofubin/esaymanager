from django.shortcuts import render, redirect ,get_object_or_404,HttpResponse
from django.contrib.auth import login, logout,authenticate
from .forms import LoginForm,ChangePassword,UserGroupForm
from .models import LoginRecord,UserInfo,UserGroup
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import UserForm
import json

def UserIP(request):
    '''获取用户IP'''
    ip = ''
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                login(request, user)
                LoginRecord.objects.create(type=u'用户登录', user=request.user, action=u'用户登录', ip=UserIP(request), content='用户登录 %s' % request.user)
                return redirect("/index")
        LoginRecord.objects.create(type=u'用户登录', user=request.POST.get('username'), action=u'用户登录',
                                   ip=UserIP(request), content=u'用户登录失败 %s' % request.POST.get('username'))
        return render(request, 'base/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'base/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect("/")

@login_required
def change_password(request):
    user = get_object_or_404(UserInfo, username=request.user)
    if request.method == 'POST':
        form = ChangePassword(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ChangePassword(instance=user)
    return render(request, "user/changepasswd.html", {"form": form})

@login_required
def index(request):
    return render(request, 'base/index.html')

@login_required
def user_list(request):
    user_obj = UserInfo.objects.all()
    # return render(request,'userauth/user_list.html',{'user_obj':user_obj})
    return render(request, 'user/user_list.html', {'user_obj': user_obj})

@login_required
def user_audit(request):
    '''
    审计日志
    '''
    if request.user.is_superuser:
        logs = LoginRecord.objects.all()[:300]
        if request.method == 'GET':
            if request.GET.get('aid'):
                aid = request.get_full_path().split('=')[1]
                log_detail = LoginRecord.objects.filter(id=aid)
                return render(request, 'user/useraudit_detail.html', {'log_detail': log_detail})

        return render(request, 'user/user_audit.html', {'all_logs': logs})
    else:
        raise Http404

@login_required
def user_add(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request,'user/user_add.html',{'form':form})
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            '''合法之后修改密码和组'''
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            group_select = request.POST.getlist('group_sel')
            group_delete = request.POST.getlist('group_del')
            perm_select = request.POST.getlist('perm_sel')
            perm_delete = request.POST.getlist('perm_del')
            if password1 and password1 == password2:
                form.save()
                user = get_object_or_404(UserInfo, username=username)
                print(user)
                user.set_password(password1)
                user.save()
                # 添加用户至UserGroup
                user.groups.add(*group_select)
                user.groups.remove(*group_delete)
                # 授予用户权限
                user.user_permissions.add(*perm_select)
                user.user_permissions.remove(*perm_delete)
                # UserInfo.objects.create(**obj.cleaned_data)
                return redirect("/user_list")
        else:
            return render(request,"user/user_add.html")

@login_required
def user_edit(request,aid):

    if request.method == 'GET':
        user_obj = UserInfo.objects.filter(id=aid).first()
        form = UserForm(instance=user_obj)
        return render(request,'user/user_edit.html',{'form': form,'aid':aid})

    elif request.method == "POST":
        user_obj = UserInfo.objects.filter(id=aid).first()
        form = UserForm(request.POST,instance=user_obj)
        if form.is_valid():
            group_select = request.POST.getlist('group_sel')
            group_delete = request.POST.getlist('group_del')
            perm_select = request.POST.getlist('perm_sel')
            perm_delete = request.POST.getlist('perm_del')
            form.save()
            #修改用户的组，用户的权限
            user_obj.groups.add(*group_select)
            user_obj.groups.remove(*group_delete)
            user_obj.user_permissions.add(*perm_select)
            user_obj.user_permissions.remove(*perm_delete)

        return redirect("/user_list")

def user_del(request):

    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        print(nid)
        obj = UserInfo.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

@login_required
def user_group_list(request):
    '''用户组信息'''
    groups = UserGroup.objects.all()
    return render(request,'user/user_group_list.html',{'groups':groups})

@login_required
def user_group_add(request):
    group = UserGroup()
    if request.method == 'POST':
        form = UserGroupForm(request.POST, instance=group)
        if form.is_valid():
            user_select = request.POST.getlist('user_sel')
            user_delete = request.POST.getlist('user_del')
            perm_select = request.POST.getlist('perm_sel')
            perm_delete = request.POST.getlist('perm_del')
            form.save()
            group.save()
            group.user_set.add(*user_select)
            group.user_set.remove(*user_delete)
            group.permissions.add(*perm_select)
            group.permissions.remove(*perm_delete)
            return redirect("/user_group_list")
    else:
        form = UserGroupForm(instance=group)
    return render(request, 'user/user_group_add.html', {'form': form})

@login_required
def user_group_del(request):

    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        print(nid)
        obj = UserGroup.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


@login_required
def user_group_edit(request,aid):
    if request.method == 'GET':
        user_group_obj = UserGroup.objects.filter(id=aid).first()
        form = UserGroupForm(instance=user_group_obj)

        return render(request,'user/user_group_edit.html',{'form': form,'aid':aid})

    elif request.method == "POST":
        group_obj = UserGroup.objects.filter(id=aid).first()
        form = UserGroupForm(request.POST,instance=group_obj)
        if form.is_valid():
            user_select = request.POST.getlist('user_sel')
            user_delete = request.POST.getlist('user_del')
            perm_select = request.POST.getlist('perm_sel')
            perm_delete = request.POST.getlist('perm_del')
            form.save()
            #修改用户的组，用户的权限
            group_obj.user_set.add(*user_select)
            group_obj.user_set.remove(*user_delete)
            group_obj.permissions.add(*perm_select)
            group_obj.permissions.remove(*perm_delete)

        return redirect("/user_group_list")