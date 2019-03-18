from django.db import models


class BaseModel(models.Model):
    '''模型抽象基类'''
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True
