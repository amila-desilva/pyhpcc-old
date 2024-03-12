# -*- coding: utf-8 -*-

import logging
import json
import requests
import os
import subprocess
from pyhpcc.authentication import auth
class workunit_submit(object):

    def __init__(self, hpcc, cluster1 = '' , cluster2 = '' ):
        self.hpcc = hpcc
        self.cluster1 = cluster1
        self.cluster2 = cluster2
        self.stateid  = {   'unknown' : 0,
                            'compiled' : 1,
                            'running' : 2,
                            'completed' :3,
                            'failed' : 4,
                            'archived' : 5,
                            'aborting' : 6,
                            'aborted' : 7,
                            'blocked' : 8,
                            'submitted' : 9,
                            'scheduled' :10,
                            'compiling' :11,
                            'wait' :12,
                            'uploadingFiles' : 13,
                            'debugPaused' : 14,
                            'debugRunning' : 15,
                            'paused' : 16,
                            'statesize' : 17
                        }
        
    def write_file(self, querytext, folder, jobname):
        words = jobname.split()
        jobname = '_'.join(words)
        filename  = os.path.join(folder, jobname + '.ecl')
        f = open(filename, 'w')
        f.write(querytext)
        f.close
        return filename
    def get_bashcommand(self,filename, repository):
        
        f = filename.split('.')[0]
        
        outputfile = f + '.eclxml'
        bashcommand = ''' eclcc -legacy  -I {0}  -platform=thor  -E -o {1} {2} -wu'''.format(repository, outputfile,filename)
        
        return bashcommand , outputfile
    
    def get_workload(self):
        payload = {'SortBy' : 'Name', 'Descending':1}

        resp = self.hpcc.Activity(**payload).json()
        len1 = 0
        len2 = 0
        #if 'Running' in  resp['ActivityResponse'].keys():
        if 'Running' in list(resp['ActivityResponse'].keys()):
            workunits  = resp['ActivityResponse']['Running']['ActiveWorkunit']
            for workunit in workunits:
                if workunit['TargetClusterName'] ==  self.cluster1:
                    len1 = len1 + 1
                if workunit['TargetClusterName'] ==  self.cluster2:
                    len2 = len2 + 1

        return len1 , len2

    def create_filename(self,QueryText,working_folder,Jobname):
        self.Jobname = Jobname
        return self.write_file(QueryText, working_folder, Jobname)


    def bash_compile(self,  filename, gitrepository ):

        bashcommand , outputfile = self.get_bashcommand(filename, gitrepository)
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        return output, outputfile
        
    def bash_run(self,compiledfile, cluster ):
        if cluster == '':
            len1 , len2 = self.get_workload()
            if len2 > len1:
                cluster = self.cluster1
            else:
                cluster = self.cluster2
        self.Jobname = self.Jobname.replace(' ' , '_')
        bashcommand = '''ecl run {0} --limit=100 --wait=0 --target={1}  --server={2} --ssl --port={3} -u={4} -pw={5} --name={6} -v'''.format(compiledfile,cluster,self.hpcc.auth.ip,self.hpcc.auth.port,self.hpcc.auth.oauth[0],self.hpcc.auth.oauth[1],self.Jobname)
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        
        return output, error
        
        
        
    def compileworkunit(self, Wuid ,Cluster  = '' ):
        if Cluster == '':
            len1 , len2 = self.get_workload()
            if len2 > len1:
                Cluster = self.cluster1
            else:
                Cluster = self.cluster2
        self.hpcc.wuSubmit(Wuid = Wuid, Cluster = Cluster)
        try:
            w3 = self.hpcc.WUWaitCompiled(Wuid = Wuid)
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            w3 = self.WUWaitCompiled(Wuid= Wuid)
            w3 = json.loads(w3.text)
            return w3['WUWaitResponse']['StateID']
        else:
            w3 = json.loads(w3.text)
            return w3['WUWaitResponse']['StateID']
        
    def createworkunit(self, Action , ResultLimit , QueryText , Jobname ,ClusterOrig ='', data= '' ):

        if ClusterOrig == '':
            len1 , len2 = self.get_workload()

            if len2 > len1:
                ClusterOrig = self.cluster1
            else:
                ClusterOrig = self.cluster2
        if QueryText is None:
            data = {'QueryText':data}
            kwargs = {'data':data}
        else:
            data = {'QueryText':QueryText}
            kwargs = {'data':data}
                
        resp  =   self.hpcc.wuCreateAndUpdate(Action = Action,
                                                    ResultLimit = ResultLimit,
                                                    Jobname   = Jobname,
                                                    ClusterOrig = ClusterOrig, **kwargs)
            
        
        if resp.status_code == 200:
            resp = json.loads(resp.text)
            if ( 'WUUpdateResponse' in resp
                and 'Workunit' in resp['WUUpdateResponse']
                and 'Wuid' in resp['WUUpdateResponse']['Workunit'] ):
                    return resp['WUUpdateResponse']['Workunit']['Wuid']

        else:
            raise ('workunit id not created')
        

    def WUWaitCompiled(self,Wuid):
        try:
            logging.info("session timeout for WUWaitCompiled, starting new session for WUWaitComplete")
            w4 = self.hpcc.WUWaitCompiled(Wuid = Wuid)
        except requests.exceptions.Timeout:
            w4 = self.WUWaitCompiled(Wuid= Wuid)
            return w4
        else:
            return w4
                    


    def WUWaitComplete(self,Wuid):
        try:
            logging.info("session timeout for WuRun, starting new session for WUWaitComplete")
            w4 = self.hpcc.WUWaitComplete(Wuid = Wuid)
        except requests.exceptions.Timeout:
            w4 = self.WUWaitComplete(Wuid= Wuid)
            return w4
        else:
            return w4
        
        
    def runworkunit(self,Wuid,Cluster =''):
        if Cluster == '':
            len1 , len2 = self.get_workload()

            if len2 > len1:
                Cluster = self.cluster1
            else:
                Cluster = self.cluster2
        try:
            w4 = self.hpcc.wuRun(   Wuid = Wuid,
                     Cluster = Cluster,
                    Variables = [])
        except requests.exceptions.Timeout:
            w4 = self.WUWaitComplete(Wuid= Wuid)
            w4 = w4.json()
            
            return w4['WUWaitResponse']['StateID']
        else:
            w4 = json.loads(w4.text)
            state=  w4['WURunResponse']['State']
            return self.stateid[state]

if __name__ == "__main__":
    pass
    