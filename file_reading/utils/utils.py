import logging
logger = logging.getLogger(__name__)
from rest_framework.response import Response
import config
from file_reading.serializer.S100UPLOADFILE import *
from file_reading.serializer.S100UPDATEFILE import *
import h5py
from django.http import HttpResponse
import json
from datetime import datetime, timezone
import os

def saving_data(self, request):
    file = request.FILES['file']
    retrieve_file = Fileinfo.objects.filter(file_name=file).first()
    logger.info("Selected file is " + str(file))
    fileName = request.FILES[config.FILE].name
    logger.info("filename is " + fileName)
    header = request.data.get(config.HEADER)
    logger.info("Status of selected Header of file is " + str(header))
    metadata = request.data.get(config.METADATA)
    logger.info("Status of selected Metadata of fie is " + str(metadata))
    if(fileName.endswith('.h5') or fileName.endswith('.H5')):
        hf = h5py.File(file,'r')
        logger.info(str(hf) + "File reads")
        name_of_file = fileName
        name_of_file = os.path.basename(name_of_file)
        logger.info("selected file name is " +name_of_file)
        if config.SAVEURL in request.get_full_path():
            completeName = os.path.join(config.TMP, name_of_file)
        elif config.MODIFYURL in request.get_full_path():
            completeName = os.path.join(config.TMP1, name_of_file)   
        logger.info("Selected file path for storage is " +completeName)
        logger.info("complete path is " +completeName)
        f1 = h5py.File(completeName, 'w')
        with h5py.File(file, "r") as f:
            for ds in f.keys():
                f.copy(ds, f1)
        f1.close()
        file_size = os.path.getsize(completeName)
        logger.info("file size of selected file is " + str(file_size))
        uploaded_by = request.data.get('uploaded_by')
        if config.SAVEURL in request.get_full_path():
            dict1 = {config.FILENAME:name_of_file, config.FILEPATH:config.TMP, config.FILESIZE:file_size, config.UPLOADEDBY: uploaded_by, config.AGENCYNAME:'Privacyuser', config.UPLOADEDBY:uploaded_by, config.UPDATEDDATE:datetime.now(), config.DESCRIPTION:'Inserting file info'}
        elif config.MODIFYURL in request.get_full_path():
            dict1 = {config.FILENAME:name_of_file, config.FILEPATH:config.TMP1, config.FILESIZE:file_size, config.UPLOADEDBY: uploaded_by, config.AGENCYNAME:'Privacyuserupdations', config.UPLOADEDBY:uploaded_by, config.UPDATEDDATE:datetime.now(), config.DESCRIPTION:'Inserting file info checking'}
        logger.info("Dictionary of file to be inserted is " + str(dict1))
    return dict1

def onlydataset(self, request):
    header = request.data.get(config.HEADER)
    metadata = request.data.get(config.METADATA)
    if header == config.FALSE and metadata == config.FALSE:
        filedict = {"keys" : "Read file", "value" : "Successfully"}
        return Response(filedict)

def headerdataset(self, request):
    header = request.data.get(config.HEADER)
    file = request.FILES['file']
    fileName = request.FILES[config.FILE].name
    name_of_file = fileName
    name_of_file = os.path.basename(name_of_file)
    try:
        hf = h5py.File(file,'r')
        if config.MODIFYURL in request.get_full_path():
            file = request.FILES['file']
            retrieve_file = Fileinfo.objects.filter(file_name=file).first()
        headerdict1 = {}
        for headerattr in hf.attrs:
            try:
                if(headerattr != None and headerattr != 'None' and headerattr != ''):
                    headerdict1.__setitem__(headerattr, str(hf.attrs[headerattr]))                
                    logger.info("Dictionary of selected file header is " + str(headerdict1))
            except ValueError as errMessage:
                return Response({'Message': str(errMessage)}) 
        
        if config.SAVEURL in request.get_full_path():
            headerdict = {config.PRODUCTLINE: config.S102, config.HEADERNAME: name_of_file, config.HEADERVAL:json.dumps(headerdict1), config.DESCRIPTION: 'Header info'}
            serializer = S100HeaderInfoSerializer(data=headerdict)
        elif config.MODIFYURL in request.get_full_path():
            headerdict = {config.PRODUCTLINE: config.S102, config.HEADERNAME: name_of_file, config.HEADERVAL:json.dumps(headerdict1), config.DESCRIPTION: 'Header info updates'}
            header_file = Headerinfo.objects.filter(id=retrieve_file.id).first()
            serializer = S100HeaderModifySerializer(header_file, data=headerdict)
        elif config.FILEURL in request.get_full_path():
            return HttpResponse(json.dumps(headerdict1))

        logger.info("Header of selected file is " +str(headerdict))
        
        object1=''
        if serializer.is_valid(raise_exception=True):
            object1 = serializer.save() 
        if config.SAVEURL in request.get_full_path():
            queryset = Headerinfo.objects.all()
            serializer_class = S100HeaderInfoSerializer(queryset, many=True)
            return HttpResponse(json.dumps(serializer_class.data))
        elif config.MODIFYURL in request.get_full_path():
            return HttpResponse(json.dumps(serializer.data))
        
    except ValueError as errMessage:
        logger.error(str(errMessage))
        return Response({'Message': str(errMessage)}) 
        
