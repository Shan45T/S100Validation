
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
from validation.serializer.S100VALIDATIONFILE import *

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
basePath = os.path.join(BASE_DIR, "resources")
sys.path.append(basePath)
import config


logger = logging.getLogger(__name__)#

def home(request):
    return render(request, 'index.html')

class S100FileValidationViewset(viewsets.ModelViewSet): 

    serializer_class = S100FileSerializer

    def get_queryset(self):
        return
    def create(self, request):
        serializer_class = S100FileSerializer(data=request.data)
        if 'file' not in request.FILES or not serializer_class.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            file = request.FILES['file']
            fileName = request.FILES['file'].name            
            if(fileName.endswith('.h5') or fileName.endswith('.H5')):
                length = len(fileName)
                lastIndex=0
                if(fileName.__contains__('_')):                    
                    data = request.FILES['file'] # or self.files['image'] in your form
                    path = default_storage.save(fileName, ContentFile(data.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                    lastIndex = fileName.rindex('_')        
                    if(length >= lastIndex+4):
                        subFileName = fileName[:lastIndex]                        
                        hf = h5py.File(subFileName+'_%d.h5','r', driver='family', memb_size=0)
                        default_storage.delete(tmp_file)
                else:
                    logging.info('file reading other case')            
                    hf = h5py.File(file,'r')
            else:
                raise Exception("Please pass the H5 input file")   
            return Response(("validation h5 file successfully"),status=status.HTTP_201_CREATED)
