from django.db import models

# Create your models here.

class Business(models.Model):
    # 默认生成自增id列
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32, null=True,default="SA")


# 主机信息
class Host(models.Model):
    nid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=32, db_index=True)
    ip = models.GenericIPAddressField(protocol="ipv4", db_index=True) # protocol默认是both
    port = models.IntegerField()
    b = models.ForeignKey("Business", to_field='id', on_delete=models.CASCADE)


# 应用信息
class Application(models.Model):
    name = models.CharField(max_length=32)
    r = models.ManyToManyField("Host")

# 主机与应用关系
# class HostToApp(models.Model):
#     hobj = models.ForeignKey(to='Host', to_field='nid')
#     aobj = models.ForeignKey(to='Application', to_field='id')
