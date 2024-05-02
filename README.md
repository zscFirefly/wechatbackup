# wechatbackup
## 项目说明
项目通过pysqlcipher3，将电脑的微信聊天记录导出为csv文件保存。

适用环境：mac

python版本：python3.11


## 部署方式
- 修改config/config.py配置
	- **FilePath:**微信文件路径
	- **SECRETKEY:**微信db的64位编码
	- **FileList:**db文件列表

## 启动方式
程序主入口。
```python
python core/main.py
```
