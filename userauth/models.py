from django.db import models
from django.contrib.auth.models import AbstractUser,Group


class UserInfo(AbstractUser):
    """用户信息"""
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name="姓名")
    qq = models.CharField(max_length=16, blank=True, null=True, verbose_name='QQ')
    wechat = models.CharField(max_length=32, blank=True, null=True, verbose_name='微信')
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='联系电话')

    class Meta:
        default_permissions = ()
        permissions = (
            ('view_user', '查看用户'),
            ('edit_user', '管理用户'),
        )
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

class UserGroup(Group):
    group_name = models.CharField(max_length=32, unique=True, verbose_name=u'用户组')
    comment = models.TextField(blank=True, null=True, verbose_name=u'备注')

    def clean(self):
        self.name = self.group_name
    def __str__(self):
        return self.name
    class Meta:
        default_permissions = ()
        permissions = (
            ('view_usergroup', '查看用户组'),
            ('edit_usergroup', '管理用户组'),
        )
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

class LoginRecord(models.Model):
    user = models.CharField(max_length=32, verbose_name='用户')
    date = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    type = models.CharField(max_length=32, verbose_name='类型')
    action = models.CharField(max_length=32, verbose_name='动作')
    ip = models.CharField(max_length=15, verbose_name='用户IP')
    content = models.TextField(verbose_name='内容')

    def __str__(self):
        return self.user

    class Meta:
        default_permissions = ()
        permissions = (
            ("view_loginrecord", "查看登录记录"),
            ("edit_loginrecord", "管理登录记录"),
        )
        ordering = ['-date']
        verbose_name = "登录信息"
        verbose_name_plural = "登录信息管理"