#! /usr/bin/env python
# -*- coding=utf-8 -*-
# email:xueatian@cisco.com
import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# login information of vmanage
vmanage_host ='10.75.37.247'
vmanage_port = '8443'
vmanage_username = 'api'
vmanage_password='Cisco@123'

# Standard vManage API login function
class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, username, password):
        api = "/j_security_check"
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        url = base_url + api
        payload = {'j_username' : username, 'j_password' : password}

        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return(jsessionid[0])
        except:
            if logger is not None:
                logger.error("No valid JSESSION ID returned\n")
            exit()

    @staticmethod
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None

Auth = Authentication()
jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,vmanage_username,vmanage_password)
token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)

if token is not None:
    header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json",'Cookie': jsessionid}

base_url = "https://%s:%s/dataservice"%(vmanage_host, vmanage_port)


# To get the ip addresses list from local file
def get_list():

    with open('prefix_test.txt','r') as file:
            lists=file.readlines()
            for line in lists:
                line=line.rstrip('\n')
                lst.append(line)
    print('new ip prefix number is {}'.format(len(lst)))
    return lst


# the uuid of the policy and prefix-list
data_prefixlist_uuid = '0e20696b-f175-4dd1-8f43-458ddac0f7c9'
vsmart_policy_uuid='1eb30983-652a-42ba-b2d0-ca7ab31983c1'

def deactivate_policy():
    #https://vmanage-ip/dataservice/template/policy/vsmart/deactivate/{policyId}
    vsmartd_payload = {
      "isPolicyActivated": "false",
      "policyId": vsmart_policy_uuid
      }
    policy_payload = json.dumps(vsmartd_payload)
    policy_url=base_url + "/template/policy/vsmart/deactivate/"+vsmart_policy_uuid
    deactivate=requests.post(url=policy_url,headers=header,verify=False,data=policy_payload)


    if deactivate.status_code != 200:
        print(deactivate.raise_for_status)
    else:
        print('the policy has been deactivated now')
        pass


def activate_policy():
    #https://vmanage-ip/dataservice/template/policy/vsmart/activate/{policyId}
    vsmartd_payload = {
                         "isEdited": 'false'
                      }
    policy_payload = json.dumps(vsmartd_payload)
    policy_url=base_url + "/template/policy/vsmart/activate/"+vsmart_policy_uuid
    activate=requests.post(url=policy_url,headers=header,verify=False,data=policy_payload)



    if activate.status_code != 200:
        print(activate.raise_for_status)
    else:
        print('the policy has been activated now')
        pass



# To put the list to prefix list of vManage

def put_prefix_list(lst):
    #https://vmanage-ip/dataservice/template/policy/vsmart
    prefix=[]

    #print(lst)
    for item in lst:
        d={}
        d['ipPrefix'] = item
       # print(d)
        prefix.append(d)
    #print(prefix)
    lens =len(prefix)
    #print(lens)

    read_url = base_url + "/template/policy/list/dataprefix/"+data_prefixlist_uuid
    put_url = base_url + "/template/policy/list/dataprefix/"+data_prefixlist_uuid

    new_list={
              "name": "aboard-ip",
              "type": "dataPrefix",
              "entries": prefix
             }
    payload=json.dumps(new_list)
    r=requests.put(url=put_url,headers=header,verify=False,data=payload)
    response = requests.get(url=read_url, headers=header,verify=False)

    if r.status_code != 200:
        print(r.raise_for_status)
    else:
        print('the new IP prefix input successfully, the input IP number is {}'.format(lens))
        pass

    #curl -X PUT "https://10.75.37.247:8443/dataservice/template/policy/list/dataprefix/35622476-106d-4b7f-ab10-c1fbbff350ca" -H "accept: application/json" -H "Content-Type: application/json" -H "X-XSRF-TOKEN: 087333D358ECC54D4CE29F10470DFB7B2511CBA1B2074980291F778367C042C477F2C70114D3776A5D9DFE359978DBE9C2E9" -d "{\"name\":\"external_IP1\",\"description\":\"Desc Not Required\",\"type\":\"dataPrefix\",\"listId\":\"1066ffec-e6ab-426a-b303-434d41b0a4a61\",\"entries\":[{\"ipPrefix\":\"1.1.1.2/32\"}]}"

    if response.status_code == 200:
        items = response.json()
       # print(items)
    else:
        print("Failed " + str(response.text))
        exit()

def countdown(t):
    while t:
        print('---------------wait {} seconds ------------'.format(t))
        time.sleep(1)
        t-=1

if __name__ == "__main__":
    lst=[]
    get_list()
    print('-------------------------------------------')
    print('first, to deactivate the policy')
    print('-------------------------------------------')
    #deactivate_policy()

    print('--------------To wait 30 seconds ------------')

    countdown(30)
    print('Second,update the prefix list')
    print('-------------------------------------------')
    #put_prefix_list(lst)

    print('---------------To wait 20 seconds ------------')
    countdown(20)
    print('Finally,activate the policy again!')
    print('-------------------------------------------')
    #activate_policy()


