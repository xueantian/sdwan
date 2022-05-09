#!/usr/bin/python
import requests
import zipfile
import os
import csv
import json
import ipaddress
import uuid
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# Enter your vManage credentials, data-prefix-list-uuid, vSmart-polocy-uuid
vManage_IP = "FQDN/IPaddress"
vManage_ID = "admin"
vManage_Password = "admin"
Data_prefix_list_uuid = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

def download(url):
    file_name = os.path.basename(url)
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024):
                file.write(chunk)

def geoip(geourl):
    download(geourl)
    with zipfile.ZipFile('GeoLite2-Country-CSV.zip') as zf:
     uzf = zf.extractall()
    all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    latest_subdir = max(all_subdirs, key=os.path.getmtime)
    os.chdir(latest_subdir)
    reader = csv.reader(open(r"./GeoLite2-Country-Blocks-IPv4.csv"),delimiter=',')
    #China country code is1814991
    filtered = filter(lambda p: "1814991" == p[2], reader)
    l = []
    for line in filtered:
     l.append(line[0])
    return l

def login(vmanage_ip, username, password):
    session = {}
    base_url_str = 'https://%s:443/'%vmanage_ip
    login_action = '/j_security_check'
    login_data = {'j_username' : username, 'j_password' : password}
    login_url = base_url_str + login_action
#    url = base_url_str + loginyy_url
    url = base_url_str
    sess = requests.session()
    #URL for retrieving client token
    token_url = base_url_str + 'dataservice/client/token'

    # If the vmanage has a certificate signed by a trusted authority change verify to True
    login_response = sess.post(url=login_url, data=login_data, verify=False)
    login_token  = sess.get(url=token_url, verify=False)
    try:
        if login_response.status_code == 200 and login_token.status_code == 200 :
            sess.headers['X-XSRF-TOKEN'] = login_token.content
            session[vmanage_ip] = sess
            print(sess.cookies)
            # global sessions
            # sessions = session[vmanage_ip]
            return session[vmanage_ip]
        elif '<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)
        else:
            print("Unknown exception")
    except Exception as err:
        return

def put_prefix_list_builder(list_IPv4):
    lst = [] # List of IP Prefixes
    # Change list_IPv4 to dictionary per line
    for pn in list_IPv4:
        d = {}
        d['ipPrefix'] = pn
        lst.append(d)
    json.dumps(list_IPv4)
    payload = {
                  "name": "china-geoip",
                  "type": "dataPrefix",
                  "entries": lst
                }
    test = json.dumps(payload)
    #print(test)
    headers = {'Content-Type': 'application/json'}
    sessions = login(vManage_IP, vManage_ID, vManage_Password)
    url = 'https://'+vManage_IP+':443/dataservice/template/policy/list/dataprefix/'+Data_prefix_list_uuid
    print('vManage API URL :'+url)
    r = sessions.put(url, data=test, headers=headers, verify=False)
    if r.status_code != 200:
        print(r.raise_for_status)
    else:
        return

if __name__ == '__main__':
    geourl = 'https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip'
    list_IPv4 = geoip(geourl)
    put_prefix_list_builder(list_IPv4)