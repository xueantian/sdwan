#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# email:xueatian@cisco.com


a=1
b=1
c=1
d=1
ipaddress=[]

while d < 4 :
    d+=1
    #print(a,'.',b,'.',c,'.',d)
    ip=str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)+'/32'+'\n'
    ipaddress.append(ip)
    c=0
    while c < 5:
        ip2=str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)+'/32'+'\n'
        ipaddress.append(ip2)
        #print(ip2)
        c+=1
        b=0
        while b < 10:
            ip3=str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)+'/32'+'\n'
            ipaddress.append(ip3)
            #print(ip2)
            b+=1

with open('prefix_test.txt','a') as file:
        for item in ipaddress:
            file.write(item)
with open('prefix_test.txt','r') as file:
    a=len(file.readlines())

file.close()
print(a)
