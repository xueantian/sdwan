
# email:xueatian@cisco.com

import requests
import sys
import json
import os
import tabulate
import click
import pprint
import time
import yaml
import six

from requests.packages.urllib3.exceptions import InsecureRequestWarning

def login_information():
    vmanage_host = input('input the vManage IP or hostname:')
    vmanage_port = 8443
    username = input('Input your username:')
    password = input('Input your password:')


vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
username = 'api'
password='Cisco@123'
#username = os.environ.get("username")
#password = os.environ.get("password")

requests.packages.urllib3.disable_warnings()
class rest_api_lib:
    vmanage_host = '10.75.37.247'
    vmanage_port = '8443'
    username = 'api'
    password='Cisco@123'
    def __init__(self, vmanage_host, vmanage_port, username, password):
        self.vmanage_host = vmanage_host
        self.vmanage_port = vmanage_port
        self.session = {}
        self.login(self.vmanage_host, username, password)

    def login(self, vmanage_host, username, password):
        """Login to vmanage"""

        base_url = 'https://%s:%s/' % (self.vmanage_host, self.vmanage_port)

        base_url = 'https://10.75.37.247:8443/'
        login_action = 'j_security_check'

        # Format data for loginForm
        login_data = {'j_username': username, 'j_password': password}

        # Url for posting login data
        login_url = base_url + login_action
        url = base_url + login_url

        sess = requests.session()

        # If the vmanage has a certificate signed by a trusted authority change verify to True

        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if b'<html>' in login_response.content:
            print("Login Failed")
            sys.exit(0)

        self.session[vmanage_host] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s" % (self.vmanage_host, self.vmanage_port, mount_point)
        # print(url)

        response = self.session[self.vmanage_host].get(url, verify=False)

        return response

    def post_request(self, mount_point, payload,
                     headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        """POST request"""
        url = "https://%s:%s/dataservice/%s" % (self.vmanage_host, self.vmanage_port, mount_point)
        # print(url)
        payload = json.dumps(payload)
        # print (payload)

        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, verify=False)
        # print(response.text)
        # exit()
        # data = response
        return response


# Create session with vmanage

vmanage_session = rest_api_lib(vmanage_host, vmanage_port, username, password)

def policy():
   # https://10.75.37.247:8443/dataservice/template/policy/list/dataprefix/35622476-106d-4b7f-ab10-c1fbbff350ca
    # https://10.75.37.247:8443/dataservice/template/policy/list/dataprefix/


    response = vmanage_session.get_request('template/policy/list/dataprefix/').json()

    items = response['data']


    items_detail=response

    print(items_detail)
    with open('template.txt','w') as file:
        file.write(str(items_detail))
        file.close()

if __name__ == "__main__":
    #requests.packages.urllib3.disable_warnings()

    #login_information()
    policy()
