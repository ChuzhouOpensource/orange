from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号码')
    avatar = models.ImageField(upload_to='avatar', verbose_name='用户头像', null=True, blank=True)
    class Meta:
        db_table = 'orange_users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
