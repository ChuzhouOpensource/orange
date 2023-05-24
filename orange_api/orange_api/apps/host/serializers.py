from rest_framework import serializers
from .models import Host,HostCategory
from orange_api.utils.ssh import SshParamiko
from orange_api.utils.key import PkeyManger
from django.conf import settings


class HostCategoryModelSerializer(serializers.ModelSerializer):
    '''主机类别序列化器'''
    class Meta:
        model = HostCategory
        fields = ('id', 'name')

class HostModelSerializer(serializers.ModelSerializer):
    '''主机序列化器'''
    category_name = serializers.CharField(source='category.name', read_only=True)
    password = serializers.CharField(max_length=32, write_only=True, label='登录密码')

    class Meta:
        model = Host
        fields = ('id', 'category', 'category_name', 'name', 'ip_addr', 'port', 'description', 'username', 'password')

    def get_public_key(self):
        '''

        :return: public_key 公钥
        '''
        try:
            # 获取公私钥
            private_key, public_key = PkeyManger.get(settings.DEFAULT_KEY_NAME)
        except KeyError as e:
            #异常无公私钥的话，生成公私钥
            private_key, public_key = SshParamiko.gen_key()
            print(private_key, public_key)
            PkeyManger.set(settings.DEFAULT_KEY_NAME,private_key, public_key, description='ssh全局密钥对')

        return public_key

    def validate(self, attrs):
        '''当用户添加或编辑主机信息时自动执行该方法'''
        ip_addr = attrs.get('ip_addr')
        port = attrs.get('port')
        username = attrs.get('username')
        password = attrs.get('password')

        #to do 验证主机信息
        cli = SshParamiko(hostname=ip_addr,port=port,username=username,password=password)
        if cli.get_connectd_client():
            #获取公钥
            public_key = self.get_public_key()
            #上传公钥到对应主机
            try:
                cli.upload_key(public_key)
            except Exception as e:
                raise serializers.ValidationError('主机验证失败,请检查主机信息')
            return attrs




    def create(self, validated_data):
        #添加主机信息，第一次添加需要生成全局公钥和私钥
        ip_addr = validated_data.get('ip_addr')
        port = validated_data.get('port')
        username = validated_data.get('username')
        password = validated_data.get('password')


        password = validated_data.pop('password') #将密码字段剔除，不入库
        instance = Host.objects.create(**validated_data)
        return instance
    #
    # def update(self, instance, validated_data):
    #     #更新主机信息
    #     pass
    #
    #     return instance
