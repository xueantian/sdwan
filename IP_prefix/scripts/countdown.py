#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# email:xueatian@cisco.com
import time
def countdown(t):
    while t:
        print('time is:{}'.format(t))
        time.sleep(1)
        t-=1

if __name__ == '__main__':
    countdown(5)