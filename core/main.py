import sys 
sys.path.append("..")
import pysqlcipher3.dbapi2 as sqlite
import pandas as pd 
import pysqlcipher3

from utils import functions
from config import config

FilePath = config.BaseConfig.FilePath
secretkey = config.BaseConfig.SECRETKEY
FileList = config.BaseConfig.FileList


# 获取db文件里面的数据表集合
def get_table(path,filename):
    db = sqlite.connect(path + filename)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA key='x''{secretkey}''';".format(secretkey=secretkey))
    db_cursor.execute("PRAGMA cipher_compatibility=3;")
    db_cursor.execute("PRAGMA cipher_page_size=1024;")
    db_cursor.execute("PRAGMA kdf_iter=64000;")
    db_cursor.execute("PRAGMA cipher_hmac_algorithm=HMAC_SHA1;")
    db_cursor.execute("PRAGMA cipher_kdf_algorithm=PBKDF2_HMAC_SHA1;")
    db_cursor.execute("SELECT name FROM sqlite_master;")
    data_list = db_cursor.fetchall()
    table_df = pd.DataFrame(data_list)
    return table_df    

# 通过db文件及table表名获取数据
def get_data(path,filename,table):
    db = sqlite.connect(path + filename)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA key='x''{secretkey}''';".format(secretkey=secretkey))
    db_cursor.execute("PRAGMA cipher_compatibility=3;")
    db_cursor.execute("PRAGMA cipher_page_size=1024;")
    db_cursor.execute("PRAGMA kdf_iter=64000;")
    db_cursor.execute("PRAGMA cipher_hmac_algorithm=HMAC_SHA1;")
    db_cursor.execute("PRAGMA cipher_kdf_algorithm=PBKDF2_HMAC_SHA1;")

    sql = "SELECT * FROM {table};".format(table=table)
    resdata_list = db_cursor.execute(sql).fetchall()

    return resdata_list

# 获取微信好友及其对应的db
def get_userdb():
    userdb = pd.DataFrame()
    chatinfo_path = FilePath + 'Message/'
    for file in FileList:
        table_df = get_table(chatinfo_path,file)
        table_df['db'] = file
        userdb = pd.concat([userdb,table_df])
    userdb.rename(columns={0:'content'},inplace=True)
    userdb.reset_index(inplace=True)
    userdb.to_csv("../data/userchat.csv",index=False)
    print("userchat save success!")
    return userdb

# 获取用户信息
def get_user_info():
    user_info_df = pd.DataFrame()
    path = FilePath + "Contact/"
    filename = 'wccontact_new2.db'
    table = 'WCContact'
    userinfo_list = get_data(path,filename,table)
    for i in userinfo_list:
        tmp = {}
        tmp['id'] = i[0]
        tmp['nickname'] = i[2]
        tmp['full_py'] = i[3]
        tmp['remark'] = i[5]
        tmp['sex'] = i[9]
        tmp['sex1'] = i[10]
        tmp['uitype'] = i[11]
        tmp['aliasName'] = i[23]
        tmp['md5'] = functions.md5_encrypt(i[0])
        user_info_df = pd.concat([user_info_df,pd.DataFrame(tmp,index=[0])])
    user_info_df.reset_index(inplace=True)
    user_info_df.to_csv("../data/userinfo.csv",index=False)
    print("userinfo save success!")
    return user_info_df

# 检索用户所在的数据库
def get_dbfile(userdb,userid):
    chatid = userdb.query("content.str.contains('%s')"%(userid))
    if len(chatid['db'])==0:
        return None
    else:
        return chatid['db'].drop_duplicates().values[0]

# 清洗聊天记录
def wash_userchat(userchatlist):
    userchat_df = pd.DataFrame()
    for i in userchatlist:
        tmp = {}
        tmp['time'] = functions.format_timestamp(i[2])
        tmp['msgtype'] = functions.exprase_msgformat(i[6])
        tmp['content'] = i[3]
        tmp['user'] = i[7]
        userchat_df = pd.concat([userchat_df,pd.DataFrame(tmp,index=[0])])
    return userchat_df

# 获取所有的聊天记录并保存
def get_all_user_chat_context():
    userdata = get_user_info()
    userdb = get_userdb()
    chat_path = FilePath + 'Message/'
    finish_data = pd.DataFrame()
    for i in range(len(userdata)):
        userid = userdata.at[i,'md5']
        username = userdata.at[i,'remark']
        nickname = userdata.at[i,'nickname']
        print(userid,username,nickname)
        dbfile = get_dbfile(userdb,userid)
        if dbfile == None:
            continue
        if userid == 'None' or userid == None or userid == '':
            continue

        table = "Chat_{userid}".format(userid=userid)
        userchat_list = get_data(chat_path,dbfile,table)
        userchat_df = wash_userchat(userchat_list)

        userchat_df['username'] = username
        userchat_df['nickname'] = nickname
        finish_data = pd.concat([finish_data,userchat_df])
    finish_data.to_csv("../data/chat.csv",index=False)


def main():
    get_all_user_chat_context()
    # user_info_df = get_user_info()
    # userdb = get_userdb()
    # print(userdb)



if __name__ == '__main__':
    main()

