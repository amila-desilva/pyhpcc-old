# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

from pyhpcc.binder import wrapper


class hpcc(object):
    """HPCC API"""

    def __init__(self, auth,
                 timeout=1200, response_type='.json'):
        """ Api instance Constructor
        :param cache: Cache to query if a GET method is used, default:None
        :param retry_count: number of allowed retries, default:0
        :param retry_delay: delay in second between retries, default:0
        :param retry_errors: default:None
        :param timeout: delay before to consider the request as timed out in seconds, default:60

        :raise TypeError: If the given parser is not a ModelParser instance.
        """
        self.auth = auth
        self.timeout = timeout
        self.response_type = response_type

    @property
    def get_wuinfo(self):
        """ :reference: /WsWorkunits/WUInfo.json
            :allowed_param: 'Wuid', 'TruncateEclTo64k','IncludeExceptions','IncludeGraphs',
                            'IncludeSourceFiles','IncludeResults','IncludeResultsViewNames',
                            'IncludeVariables','IncludeTimers','IncludeResourceURLs','IncludeDebugValues',
                            'IncludeApplicationValues','IncludeWorkflows','IncludeXmlSchemas','SuppressResultSchemas',
                            'rawxml_'
        """
        return wrapper(
            api=self,
            path='WsWorkunits/WUInfo', payload_list=True,
            allowed_param=['Wuid',
                           'TruncateEclTo64k',
                           'IncludeExceptions',
                           'IncludeGraphs',
                           'IncludeSourceFiles',
                           'IncludeResults',
                           'IncludeResultsViewNames',
                           'IncludeVariables',
                           'IncludeTimers',
                           'IncludeResourceURLs',
                           'IncludeDebugValues',
                           'IncludeApplicationValues',
                           'IncludeWorkflows',
                           'IncludeXmlSchemas',
                           'SuppressResultSchemas',
                           'rawxml_'])

    @property
    def get_wuresult(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUResult', payload_list=True,
            allowed_param=['Wuid',
                           'Sequence',
                           'ResultName',
                           'LogicalName',
                           'Cluster',
                           'false',
                           'FilterBy',
                           'Start',
                           'Count'])

    @property
    def getdfuInfo(self):
        return wrapper(
            api=self,
            path='WsDfu/DFUInfo', payload_list=True,
            allowed_param=["Name",
                           "Cluster",
                           "UpdateDescription",
                           "FileName",
                           "FileDesc"])

    @property
    def wuCreateAndUpdate(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUCreateAndUpdate', payload_list=True,
            allowed_param=['Wuid',
                           'State',
                           'StateOrig',
                           'Jobname',
                           'JobnameOrig',
                           'QueryText',
                           'Action',
                           'Description',
                           'DescriptionOrig',
                           'AddDrilldownFields',
                           'ResultLimit',
                           'Protected',
                           'ProtectedOrig',
                           'PriorityClass',
                           'PriorityLevel',
                           'Scope',
                           'ScopeOrig',
                           'ClusterSelection',
                           'ClusterOrig',
                           'XmlParams',
                           'ThorSlaveIP',
                           'QueryMainDefinition',
                           'DebugValues',
                           'ApplicationValues'])

    @property
    def wuSubmit(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUSubmit', payload_list=True,
            allowed_param=['Wuid',
                           'Cluster',
                           'Queue',
                           'Snapshot',
                           'MaxRunTime',
                           'BlockTillFinishTimer',
                           'SyntaxCheck',
                           'NotifyCluster'])

    @property
    def wuRun(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WURun', payload_list=True,
            allowed_param=['QuerySet',
                           'Query',
                           'Wuid',
                           'CloneWorkunit',
                           'Cluster',
                           'Wait',
                           'Input',
                           'NoRootTag',
                           'DebugValues',
                           'Variables',
                           'ApplicationValues',
                           'ExceptionSeverity'])

    @property
    def get_wuquery(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUQuery', payload_list=True,
            allowed_param=['Wuid',
                           'Type',
                           'Cluster',
                           'RoxieCluster',
                           'Owner',
                           'State',
                           'StartDate',
                           'EndDate',
                           'ECL',
                           'Jobname',
                           'LogicalFile',
                           'LogicalFileSearchType',
                           'ApplicationValues',
                           'After',
                           'Before',
                           'Count',
                           'PageSize',
                           'PageStartFrom',
                           'PageEndAt',
                           'LastNDays',
                           'Sortby',
                           'false',
                           'CacheHint'])

    @property
    def wuQuery(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUQuery', payload_list=True,
            allowed_param=['Wuid',
                           'Type',
                           'Cluster',
                           'RoxieCluster',
                           'Owner',
                           'State',
                           'StartDate',
                           'EndDate',
                           'ECL',
                           'Jobname',
                           'LogicalFile',
                           'LogicalFileSearchType',
                           'ApplicationValues',
                           'After',
                           'Before',
                           'Count',
                           'PageSize',
                           'PageStartFrom',
                           'PageEndAt',
                           'LastNDays',
                           'Sortby',
                           'Descending',
                           'CacheHint'])

    @property
    def fileQuery(self):
        return wrapper(
            api=self,
            path='WsDfu/DFUQuery', payload_list=True,
            allowed_param=['LogicalName',
                           'Description',
                           'Owner',
                           'RoxieCluster',
                           'Owner',
                           'NodeGroup',
                           'FileSizeFrom',
                           'FileSizeTo',
                           'FileType',
                           'StartDate',
                           'EndDate',
                           'ToTime',
                           'PageStartFrom',
                           'PageSize'])

    @property
    def getFileInfo(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUResult', payload_list=True,
            allowed_param=['LogicalName',
                           'Cluster',
                           'Count'])

    @property
    def WUWaitCompiled(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUWaitCompiled', payload_list=True,
            allowed_param=['Wuid',
                           'Wait',
                           'ReturnOnWait'])

    @property
    def WUWaitComplete(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUWaitComplete', payload_list=True,
            allowed_param=['Wuid',
                           'Wait',
                           'ReturnOnWait'])

    @property
    def getSubFileInfo(self):
        return wrapper(
            api=self,
            path='WsDfu/DFUInfo', payload_list=True,
            allowed_param=['Name'])

    @property
    def checkFileExists(self):
        return wrapper(
            api=self,
            path='WsDfu/DFUQuery', payload_list=True,
            allowed_param=['LogicalName'])

    @property
    def TpClusterInfo(self):
        return wrapper(
            api=self,
            path='WsTopology/TpClusterInfo', payload_list=True,
            allowed_param=['Name'])

    @property
    def Activity(self):
        return wrapper(
            api=self,
            path='WsSMC/Activity', payload_list=True,
            allowed_param=['Sortby', 'Descending'])

    @property
    def UploadFile(self):
        return wrapper(api=self,
                       path='FileSpray/UploadFile',
                       payload_list=True,
                       allowed_param=['upload_',
                                      'rawxml_',
                                      'NetAddress',
                                      'Path',
                                      'OS']
                       )

    @property
    def DropZoneFiles(self):
        return wrapper(api=self,
                       path='FileSpray/DropZoneFiles',
                       payload_list=True,
                       allowed_param=['id',
                                      'rawxml_']
                       )

    @property
    def dfuQuery(self):
        return wrapper(
            api=self,
            path='WsDfu/DFUQuery', payload_list=True,
            allowed_param=["Prefix",
                           "NodeGroup",
                           "ContentType",
                           "LogicalName",
                           "Description",
                           "Owner",
                           "StartDate",
                           "EndDate",
                           "FileType",
                           "FileSizeFrom",
                           "FileSizeTo",
                           "FirstN",
                           "PageSize",
                           "PageStartFrom",
                           "Sortby",
                           "Descending",
                           "OneLevelDirFileReturn",
                           "CacheHint",
                           "MaxNumberOfFiles",
                           "IncludeSuperOwner"])


    @property
    def getDfuWorkunitInfo(self):
        return wrapper(
            api=self,
            path='FileSpray/GetDFUWorkunit', payload_list=True,
            allowed_param=["wuid"])

    @property
    def getDfuWorkunits(self):
        return wrapper(
            api=self,
            path='FileSpray/GetDFUWorkunits', payload_list=True,
            allowed_param=["Wuid",
                           "Owner",
                           "Cluster",
                           "StateReq",
                           "Type",
                           "Jobname",
                           "PageSize",
                           "CurrentPage",
                           "PageStartFrom",
                           "Sortby",
                           "Descending",
                           "CacheHint", ])

    @property
    def sprayVariable(self):
        return wrapper(
            api=self,
            path='FileSpray/SprayVariable', payload_list=True,
            allowed_param=["sourceIP",
                           "sourcePath",
                           "srcxml",
                           "sourceMaxRecordSize",
                           "sourceFormat",
                           "NoSourceCsvSeparator",
                           "sourceCsvSeparate",
                           "sourceCsvTerminate",
                           "sourceCsvQuote",
                           "sourceCsvEscape",
                           "sourceRowTag",
                           "destGroup",
                           "destLogicalName",
                           "overwrite",
                           "replicate",
                           "ReplicateOffset",
                           "maxConnections",
                           "throttle",
                           "transferBufferSize",
                           "prefix",
                           "nosplit",
                           "noRecover",
                           "compress",
                           "push",
                           "pull",
                           "encrypt",
                           "decrypt",
                           "failIfNoSourceFile",
                           "recordStructurePresent",
                           "quotedTerminator",
                           "sourceRowPath",
                           "isJSON"]
        )

    @property
    def sprayFixed(self):
        return wrapper(
            api=self,
            path='FileSpray/SprayFixed', payload_list=True,
            allowed_param=["sourceIP",
                           "sourcePath",
                           "srcxml",
                           "sourceFormat",
                           "sourceRecordSize",
                           "destGroup",
                           "destLogicalName",
                           "overwrite",
                           "replicate",
                           "ReplicateOffset",
                           "maxConnections",
                           "throttle",
                           "transferBufferSize",
                           "prefix",
                           "nosplit",
                           "norecover",
                           "compress",
                           "push",
                           "pull",
                           "encrypt",
                           "decrypt",
                           "wrap"
                           "failIfNoSourceFile",
                           "recordStructurePresent",
                           "quotedTerminator"]
        )
    @property
    def WUUpdate(self):
        return wrapper(
            api=self,
            path='WsWorkunits/WUUpdate', payload_list=True,
            allowed_param=[ 
            'Wuid',
            'State',
            'StateOrig',
            'Jobname',
            'JobnameOrig',
            'QueryText',
            'Action',
            'Description',
            'DescriptionOrig',
            'AddDrilldownFields',
            'ResultLimit',
            'Protected',
            'ProtectedOrig',
            'PriorityClass',
            'PriorityLevel',
            'Scope',
            'ScopeOrig',
            'ClusterSelection',
            'ClusterOrig',
            'XmlParams',
            'ThorSlaveIP',
            'QueryMainDefinition',
            'DebugValues',
            'ApplicationValues',
           ]
        )
    @property
    def getgraph(self):
        """ :reference: http://ip:port/WsWorkunits/WUGetGraph.json
            :allowed_param: 'Wuid', 'GraphName', 'rawxml_'
        """
        return wrapper(
            api=self,
            path='WsWorkunits/WUGetGraph', payload_list=True,
            allowed_param=[ 'Wuid', 'GraphName', 'rawxml_'])
        
        
    @property
    def downloadfile(self):
        """ :reference: http://ip:port/WsWorkunits/WUGetGraph.json
            :allowed_param: 'Name', 'NetAddress', 'Path', 'OS'
        """
        return wrapper(
            api=self,
            path='FileSpray/DownloadFile', payload_list=True,
            allowed_param=[ 'Name', 'NetAddress', 'Path','OS'])
        
    @property
    def AddtoSuperfileRequest(self):
         return wrapper(
            api=self,
            path='WsDfu/AddtoSuperfile', payload_list=True,
            allowed_param=[ 'Superfile', 'ExistingFile'])       
            
    @property
    def fileList(self):
         return wrapper(
            api=self,
            method= 'POST',
            path='FileSpray/FileList', payload_list=True,
            allowed_param=[ 'Netaddr', 'Path','Mask','OS','rawxml_']) 

     