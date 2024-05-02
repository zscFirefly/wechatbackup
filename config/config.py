

class BaseConfig:

    FilePath = '/Users/zhengshuocong/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/f286737dce49419f3f90b80688b922dc/'
    SECRETKEY = 'bfd1a62fed444615a725512945c4f00a72c0d20bcc544fc79214e4d79acc188c'
    FileList = ['msg_{n}.db'.format(n=i) for i in range(10)] # 这里range中的数值，取决于list中有有多少个msg文件。
