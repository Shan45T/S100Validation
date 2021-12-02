from file_reading.utils.cacheutility import CacheUtillity
import h5py
import binascii
import sys
import logging
from django.shortcuts import render
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import numpy as np
import xml.etree.ElementTree as ET
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import json
from file_reading.serializer.S100UPLOADFILE import *
from django.http import HttpResponse
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
basePath = os.path.join(BASE_DIR, "resources")
sys.path.append(basePath)
import config

from file_reading.utils import utils
logger = logging.getLogger(__name__)#
from django.db.models import Q

def home(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'Login.html')

def signup(request):
    return render(request, 'signup.html')

def changepassword(request):
    return render(request, 'changepassword.html')        

class S100FlieReadingViewset(viewsets.ModelViewSet): 

    serializer_class = S100FileSerializer

    def get_queryset(self):
        return
    def create(self, request):
        try:
            file = request.FILES['file']
            requested_user = request.user
            role = RoleInfo.objects.get(role_name = 'Admin')
            logger.info("Admin role id is " + str(role.id))
            userinfo = UserInfo.objects.filter(Q(user_name = requested_user) & Q(role_id = role.id))
            logger.info("Selected file is " + str(file))
            print(len(userinfo))
            #if (len(userinfo) != 0):
            serializer_class = S100FileSerializer(data=request.data)
            if 'file' not in request.FILES or not serializer_class.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                file = request.FILES['file']
                logger.info("Selected file is " + str(file)) 
                fileName = request.FILES['file'].name
                logger.info("filename is " + fileName)
                header = request.data.get(config.HEADER)
                logger.info("Status of selected Header of file is " + str(header))
                metadata = request.data.get(config.METADATA)
                logger.info("Status of selected Metadata of fie is " + str(metadata))
                try:
                    if(fileName.endswith('.h5') or fileName.endswith('.H5')):
                        length = len(fileName)
                        lastIndex=0
                        hf = h5py.File(file,'r')
                        logger.info(str(hf) + "File reads")
                        if(fileName.__contains__('_')):
                            try:
                                lastIndex = fileName.rindex('_')        
                                if(length >= lastIndex+4):
                                    subFileName = fileName[:lastIndex]
                                    logger.info(" subFileName : "+subFileName)
                                    hf = h5py.File(subFileName+'_%d.h5','r', driver='family', memb_size=0)
                            except ValueError as errMessage:
                                logger.error(str(errMessage))
                                return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)
                        else:
                            logging.info('file reading other case')  
                            hf = h5py.File(file,'r')
                        firstKey = list(hf.keys())[0]
                        logger.info("firstkey of file is  "+ str(firstKey))
                        secondKey = list(hf[firstKey])[0]
                        logger.info("secondkey of file is  "+ str(secondKey))
                        thirdKey = list(hf[firstKey][secondKey])[0]
                        logger.info("thirdkey of file is  "+ str(thirdKey))
                        fourKey = list(hf[firstKey][secondKey][thirdKey])[0]
                        logger.info("Fourthkey of file is " + str(fourKey))
                        data_four = list(hf[firstKey][secondKey][thirdKey][fourKey])

                        lastIndex1 = fileName.rindex('.')        
                        usName = fileName[:lastIndex1]
                        if header == 'false' and metadata == 'false':
                            filedict = {"keys" : "Read file", "value" : "Successfully"}
                            return HttpResponse("Read file", status=status.HTTP_201_CREATED)
                            
                        elif header == 'true':
                            hf = h5py.File(file,'r')
                            headerdict = {}
                            for headerattr in hf.attrs:
                                try:
                                    if(headerattr != None and headerattr != 'None' and headerattr != ''):
                                        headerdict.__setitem__(headerattr, str(hf.attrs[headerattr]))                
                                        logger.info("Dictionary of selected file header is " + str(headerdict))
                                except ValueError as errMessage:
                                    return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)
                            logger.info("Header of selected file is " +str(headerdict))
                            return HttpResponse(json.dumps(headerdict), status=status.HTTP_201_CREATED)

                        elif metadata == 'true':
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
                                        logger.info("Dictionary of selected file metadata is " + str(metadatadict))
                                return HttpResponse(metadatadict, status=status.HTTP_201_CREATED)
                    else:
                        raise Exception("Pass h5 file only") 
                    return Response(("Read h5 file successfully"),status=status.HTTP_201_CREATED)
                except ValueError as errMessage:
                    return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)        
            # else:
            #     return HttpResponse("Invalid user")                        
        except ValueError as errMessage:
            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)