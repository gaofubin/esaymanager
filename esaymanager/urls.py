"""esaymanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from userauth import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index,name='index'),
    url(r'^$', views.user_login,name='user_login'),
    url(r'^logout/', views.user_logout,name='user_logout'),
    url(r'^change_password/', views.change_password,name='change_password'),
    url(r'^user_list/', views.user_list,name='user_list'),
    url(r'^user_audit/', views.user_audit,name='user_audit'),
    url(r'^user_add/', views.user_add,name='user_add'),
    url(r'^user_edit-(\d+)/', views.user_edit,name='user_edit'),
    url(r'^user_del/', views.user_del,name='user_del'),
    url(r'^user_group_list/', views.user_group_list, name='user_group_list'),
    url(r'^user_group_add/', views.user_group_add, name='user_group_add'),
    url(r'^user_group_del/', views.user_group_del, name='user_group_del'),
    url(r'^user_group_edit-(\d+)/', views.user_group_edit, name='user_group_edit'),
    url(r'^cmdb/',include('cmdb.urls')),
    url(r'^deploy/',include('deploy.urls')),
]
