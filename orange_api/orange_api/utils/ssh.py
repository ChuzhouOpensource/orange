from paramiko.client import  SSHClient, AutoAddPolicy
from  paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException, SSHException,NoValidConnectionsError
from io import StringIO

class SshParamiko(object):
    def __init__(self,hostname,port=22,username='root', pkey=None, password=None,  connect_timeout=10):

        if pkey is  None and password is None:
            raise SSHException('私钥或密码必须上传一个')

        self.client = None

        self.params = {
            "hostname": hostname,
            "port": port,
            "username": username,
            "password": password,
            "pkey": RSAKey.from_private_key(StringIO(pkey)) if isinstance(pkey, str) else pkey,
            "timeout": connect_timeout,
        }

    #验证登录数据
    def get_connectd_client(self):
        if self.client is not None:
            raise RuntimeError('ssh连接已建立')

        if not self.client:
            try:
                #创建客户端连接对象
                self.client = SSHClient()

                #第一次指纹处理
                self.client.set_missing_host_key_policy(AutoAddPolicy)

                #建立连接
                self.client.connect(**self.params)

            except (TimeoutError, NoValidConnectionsError, AuthenticationException) as e:
                return None
        return self.client

    @staticmethod
    def gen_key():
        #生成公私钥键值对
        iodata = StringIO()
        key = RSAKey.generate(2048) #生成长度2048的密钥对
        key.write_private_key(iodata)

        return iodata.getvalue(), 'ssh-rsa' + key.get_base64()

    #上传公钥到对应主机
    def upload_key(self, public_key):

        cmd = f'mkdir -p -m 700 ~.ssh && \
              echo {public_key!r} >> ~/.ssh/authorized_keys && \
              chmod 600 ~/.ssh/authorized_keys'

        code, out = self.execute_cmd(cmd)
        if code != 0:
            raise Exception(f'添加公钥失败：{out}')

    def execute_cmd(self, cmd, timeout=1800, environment=None):
        #设置执行指令过程，一旦异常就raise
        cmd = 'set -e\n' + cmd
        channel = self.client.get_transport().open_session()
        channel.settimeout(timeout)
        channel.set_combine_stderr(True)  # 正确和错误输出都在一个管道对象里面输出出来
        channel.exec_command(cmd)
        try:
            out_data = channel.makefile("rb", -1).read().decode()
        except UnicodeDecodeError:
            out_data = channel.makefile("rb", -1).read().decode("GBK")

        return channel.recv_exit_status(), out_data

