# -*- coding: utf-8 -*-

import getpass
import sys
import requests
import pandas as pd
from xml.etree import ElementTree as ET
from pyhpcc import api
import os
from pyhpcc.authentication import auth
from pyhpcc import utils

class ReadFileInfo(object):

    def __init__(self,hpcc, 
                  logicalFileName,cluster,fileType, fileSizelimit = 25, ifExists = -1, isSuperFile = -1,actualFileSize = -1,recordCount = -1,desprayIP = '', desprayPath = '', desprayallowoverwrite = 'true', shouldDespray = False, checkStatus = False, csvSeperatorforRead = ',', readStatus = 'Not read', desprayFromCluster = '', csvHeaderFlag = 0):

        """ ReadFileInfo instance Constructor

        :param hpcc: instance of the hpcc Class
        :param logicalFileName: name of the file to get
        :param cluster: name of the cluster the file resides in
        :param fileSizelimit: maximum limit for read ( in MB), default: 100 MB     
        :param fileType: type of the file
        :param ifExists: flag to mark the existence of a file     
        :param isSuperFile: flag to mark if the file is a superFile
        :param acutalFileSize: file size of the file
        :param recordCount: record count for the file
        """

        self.hpcc = hpcc
        self.logicalFileName = logicalFileName
        self.cluster = cluster
        self.fileSizelimit = fileSizelimit
        self.fileType = fileType
        self.ifExists = ifExists
        self.isSuperFile = isSuperFile
        self.actualFileSize = actualFileSize
        self.recordCount = recordCount
        self.desprayIP = desprayIP
        self.desprayPath = desprayPath
        self.desprayallowoverwrite = desprayallowoverwrite
        self.shouldDespray = shouldDespray
        self.checkStatus = checkStatus
        self.csvSeperatorforRead = csvSeperatorforRead
        self.readStatus = readStatus
        self.desprayFromCluster = desprayFromCluster
        self.csvHeaderFlag = csvHeaderFlag
        
        
    def checkIfFileExistsAndIsSuperFile(self,clusterFromUser):
        self.checkStatus = True
        fileSearch = self.hpcc.fileQuery(LogicalName = self.logicalFileName,LogicalFileSearchType = 'Logical Files and Superfiles')        
        self.ifExists = utils.getfileStatus(fileSearch)
        if self.ifExists != 0 and self.ifExists != '0':
            arrFESF = utils.getfileType(fileSearch)
            self.cluster = arrFESF['NodeGroup'] if arrFESF['NodeGroup'] is not None else clusterFromUser
            self.ifSuperFile = arrFESF['isSuperfile'] if arrFESF['isSuperfile'] is not None else ''
            self.actualFileSize = int(arrFESF['Totalsize'].replace(',', '')) if arrFESF['Totalsize'] is not None else ''
            self.fileType = arrFESF['ContentType'] if arrFESF['ContentType'] is not None else self.fileType
            if bool(arrFESF):
                if(arrFESF['RecordCount'] != ''):
                    self.recordCount = 0 if arrFESF['RecordCount'] is None else int(arrFESF['RecordCount'].replace(',', ''))
                else:
                    self.recordCount = -2
        else:
            self.fileType = ''
            self.ifSuperFile = ''
            self.actualFileSize = None
            self.recordCount = None
            self.cluster = ''
            self.readStatus = "File doesn't exist"
            
    def setFilename(self, filename): 
        self.logicalFileName = filename
        self.checkIfFileExistsAndIsSuperFile(self.cluster)
        
    def getSubFileInformation(self):
        if(not self.checkStatus):
            self.checkIfFileExistsAndIsSuperFile(self.cluster)
        if(self.isSuperFile == 1):
            subFileInfo = self.hpcc.getSubFileInfo(Name = self.logicalFileName)
            return(utils.getSubfileNames(subFileInfo))
        else:
            return('Not a superfile')
        
    def checkfileinDFU(self):
            statusDetails = self.hpcc.checkFileExists(Name = self.logicalFileName)
            status = utils.checkfileexistence(statusDetails)
            if status == 0:
                return False
            else:
                return True
                
    def getData(self):
        self.checkIfFileExistsAndIsSuperFile(self.cluster)
        if self.ifExists != 0 and self.ifExists != '0':
            filesizeinMB = (self.actualFileSize/1024)/1024
            if(filesizeinMB > self.fileSizelimit or self.fileType == 'xml' or self.shouldDespray):
                if(self.desprayIP != '' and self.desprayPath != ''):
                    QueryString = "IMPORT STD; STD.file.despray(~\'"+self.logicalFileName +"\',\'"+self.desprayIP+"\',\'"+self.desprayPath+"\',,,,"+self.desprayallowoverwrite+");"
                    clusterfrom = ''
                    if(self.desprayFromCluster == ''):
                        clusterfrom = self.cluster
                    else:
                        clusterfrom = self.desprayFromCluster
                    setattr(self.hpcc,'response_type','.json')   
                    self.readStatus = utils.desprayfile(self.hpcc,QueryString,clusterfrom, 'Despraying : ' +self.logicalFileName)
                else:
                    self.readStatus = 'Unable to despray with the given input values. Please provide values for despray IP and folder'
            else:
                if(self.recordCount == -2):
                    countupdated = 9223372036854775807
                else:
                    countupdated = self.recordCount        
                    flatcsvresp = self.hpcc.getFileInfo(LogicalName = self.logicalFileName, Cluster = self.cluster, Count = countupdated)
                    if(self.fileType == 'flat'):
                        self.readStatus = 'Read'
                        return(utils.getflatdata(flatcsvresp))
                    else:
                        self.readStatus = 'Read'
                        return(utils.getcsvdata(flatcsvresp, self.csvSeperatorforRead, self.csvHeaderFlag))
        else:
            self.readStatus = "File doesn't exist"            