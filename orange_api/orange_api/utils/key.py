from functools import lru_cache
from host.models import PkeyModel



class PkeyManger(object):
    '''管理公私钥类'''

    keys = ('public_key', 'private_key')

    @classmethod
    @lru_cache(maxsize=64)
    def get(cls, name):
        '''获取公私钥，从库中获取'''
        info = PkeyModel.objects.filter(name=name).first()
        if not info:
            raise KeyError(f'没有这个{name!r}密钥对')

        #已元祖形式，返回公私钥
        return (info.private, info.public)

    @classmethod
    def set(cls, name, private_key, public_key, description=None):
        '''保存公私钥,入库'''
        PkeyModel.objects.update_or_create(name=name, defaults={
            'private': private_key,
            'public': public_key,
            'description': description
        })