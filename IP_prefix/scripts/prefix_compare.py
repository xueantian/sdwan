#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# email:xueatian@cisco.com
cn_lst=[]
external_lst=[]
result=[]
with open('cn_list.txt','r') as cn_list:
    cn_lists=cn_list.readlines()
    for line in cn_lists:
        line=line.rstrip('\n')
        cn_lst.append(line)
    cn_list.close()
print(len(cn_lst))

with open('external_bgp_list.txt', 'r') as external_list:
    external_lists=external_list.readlines()
    for line in external_lists:
        line=line.rstrip('\n')
        external_lst.append(line)
print(len(external_lst))

def compare_24():
    result=[]
    #compare the first number
    cn_lst_new=[]
    external_lst_new=[]
    for line in cn_lst:
        line=line.split('.')
        cn_lst_new.append(line)

    for line in external_lst:
        line=line.split('.')
        external_lst_new.append(line)

    i=0
    for items in external_lst_new:
        for cn_item in cn_lst_new:
            if items[0] == cn_item[0]:
                if items[1] == cn_item[1]:
                    if items[2] == cn_item[2]:

                        result.append(('bgp route-',items,'---国内路由--',cn_item))

    with open('campare_result.txt','w') as resultfile:
        resultfile.write('前24位相同的IP 地址:'+'\n')
        for items in result:
            resultfile.write(str(items)+'\n')
    resultfile.close()

def compare_16():
    result=[]

    cn_lst_new=[]
    external_lst_new=[]
    for line in cn_lst:
        line=line.split('.')
        cn_lst_new.append(line)

    for line in external_lst:
        line=line.split('.')
        external_lst_new.append(line)

    for items in external_lst_new:
        for cn_item in cn_lst_new:
            if items[0] == cn_item[0]:
                if items[1] == cn_item[1]:

                    #print(items,'______',cn_item)
                    #if items[2] == cn_item[2]:
                    if cn_item[3] =='0/23':
                        result.append(('bgp route--->',items,'---国内路由-->',cn_item,cn_item[0-2],'to',str(int(cn_item[2])+1),'254'))
                    elif cn_item[3] =='0/22':
                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[0-2],'to',str(int(cn_item[2])+3),'254'))
                    elif cn_item[3] =='0/21':
                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[0-2],'to',str(int(cn_item[2])+7),'254'))
                    elif cn_item[3] =='0/20':
                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[0-2],'to',str(int(cn_item[2])+15),'254'))
                    elif cn_item[3] =='0/19':
                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[0-2],'to',str(int(cn_item[2])+31),'254'))
                    elif cn_item[3] =='0/18':
                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[0-2],'to',str(int(cn_item[2])+63),'254'))
                    elif cn_item[3] =='0/17':
                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[0-2],'to',str(int(cn_item[2])+127),'254'))
                    elif cn_item[3] =='0/16':
                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[0-2],'to',str(int(cn_item[2])+255),'254'))

                else:
                        continue
            else:
                        continue

    with open('campare_result.txt','a') as resultfile:
        resultfile.write('前16位相同的IP 地址:'+'\n')
        for items in result:
            resultfile.write(str(items)+'\n')

    resultfile.close()

def compare_8():
    #compare the first number
    cn_lst_new=[]
    external_lst_new=[]
    result=[]
    for line in cn_lst:
        line=line.split('.')
        cn_lst_new.append(line)

    for line in external_lst:
        line=line.split('.')
        external_lst_new.append(line)

    for items in external_lst_new:
        for cn_item in cn_lst_new:
            if cn_item[3] =='0/15':
                if items[0] == cn_item[0]:

                    if int(items[1]) >=int(cn_item[1]) and int(items[1]) <= (int(cn_item[1])+1):

                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[1],'to',str(int(cn_item[1])+1),'255.254'))
            if cn_item[3] =='0/14':
                if items[0] == cn_item[0]:
                    if int(items[1]) >=int(cn_item[1]) and int(items[1]) <= (int(cn_item[1])+3):

                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[1],'to',str(int(cn_item[1])+3),'255.254'))
            if cn_item[3] =='0/13':
                if items[0] == cn_item[0]:
                    if int(items[1]) >=int(cn_item[1]) and int(items[1]) <= (int(cn_item[1])+7):

                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[1],'to',str(int(cn_item[1])+7),'255.254'))
            if cn_item[3] =='0/12':
                if items[0] == cn_item[0]:
                    if int(items[1]) >=int(cn_item[1]) and int(items[1]) <= (int(cn_item[1])+15):

                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[1],'to',str(int(cn_item[1])+15),'255.254'))
            if cn_item[3] =='0/11':
                if items[0] == cn_item[0]:
                    if int(items[1]) >=int(cn_item[1]) and int(items[1]) <= (int(cn_item[1])+31):

                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[1],'to',str(int(cn_item[1])+31),'255.254'))
            if cn_item[3] =='0/10':
                if items[0] == cn_item[0]:
                    if int(items[1]) >=int(cn_item[1]) and int(items[1]) <= (int(cn_item[1])+63):

                        result.append(('bgp route-',items,'---国内路由--',cn_item,cn_item[1],'to',str(int(cn_item[1])+63),'255.254'))


    with open('campare_result15.txt','w') as resultfile:
        resultfile.write('前8位相同的IP 地址:'+'\n')
        for items in result:
            resultfile.write(str(items)+'\n')



if __name__ == '__main__':
    compare_24()
    compare_16()
    compare_8()