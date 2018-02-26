from django.contrib import admin

from .models import Cloud,Server,DataBase,Project,Area


admin.site.register(Cloud)
admin.site.register(Server)
admin.site.register(DataBase)
admin.site.register(Project)
admin.site.register(Area)