"""
The following script is used to submit a workunit to the eclcc clusters on a given environment using code from a Git repo.
"""
import os
from pyhpcc.authentication import auth
from pyhpcc.api import hpcc
import pyhpcc.workunit_submit as ws

# Configurations
user = os.getenv('HPCC_USERNAME')
password = os.environ['HPCC_PASSWORD']

environment = '' #enter the domain or IP address of HPCC Systems environment 
port = 3001 #enter the port, ex: 3001
require_auth = True
protocol = 'https'
cluster1 = '' #enter target thor cluster
cluster2 = '' #enter target thor cluster
eclQuery = '''OUTPUT('Hello World'); '''

# *** To read ECL script from a file ***
# with open('ECLScript.txt','r') as ecl_file:
#     eclQuery = ecl_file.read()

jobName = 'HelloWorld'
workingFolder = os.getcwd() # Directory where ECL and compiled files generated via code will be stored
gitRepo = r'' # Directory where ECL git repository resides 

try:
    # Create a hpcc object
    hpccObj = hpcc(auth(environment, port, user, password, require_auth, protocol))

    # Compile the query
    work_s = ws.workunit_submit(hpccObj, cluster1=cluster1, cluster2=cluster2)
    filename = work_s.create_filename(QueryText=eclQuery, Jobname=jobName, working_folder=workingFolder)  # ECL file created
    output, outputfile = work_s.bash_compile(filename, gitrepository=gitRepo)
    print("Compiled file: " + outputfile)

    # If no error found during compile, submit the workunit
    if str(output).find('error') == -1:
        output, error = work_s.bash_run(outputfile, '') # Submit the workunit. 
        # PyHPCC will intelligently schedule workunit on one of the two clusters on line 34 with least activity
        index = str(output).find('running')
        wuid = str(output)[:index-1] # Get the workunit id
        _ = work_s.WUWaitComplete(wuid) # Wait for the workunit to complete
    else:
        print(str(output))

    print(f"{wuid} submitted successfully")

except Exception as e:
    print(e)
