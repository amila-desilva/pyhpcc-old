# -*- coding: utf-8 -*-

"""
This script queries a roxie service using a custom payload.
"""
from pyhpcc.authentication import auth
from pyhpcc import roxie_api
import os

user = os.getenv('HPCC_USERNAME')
password = os.environ['HPCC_PASSWORD']
ip = '' # Enter the IP address here
port = '' # Enter the port here
roxie_auth = auth(ip, port, user, password, True)
search_service = '' # Enter the search service here
roxie_port = '' # Enter the roxie port here
roxie = roxie_api.roxie(roxie_auth, searchservice=search_service, roxie_port=roxie_port)

payload = { 'data':'1' }

try:
    resp = roxie.roxie_call(**payload )
    
except:
    pass
else:
    resp = resp.json()
    print(resp)
    serviceResponse = list(resp.keys())[0]
    print(serviceResponse)