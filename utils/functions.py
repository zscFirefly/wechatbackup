
import hashlib
from datetime import datetime


def md5_encrypt(input_string):
    """
    对输入的字符串进行MD5加密并返回其十六进制表示。

    参数:
    input_string (str): 需要加密的字符串。

    返回:
    str: 加密后的MD5值，以32位小写十六进制字符串形式表示。
    """
    # 确保字符串被正确编码为字节，因为hashlib的update方法需要字节类型
    if input_string != None:
        byte_string = input_string.encode('utf-8')

        # 创建一个md5对象
        md5_hash = hashlib.md5()

        # 更新md5对象的状态，使其包含输入数据
        md5_hash.update(byte_string)

        # 获取加密后的16进制字符串表示
        encrypted_string = md5_hash.hexdigest()

        return encrypted_string

    else:
        return ''

# # 示例
# input_str = "weixin864941368"
# encrypted_md5 = md5_encrypt(input_str)
# print(f"Original String: {input_str}")
# print(f"MD5 Encrypted: {encrypted_md5}")

def format_timestamp(timestamp):
    """将时间戳转换为易读的日期时间格式"""
    timestamp += 3600 * 8
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def exprase_msgformat(msgtype):
    if msgtype == 10000:
        return '系统消息'
    if msgtype == 1:
        return '普通文本'
    if msgtype == 3:
        return '图片'
    if msgtype == 34:
        return '语音'
    if msgtype == 43:
        return '视频'
    if msgtype == 47:
        return '表情包'
    if msgtype == 48:
        return '位置'
    if msgtype == 49:
        return '分享消息'
    return str(msgtype)
