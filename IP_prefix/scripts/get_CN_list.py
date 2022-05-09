#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# email:xueatian@cisco.com

import requests
import re
import lxml.etree
url1='https://ispip.clang.cn/'
url='https://ispip.clang.cn/all_cn_cidr.html'
resp=requests.get(url)
resp.encoding='utf-8'

#print(resp.text)
obj1=re.compile(r"# 脚本自动生成\,如有错漏或任何建议\,请联系admin\[at\]clang\.cn\n###########################################################(?P<ip_prefix>.*?)##########################  END  ##########################",re.S)
obj2=re.compile(r"<html xmlns(?P<ip_prefix>.*?)xhtml",re.S)

result1=obj1.finditer(resp.text)
print(result1)
for items in result1:
    lst=items.group('ip_prefix')
    print(lst)

with open('cn_list_auto.txt','w') as file:
    file.write(lst)
