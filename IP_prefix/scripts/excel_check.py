#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# email:xueatian@cisco.com

import openpyxl

workbook=openpyxl.load_workbook('Book1.xlsx')
sheet=workbook['Sheet4']

#get the value
H_value=sheet['H1'].value
V_value=sheet['V1'].value
Z_value=sheet['Z1'].value

print(H_value)
print(V_value)
print(Z_value)
i =1
while i < 282:
    H_value=sheet['H{}'.format(i)].value
    V_value=sheet['V{}'.format(i)].value
    Z_value=sheet['Z{}'.format(i)].value
    if H_value >=V_value and H_value <=Z_value:
        sheet['AD{}'.format(i)].value = True
    else:
        sheet['AD{}'.format(i)].value = False
    i+=1

workbook.save('Book1.xlsx')
