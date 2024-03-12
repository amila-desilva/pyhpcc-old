"""
This script uploads a given file to an HPCC Systems landing zone.
"""
import os
from pyhpcc.authentication import auth
from pyhpcc.api import hpcc

# Configurations
environment = os.environ['HPCC_ENVIRONMENT']
port = os.environ['HPCC_PORT']
user = os.getenv('HPCC_USERNAME')
password = os.environ['HPCC_PASSWORD']
require_auth = True
protocol = 'https'
file_path = r'C:\Folder\Temp_File_Delete_Later.txt'
file_name = 'Temp_File_Delete_Later.txt'
ip_address = os.environ['HPCC_LANDING_ZONE_IP']
landing_zone_path = os.environ['HPCC_LANDING_ZONE_PATH']

try:
    # Authenticate and create an hpcc object 
    hpcc_object = hpcc(auth(environment, port, user, password, require_auth, protocol))

    read_file = open(file_path, 'rb')
    file_to_upload = {'file': (file_name, read_file, 'text/plain ', {'Expires': '0'})}
    payload = {
        'upload_': '' , 
        'rawxml_': 1 , 
        'NetAddress': ip_address,
        'OS': 2, 
        'Path': landing_zone_path, 
        'files': file_to_upload  
    }
    response = hpcc_object.UploadFile(**payload).json()

    try:
        if response['UploadFilesResponse']['UploadFileResults']['DFUActionResult'][0]['Result'] == u'Success':
            print("File uploaded successfully.")
        else:
            print("File upload unsuccessful.")
    except:
        print("File upload unsuccessful.")

except Exception as e:
    print(e)

