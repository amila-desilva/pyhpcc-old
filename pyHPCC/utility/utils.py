from __future__ import print_function
import xml.etree.ElementTree as ET
import pandas as pd

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
from pyhpcc import workunit_submit as ws
import json

import six


def convert_to_utf8_str(arg):
    # written by Michael Norton (http://docondev.blogspot.com/)
    if isinstance(arg, six.text_type):
        arg = arg.encode('utf-8')
    elif not isinstance(arg, bytes):
        arg = six.text_type(arg).encode('utf-8')
    return arg

def get_graph_skew(response):
    resp_json = response.json()
    graphs =[]
    xml =  resp_json['WUGetGraphResponse']['Graphs']['ECLGraphEx'][0]['Graph']  

    root = ET.fromstringlist(xml)
    
    for node in root.findall('./node/att/graph/node'):
        graph = {'subgraphid': node.get('id')}
        for child in node:
            if child.get('name') == 'SkewMaxLocalExecute':
                graph['skewmax'] = child.get('value') 
            if child.get('name') =='TimeAvgLocalExecute':
                graph['avgtime'] = child.get('value')
            if child.get('ecl') =='TimeAvgLocalExecute':
                graph['ecl'] = child.get('value')
        graphs.append(graph)
#    for child in root.iter('node'):
##        print(child.get('id'))
#        for sub in child.iter():
##            
#            if sub.get('name')=='SkewMaxLocalExecute':
#                graphs['SkewMax'] = sub.get('value')
##                print (graphs['SkewMax'])
#                graphs['subgraphid'] = child.get('id')
    return graphs
    
def getfileStatus(arg):
    argET = ET.fromstring(arg.content)
    for child in argET:
        if child.tag == 'NumFiles':
            return child.text
            
def getfileType(arg):
    argET = ET.fromstring(arg.content)
    data_dict =  {}
    for child in argET:
        if child.tag == 'DFULogicalFiles':
            for dfufile in child:
                if dfufile.tag == 'DFULogicalFile':
                    for fileinfo in dfufile:
                        if fileinfo.tag == 'NodeGroup':
                            data_dict.update({fileinfo.tag : fileinfo.text})
                        if fileinfo.tag == 'isSuperfile':
                            data_dict.update({fileinfo.tag : fileinfo.text})
                        if fileinfo.tag == 'Totalsize':
                            data_dict.update({fileinfo.tag : fileinfo.text})
                        if fileinfo.tag == 'RecordCount':
                            data_dict.update({fileinfo.tag : fileinfo.text})
                        if fileinfo.tag == 'ContentType':
                            data_dict.update({fileinfo.tag : fileinfo.text})
    return data_dict                              

def getSubfileNames(arg):
    argET = ET.fromstring(arg.content)
    subfilenamelist = []
    for child in argET:
        if child.tag == 'DFUInfoResponse':
            for dfufile in child:
                if dfufile.tag == 'subfiles':
                    for fileinfo in dfufile:
                        if fileinfo.tag == 'Item':
                            subfilenamelist.append(fileinfo.text)
    return pd.Series(subfilenamelist)


# noinspection PyAssignmentToLoopOrWithParameter
def getflatdata(arg):
    list_dict = []    
    argET = ET.fromstring(arg.content)
    for child in argET:
        if child.tag == 'Result':
            # noinspection PyAssignmentToLoopOrWithParameter
            for child in child:
                if child.tag == 'Dataset':
                    for row in child:
                        data_dict =  {}
                        for rowdata in row:
                            data_dict[rowdata.tag] = rowdata.text
                        list_dict.append(data_dict)            
    return pd.DataFrame(list_dict)

def getcsvdata(arg,csvSeperator,csvHeader):
    argET = ET.fromstring(arg.content)
    list_dict = []
    for child in argET:
        if child.tag == 'Result':
            for child in child:
                if child.tag == 'Dataset':
                    for row in child:
                        data_dict =  {}
                        for rowdata in row:
                            data_dict[rowdata.tag] = rowdata.text + '\n'
                        list_dict.append(data_dict)    
    xmlstr = "";
    for eachdict in list_dict:
        for key, value in list(eachdict.items()):
        #for key,value in eachdict.items():
            if key == 'line':
                if "None" in str(value):
                    xmlstr = xmlstr
                else:
                    xmlstr = xmlstr + str(value);
    csvformatdata=StringIO(xmlstr)
    if(csvHeader == 0):
        return(pd.read_csv(csvformatdata, sep=csvSeperator, header=csvHeader))
    else:
        return(pd.read_csv(csvformatdata, sep=csvSeperator, header=None))

def desprayfile(hpcc,querytext,Cluster,jobn): 

    work_s = ws.workunit_submit(hpcc)
    wuID = ''
    wuID  = work_s.createworkunit(Action = 1,
                                ResultLimit = 100,
                                QueryText = querytext,
                                Jobname   = jobn,
                                ClusterOrig = Cluster)
    wustate = work_s.complieworkunit(Wuid = wuID,
                                Cluster = Cluster)
    if wustate in [1,3]:#['failed','aborted','archived','unknown_onserver']:
        print ('Running Workunit with ID '+str(wuID))
        w4 = work_s.runworkunit(Wuid = wuID,
                        Cluster = Cluster)
        w4 = json.loads(w4.text)
        return(w4['WURunResponse']['State'])

def checkfileexistence(arg):
    argET = ET.fromstring(arg.content)
    i = 0
    for child in argET:
        if child.tag == 'Prefix':
            if child.text is None:
                i = i + 0
            else:
                i = i + 1
        if child.tag == 'NodeGroup':
             if child.text is None:
                i = i + 0
             else:
                i = i + 1
        if child.tag == 'Owner':
              if child.text is None:
                i = i + 0
              else:
                i = i + 1
        if child.tag == 'FileType':
              if child.text is None:
                i = i + 0
              else:
                i = i + 1
        if child.tag == 'StartDate':
              if child.text is None:
                i = i + 0
              else:
                i = i + 1
    return i          
