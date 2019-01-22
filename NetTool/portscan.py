#!/usr/bin/env python
#coding=utf-8
import os 
import sys 
import nmap 
import re
class ScanPort():
    def __init__(self):
        self.s     = nmap.PortScanner()

    def scanms17(self):
    	self.s.scan(self.hosts, self.ports, arguments='-sS --script=smb-vuln-ms17-010.nse')
        for host in self.s.all_hosts():
            if self.s[host]['status']['state'] == 'up':
                if  'hostscript' not in self.s[host]:
                    pass
                    print "The hosts  %s is ok" %self.s[host]['addresses']['ipv4']
                else:
                    self.data = self.s[host]['hostscript'][0]['output']
                    print "Device IPAddress:" + ' '+  self.s[host]['addresses']['ipv4']
                    print ('-'*80)
                    print self.data

    def scanmysql(self):
        self.s.scan(self.hosts, self.ports, arguments='--script=mysql-empty-password.nse')
        for host in self.s.all_hosts():
            if self.s[host].state() == 'up':
                for proto in self.s[host].all_protocols():
                    lport = sorted(self.s[host][proto].keys())
                    for port in lport:
                        if 'script' not in self.s[host][proto][port]:
                            pass
                        else:
                            self.data = self.s[host][proto][port]['script']
                            for v,k in self.data.items():
                                print "Device IPAddress:"  + ' ' +  self.s[host]['addresses']['ipv4']
                                print ('-'*80)
                                print ('{v} -->{k}'.format(v=v,k=k)) 

    def scanport(self):
        list = [] 
        try:        
            self.s.scan(self.hosts,self.ports,arguments='-sS')
            for host in self.s.all_hosts() :
                if self.s[host].state() == 'up':
                    list.append("Device IPAddress:" + ' ' +  self.s[host]['addresses']['ipv4'])
                    for proto in self.s[host].all_protocols():
                        lport = sorted(self.s[host][proto].keys())
                        for port in lport:
                            list.append ('ports : %s \tserver: %s \tstatus: %s' %(port, self.s[host][proto][port]['name'],self.s[host][proto][port]['state']))
                list.append('-'*80)
        except Exception as e:
            exit(0)
        self.data = '\n'.join(list)
        print self.data

    def info(self):
        os.system("clear")
        print "#              Welcome Network Check Tool                      　　　#"
        print "---------------------------------------------------------------------"
        print "#   程序说明:                                                  　　　 #"
        print "#     1. 支持mysql空密码检查，端口3306                         　　　  #"
        print "#     2. 支持勒索病毒漏洞检查，端口445                         　　　   #"
        print "#     3. 支持主机端口状态检查,支持连续端口或是指定端口格式               #"
        print "#     4. 以下格式的例子，支持一个网段或是单个IP　　　　　　　　　　　     #"
        print "#  　　　- 192.168.32.0/24 3306        or  192.168.32.2 3306         #"
        print "#        - 192.168.32.0/24 445         or  192.168.32.2 445          #"
        print "#  　　　- 192.168.32.0/24 1-1024      or  192.168.32.2 1-1024       #"
        print "#  　　　- 192.168.32.0/24 22,80,3306  or  192.168.32.2 22,80,3306   #"
        print "#                                                                    #"
        print "#                                       ---- Author: Arcky.li v1     #"
        print "######################################################################"
        scan_row = []
        input_data = raw_input('Pls input hosts and port: ')
        scan_row = input_data.split(" ")
        if len(scan_row) !=2:
            sys.exit(0)
        self.hosts = scan_row[0]
        self.ports = scan_row[1]
        try:
            if self.ports == "445":
                self.scanms17()
            elif self.ports == "3306":
                self.scanmysql()
            else:
                self.scanport()
        except Exception as e:
            print "[!] Exception caught: {}".format(e)

if __name__ == "__main__":
    scan=ScanPort()
    scan.info()
