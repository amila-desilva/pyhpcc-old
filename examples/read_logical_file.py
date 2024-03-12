"""
The following script is used to read a logical file.
"""
from pyhpcc.authentication import auth
from pyhpcc.api import hpcc
import os
import json
import pandas as pd

# Configuration
user = os.environ['HPCC_USERNAME']
password = os.environ['HPCC_PASSWORD']
environment = os.environ['HPCC_ENVIRONMENT']
port = os.environ['HPCC_PORT']
require_auth = True
protocol = 'https'
logical_file_name = '' # Enter the logical file name here
num_rows_to_return = 100

try:
    # Create a hpcc object
    hpcc_obj = hpcc(auth(environment, port, user, password, require_auth, protocol))

    # Read logical file and return a pandas dataframe
    response = hpcc_obj.getFileInfo(LogicalName=logical_file_name, Count=num_rows_to_return).json()
    response = response['WUResultResponse']['Result']['Row']
    df_response = pd.read_json(json.dumps(response), dtype=object)
    print(df_response)

except Exception as e:
    print(e)
