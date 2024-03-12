"""
The following script is used to submit a workunit to regular clusters on a given environment.
"""
import os
import pyhpcc.api as api
from pyhpcc.authentication import auth
from pyhpcc.workunit_submit import workunit_submit as ws

# Configurations
username = os.getenv('HPCC_USERNAME')
password = os.environ['HPCC_PASSWORD']

ip = '' #enter the domain or IP address of HPCC Systems environment
port = 3001 #enter the port, ex: 3001
auth1 = auth(ip, port, username, password, True, 'https')
hpcc = api.hpcc(auth1)
cluster1 = '' #enter target thor cluster
cluster2 = '' #enter target thor cluster
wuID = '' # leave blank
jobname = "Example" # enter WU job name
querytext = "OUTPUT('Hiii');" #enter your ECL code

# *** To read ECL script from a file ***
# with open('ECLScript.txt','r') as ecl_file:
#     querytext = ecl_file.read()


work_s = ws(hpcc, cluster1=cluster1, cluster2=cluster2)

wuID = work_s.createworkunit(Action=1,
                             ResultLimit=100,
                             QueryText=querytext,
                             Jobname=jobname,
                             ClusterOrig=cluster1)

wustate = work_s.compileworkunit(Wuid=wuID, Cluster=cluster1)

## Run the submitted workunit
if wustate in [1, 3]: 
    print ('Running Workunit with ID ' + str(wuID))
    w4 = work_s.runworkunit(Wuid=wuID, Cluster=cluster1)

print ('Workunit with ID ' + str(wuID) + ', State: ' + str(w4))
