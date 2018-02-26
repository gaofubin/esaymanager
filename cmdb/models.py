from django.db import models


class Project(models.Model):

    '''项目信息'''

    name = models.CharField(max_length=32, unique=True, verbose_name='项目名称')
    area_choises = (
        (1,'大陆'),
        (2,'日韩'),
        (3,'欧美'),
    )
    area = models.SmallIntegerField(choices=area_choises, verbose_name='区域')
    people = models.CharField(max_length=32, verbose_name='负责人')
    comment = models.TextField(verbose_name='备注')
    def __str__(self):
        return self.name
    class Meta:
            default_permissions = ()
            permissions = (
                ('view_project', '查看项目'),
                ('edit_project', '管理项目'),
            )
            verbose_name = '项目管理'
            verbose_name_plural = verbose_name

class Cloud(models.Model):
    '''云平台信息'''
    name = models.CharField(max_length=32, unique=True, verbose_name='平台名称')
    address = models.CharField(max_length=200, verbose_name='平台地址')
    people = models.CharField(max_length=32, verbose_name='商务联系人')
    phone = models.CharField(max_length=32,verbose_name='联系电话')
    QQ_group = models.CharField(max_length=32,verbose_name='响应QQ群')
    comment = models.TextField(verbose_name='备注')
    def __str__(self):
        return self.name
    class Meta:
        default_permissions = ()
        permissions = (
            ('view_cloud', '查看云平台'),
            ('edit_cloud', '管理云平台'),
        )
        verbose_name = '云平台管理'
        verbose_name_plural = verbose_name

class Server(models.Model):
    '''服务器信息'''
    status_choice = (
        (1, '上线'),
        (2, '下线'),
    )
    saltid = models.CharField(max_length=32,unique=True, verbose_name='SaltId')
    hostname = models.CharField(max_length=50, blank=True, verbose_name=u'主机名')
    lan_ip = models.GenericIPAddressField(null=True,blank=True,verbose_name='内网IP')
    wan_ip = models.GenericIPAddressField(unique=True,null=True,blank=True ,verbose_name='外网ip')
    osversion = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'系统版本')
    os = models.CharField(max_length=50,blank=True,null=True,verbose_name='操作系统')
    memory = models.CharField(max_length=50, blank=True, null=True, verbose_name='内存')
    disk = models.CharField(max_length=32, blank=True, null=True, verbose_name='硬盘')
    cpu_model = models.CharField(max_length=50, blank=True, null=True, verbose_name='CPU型号')
    cpu_core = models.SmallIntegerField(blank=True, null=True, verbose_name='CPU核数')
    kernel = models.CharField(max_length=50, blank=True, null=True, verbose_name='内核')
    area = models.ForeignKey("Area", blank=True, null=True, verbose_name='所在区域')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.SmallIntegerField(choices=status_choice, verbose_name='设备状态', default=0)
    project_name = models.ForeignKey('Project', max_length=50, blank=True, null=True, verbose_name='所属项目')
    cloud_name = models.ForeignKey('Cloud', max_length=50, blank=True, null=True, verbose_name='所属云平台')

    def __str__(self):
        return self.saltid
    class Meta:
        default_permissions = ()
        permissions = (
            ('view_server', '查看主机'),
            ('edit_server', '管理主机'),
        )
        verbose_name = '主机管理'
        verbose_name_plural = verbose_name

class DataBase(models.Model):
    '''数据库信息'''
    type_choice = (
        (1, 'MySQL'),
        (2, 'MongoDB'),
        (3, 'Memcached'),
    )
    status_choice = (
        (1, '上线'),
        (2, '下线'),
    )
    sql_name = models.CharField(max_length=32, unique=True, verbose_name='数据库名称')
    ip = models.GenericIPAddressField(verbose_name='IP')
    memory = models.CharField(max_length=32, blank=True, null=True, verbose_name='内存')
    disk = models.CharField(max_length=32, blank=True, null=True, verbose_name='硬盘')
    type = models.SmallIntegerField(choices=type_choice, verbose_name='类型')
    area = models.ForeignKey("Area", blank=True, null=True, verbose_name='所在区域')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.SmallIntegerField(choices=status_choice, verbose_name='设备状态', default=0)
    project_name = models.ForeignKey('Project', max_length=50, blank=True, null=True, verbose_name='所属项目')
    cloud_name = models.ForeignKey('Cloud', max_length=50, blank=True, null=True, verbose_name='所属云平台')

    def __str__(self):
        return self.sql_name
    class Meta:
        default_permissions = ()
        permissions = (
            ('view_database', '查看数据库'),
            ('edit_database', '管理数据库'),
        )
        verbose_name = '数据库管理'
        verbose_name_plural = verbose_name

class Area(models.Model):
    """资产所在区域"""
    region = models.CharField(max_length=32, unique=True, verbose_name="区域")
    def __str__(self):
        return self.region
    class Meta:
        default_permissions = ()
        permissions = (
            ('view_area', '查看区域'),
            ('edit_area', '管理区域'),
        )
        verbose_name = '地区'
        verbose_name_plural = verbose_name

class AssetRecord(models.Model):
    '''资产变更记录'''
    pass
    # user = models.CharField(max_length=244, verbose_name=u'用户')
    # audit_time = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    # type = models.CharField(max_length=10, verbose_name=u'类型')
    # action = models.CharField(max_length=20, verbose_name=u'动作')
    # action_ip = models.CharField(max_length=15, verbose_name=u'用户IP')
    # content = models.TextField(verbose_name=u'内容')
    #
    # class Meta:
    #     default_permissions = ()
    #     permissions = (
    #         ("view_message", u"查看操作记录"),
    #         ("edit_message", u"管理操作记录"),
    #     )
    #     ordering = ['-audit_time']
    #     verbose_name = u'审计信息'
    #     verbose_name_plural = u'审计信息管理'