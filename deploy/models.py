from django.db import models

class SaltMinion(models.Model):
    name = models.CharField(max_length=100,verbose_name="Minion名称")
    create_date = models.DateField(auto_now_add=True,verbose_name="创建时间")
    status_choices = (
        (1,'已认证'),
        (2,'未认证'),
    )
    status = models.SmallIntegerField(choices=status_choices,verbose_name="认证状态")
    auth_date = models.DateField(auto_now=True,verbose_name="认证时间")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Salt认证'
        verbose_name_plural = verbose_name