def metadatadataset(self, request):
    file = request.FILES['file']
    fileName = request.FILES[config.FILE].name
    hf = h5py.File(file,'r')
    if config.MODIFYURL in request.get_full_path():
        file = request.FILES['file']
        retrieve_file = Fileinfo.objects.filter(file_name=file).first()
    metadatadict = {}
    lastIndex1 = fileName.rindex('.')     
    usName = fileName[:lastIndex1]
    
    for firstattr10 in hf.attrs:
        try:
            if(firstattr10 != None and firstattr10 != 'None' and firstattr10 != ''):
                logger.info('Key = '+firstattr10+' value = '+str(hf.attrs[firstattr10])+'\n')    
                metadatadict.__setitem__(firstattr10, str(hf.attrs[firstattr10]))
                logger.info("Dictionary of selected file metadata is " + str(metadatadict))
        except ValueError as errMessage:
            return Response({'Message': str(errMessage)}) 
    for i in range(0, len(hf.keys())):
        firstKey = list(hf.keys())[i]
        data = list(hf[firstKey])

        logger.info('\n First Key = '+str(firstKey) +'\n')
        for firstattr in hf[firstKey].attrs:
            try:
                if(firstattr != None and firstattr != 'None' and firstattr != ''):
                    logger.info('Key = '+firstattr+' value = '+str(hf[firstKey].attrs[firstattr])+'\n')    
                    metadatadict.__setitem__(firstattr, str(hf[firstKey].attrs[firstattr]))
                    logger.info("Dictionary of selected file metadata is " + str(metadatadict))
            except ValueError as errMessage:
                return Response({'Message': str(errMessage)})    
        secondKey = list(hf[firstKey])[i]
        data_sec = list(hf[firstKey][secondKey])
        logger.info(str(secondKey)+'\n')
        for secondattr in hf[firstKey][secondKey].attrs:
            if(secondattr != None and secondattr != 'None' and secondattr != ''):
                logger.info('Key = '+secondattr+' value = '+str(hf[firstKey][secondKey].attrs[secondattr])+'\n')    
                metadatadict.__setitem__(secondattr, str(hf[firstKey][secondKey].attrs[secondattr]))
        thirdKey = list(hf[firstKey][secondKey])[i]
        data_third = list(hf[firstKey][secondKey][thirdKey])
        logger.info(str(thirdKey)+'\n')
        for thirdattr in hf[firstKey][secondKey][thirdKey].attrs:
            if(thirdattr != None and thirdattr != 'None' and thirdattr != ''):
                logger.info('Key = '+thirdattr+' value = '+str(hf[firstKey][secondKey][thirdKey].attrs[thirdattr])+'\n')
                metadatadict.__setitem__(thirdattr, str(hf[firstKey][secondKey][thirdKey].attrs[thirdattr]))

        fourKey = list(hf[firstKey][secondKey][thirdKey])[i]
        logger.info(str(fourKey)+'\n')
        data_four = list(hf[firstKey][secondKey][thirdKey][fourKey])
        
        for fourattr in hf[firstKey][secondKey][thirdKey][fourKey].attrs:
            if(fourattr != None and fourattr != 'None' and fourattr != ''):
                logger.info('Key = '+fourattr+' value = '+str(hf[firstKey][secondKey][thirdKey][fourKey].attrs[fourattr]) +'\n')
                metadatadict.__setitem__(fourattr, str(hf[firstKey][secondKey][thirdKey][fourKey].attrs[fourattr]))

        firstKey1 = list(hf.keys())[i]
        logger.info('\n Second Key = '+str(firstKey1) +'\n')
        for firstattr1 in hf[firstKey1].attrs:
            if(firstattr1 != None and firstattr1 != 'None' and firstattr1 != ''):
                logger.info('Key = '+firstattr1+' value = '+str(hf[firstKey1].attrs[firstattr1])+'\n')    
                metadatadict.__setitem__(firstattr1, str(hf[firstKey1].attrs[firstattr1]))
        secondKey1 = list(hf[firstKey1])[i]
        logger.info(str(secondKey1)+'\n')
        for secondattr1 in hf[firstKey1][secondKey1].attrs:
            if(secondattr1 != None and secondattr1 != 'None' and secondattr1 != ''):
                logger.info('Key = '+secondattr1+' value = '+str(hf[firstKey1][secondKey1].attrs[secondattr1])+'\n')    
                metadatadict.__setitem__(secondattr1, str(hf[firstKey1][secondKey1].attrs[secondattr1]))
        
        firstKey2 = list(hf.keys())[i]
        logger.info('\n Third Key = '+str(firstKey2) +'\n')
        for firstattr2 in hf[firstKey2].attrs:
            if(firstattr2 != None and firstattr2 != 'None' and firstattr2 != ''):
                logger.info('Key = '+firstattr2+' value = '+str(hf[firstKey2].attrs[firstattr2])+'\n')    
                metadatadict.__setitem__(firstattr2, str(hf[firstKey2].attrs[firstattr2]))
        secondKey2 = list(hf[firstKey2])[i]
        logger.info(str(secondKey2)+'\n')
        for secondattr2 in hf[firstKey2][secondKey2].attrs:
            if(secondattr2 != None and secondattr2 != 'None' and secondattr2 != ''):
                logger.info('Key = '+secondattr2+' value = '+str(hf[firstKey2][secondKey2].attrs[secondattr2])+'\n')    
                metadatadict.__setitem__(secondattr2, str(hf[firstKey2][secondKey2].attrs[secondattr2]))
        return metadatadict
        