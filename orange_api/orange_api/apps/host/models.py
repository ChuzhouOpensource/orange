from django.db import models
from orange_api.utils.BaseModels import BaseModel
from users.models import User

class HostCategory(BaseModel):
    '''主机类别模型类'''

    class Meta:
        db_table = "host_category"
        verbose_name = "主机类别"
        verbose_name_plural = verbose_name

class Host(BaseModel):
    '''主机模型类'''
    category = models.ForeignKey('HostCategory', on_delete=models.DO_NOTHING, verbose_name='主机类别',
                                 related_name='hostcategory' )
    ip_addr = models.GenericIPAddressField(blank=True, null=True, verbose_name='连接地址')
    port = models.IntegerField(verbose_name='端口')
    username = models.CharField(max_length=50, verbose_name='登录用户')
    users = models.ManyToManyField(User)

    class Meta:
        db_table = 'host'
        verbose_name = '主机信息'
        verbose_name_plural = verbose_name
        def __str__(self):
            return f'{self.name}:{self.ip_addr}'


class PkeyModel(BaseModel):
    name = models.CharField(max_length=250, unique=True)
    private = models.TextField(verbose_name='私钥')
    public = models.TextField(verbose_name='公钥')

    def __repr__(self):
        return f'<Pkey {self.name}>'
