import numpy as np
import h5py
import binascii
import sys
import logging
from rest_framework import views, viewsets
import logging
from rest_framework.response import Response
from itertools import count
from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
from shapely import geometry
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point, LineString, MultiLineString, box, MultiPolygon
from matplotlib import pyplot
import os
from file_reading.views.S100READINGFILE import  *
import psycopg2
from datetime import datetime, timezone
from django.conf import settings
from file_reading.views import S100READINGFILE
import ast
from file_reading.models import *
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
basePath = os.path.join(BASE_DIR, "resources")
sys.path.append(basePath)
import config
from rest_framework import views, viewsets
import re
from django.http import HttpResponse,JsonResponse
from django.db import models
from file_reading.serializer.S100UPLOADFILE import *
from file_reading.utils import utils
logger = logging.getLogger(__name__)
import traceback

class S100SaveViewset(viewsets.ModelViewSet): 
    def get_queryset(self):
        return
    def create(self, request):
        try:
            file = request.FILES[config.FILE]            
            requested_user = request.user
            role = RoleInfo.objects.get(role_name = 'Admin')
            logger.info("Admin role id is " + str(role.id))
            userinfo = UserInfo.objects.filter(Q(user_name = requested_user) & Q(role_id = role.id) )
            logger.info("Selected file is " + str(file))
            if (len(userinfo) != 0):
                fileName = request.FILES[config.FILE].name                        
                logger.info("filename is " + fileName)
                header = request.data.get(config.HEADER)
                logger.info("Status of selected Header of file is " + str(header))
                metadata = request.data.get(config.METADATA)
                logger.info("Status of selected Metadata of fie is " + str(metadata))
                try:
                    if(fileName.endswith('.h5') or fileName.endswith('.H5')):
                        hf = h5py.File(file,'r')
                        logger.info(str(hf) + "File reads")
                        name_of_file = fileName
                        name_of_file = os.path.basename(name_of_file)
                        logger.info("selected file name is " +name_of_file)
                        completeName = os.path.join(config.TMP, name_of_file)
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
                        dict1 = {config.FILENAME:name_of_file, config.FILEPATH:config.TMP, config.FILESIZE:file_size, config.UPLOADEDBY: uploaded_by, config.AGENCYNAME:'Privacyuser', config.UPLOADEDBY:uploaded_by, config.UPDATEDDATE:datetime.now(), config.DESCRIPTION:'Inserting file info'}
                        logger.info("Dictionary of file to be inserted is " + str(dict1))
                        serializer = S100FileReadingSerializer(data=dict1)
                        object1=''
                        if serializer.is_valid(raise_exception=True):
                            object1 = serializer.save()                
                        queryset = Fileinfo.objects.all()
                        serializer_class = S100FileReadingSerializer(queryset, many=True)
                        if header == config.FALSE and metadata == config.FALSE:
                            filedict = {"keys" : "Read file", "value" : "Successfully"}                        
                            return HttpResponse("File Saved Successfully", status=status.HTTP_201_CREATED)
                        elif header == config.TRUE:                        
                            try:
                                hf = h5py.File(file,'r')
                                headerdict1 = {}                            
                                for headerattr in hf.attrs:
                                    try:
                                        if(headerattr != None and headerattr != 'None' and headerattr != ''):
                                            headerdict1.__setitem__(headerattr, str(hf.attrs[headerattr]))                
                                            logger.info("Dictionary of selected file header is " + str(headerdict1))
                                    except ValueError as errMessage:
                                        return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)
                                    
                                headerdict = {config.PRODUCTLINE: config.S102, config.HEADERNAME: name_of_file, config.HEADERVAL:json.dumps(headerdict1), config.DESCRIPTION: 'Header info'}
                                logger.info("Header of selected file is " +str(headerdict))
                                serializer = S100HeaderInfoSerializer(data=headerdict)
                                object1=''
                                if serializer.is_valid(raise_exception=True):
                                    object1 = serializer.save()                    
                                queryset = Headerinfo.objects.all()
                                serializer_class = S100HeaderInfoSerializer(queryset, many=True)                                
                                return HttpResponse(json.dumps(headerdict), status=status.HTTP_201_CREATED)
                            except ValueError as errMessage:
                                logger.error(str(errMessage))
                                return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND) 
                        elif metadata == config.TRUE:                            
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
                                    return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)    
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
                                        return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)    
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
                                
                                
                                metadatadict1 = {config.PRODUCTLINE: config.S102, config.CREATEDBY: uploaded_by, config.CREATEDDATE :datetime.now(), config.DELETEDBY: uploaded_by, config.DELETEDDATE: datetime.now(), config.METADATA: json.dumps(metadatadict)}
                                logger.info("Metadata of selected file is "+ str(metadatadict1))
                                serializer = S100MetadataInfoSerializer(data=metadatadict1)
                                object1=''
                                if serializer.is_valid(raise_exception=True):
                                    object1 = serializer.save()
                                queryset = Metadatainfo.objects.all()
                                serializer_class = S100MetadataInfoSerializer(queryset, many=True)
                                return HttpResponse((metadatadict1), status=status.HTTP_201_CREATED)
                        else:
                            logger.info("Not header and metadata")
                    else:
                        raise Exception("Pass h5 file only")                                        
                except ValueError as errMessage:
                    return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)
            else:
                return HttpResponse("Invalid user")
        except ValueError as errMessage:
            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)