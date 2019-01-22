#!/usr/bin/env python
#coding=utf-8

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,NetMikoAuthenticationException
#import time
import sys
import getpass
import datetime
import os,shutil
import re

def backup():
    os.system("clear")
    print "                                                             "                
    print "   #                 网络设备自动备份工具　　　　　　　         #"
    print "   ----------------------------------------------------------"
    print "   #  IP格式说明：　                                          #"  
    print "   #    1. 支持单个IP: 10.0.0.1                               #"
    print "   #    2. 支持多个IP批量备份,IP间要以','隔开，如下所示         #"
    print "   #       10.0.0.1,10.0.0.2,10.0.0.3,10.0.0.4               #"
    print "   #  设备类型请按以下格式输入:                                #"
    print "   #   - cisco_ios                                           #"
    print "   #   - cisco_asa                                           #"
    print "   #   - huawei                                              #"
    print "   #   - juniper                                             #"
    print "   #                             ---- Author: Arcky.li v1.1  #"
    print "   ###########################################################"
    
    input_ip   = raw_input("IPAddress: ")
    ipaddress  = input_ip.split(",")
    if len(input_ip) == 0:
        sys.exit(0)
    username = raw_input("Username: ")
    if len(username) == 0:
        sys.exit(0)
    password = getpass.getpass()
    tftpip   = raw_input("Tftpip: ")
    if len(tftpip) == 0:
        sys.exit(0)
    dtype = raw_input("DeviceType: ")
    if len(dtype) == 0:
        sys.exit(0)
    print " "
    for ip in ipaddress:
        device={'device_type': dtype,
            'username': username,
            'password': password,
            'ip':ip
            }
        rootDir='/Autobackup'   
        date = datetime.datetime.now().strftime('%d-%H-%M')
        try:
            connect = ConnectHandler(**device)
            connect.enable()
        except (EOFError, NetMikoTimeoutException):
            print ('Can not connect to Device!')
            exit(0)
        except (EOFError, NetMikoAuthenticationException):
            print ('Username and Password wrong!')
            exit(0)

        print "网络设备 %s 备份开始..." %ip
        try:
            if  device['device_type'] == 'cisco_ios':
                hostname = connect.find_prompt()
                hostname = hostname.replace("#","")
                bkfilename   = ''.join((('-'.join((hostname,date))),'.cfg'))
                backupcmd    =  'copy running-config tftp:'
                bkconf  = '\n'.join((backupcmd,tftpip,bkfilename))
                connect.send_command(bkconf)

            elif  device['device_type'] == 'cisco_asa':
                hostname = connect.find_prompt()
                hostname = hostname.replace("#","")
                bkfilename   = ''.join((('-'.join((hostname,date))),'.cfg'))
                backupcmd    =  'copy running-config tftp:'
                backupcmd    = ''.join((backupcmd,'\n'))
                bkconf  = '\n'.join((backupcmd,tftpip,bkfilename,'\n'))
                connect.send_command(bkconf)
        
            elif device['device_type'] == 'huawei':
                hostname = connect.find_prompt()
                hostname = (re.findall(str(".*<(.*)>.*"),hostname))[0]
                bkfilename = ''.join((('-'.join((hostname,date))),'.cfg'))
                cmd = '\n'.join(((' '.join(("save",bkfilename))),'y'))
                connect.send_command(cmd)
                bkfilename = bkfilename.lower()
                cmd01 = ' '.join(("tftp",tftpip,"put", bkfilename))
                connect.send_command(cmd01)
                cmd02 = '\n'.join(((''.join(('del flash:/',bkfilename))),'y'))
                connect.send_command(cmd02)

            elif device['device_type'] == 'juniper':
                hostname = connect.find_prompt()
                hostname = hostname.replace(">","")
                hostname = (hostname.split("@"))[1]
                bkfilename = ''.join((('-'.join((hostname,date))),'.cfg'))
                bkfilename = ''.join(('/Autobackup/',bkfilename))
                cmd = connect.send_command("show configuration")
                with open(bkfilename,'w') as f:
                    f.write(cmd)
            else:
                exit(0)
        except Exception as e:
            print "[!] Exception caught: {}".format(e)

        if connect is not None:
            connect.disconnect()
            connect = None
            path = os.path.join(rootDir,hostname)
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                pass
            shutil.move((os.path.join(rootDir,bkfilename)),path)
            print "网络设备 %s 备份完成!!!" %ip
            print "-"*60

if __name__ == '__main__':
    backup()

