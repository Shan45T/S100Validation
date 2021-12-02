
import logging
from rest_framework.response import Response
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
import config
from rest_framework import views, viewsets
import re
from django.db import models
from file_reading.serializer.S100UPLOADFILE import *
from file_reading.utils import utils

from file_reading.views import S100SIGNUPFILE
from file_reading.utils import utils
from zipfile import ZipFile
from django.utils.encoding import smart_str

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
basePath = os.path.join(BASE_DIR, "resources")
sys.path.append(basePath)


class S100LOGFILE(viewsets.ModelViewSet):
    def get_queryset(self):
        return

    def list(self, request):

        try:
            logfile = open('tmp/log.txt', 'w')
            file1 = open("Display.log", 'r')
            logfile.write(file1.read())
            logfile.close()

            zipObj = ZipFile('tmp/sample.zip', 'w')        
            zipObj.write('log.txt')          
            zipObj.close()

            zipFileName = 'tmp/log.txt'
            file_path = os.path.join(settings.BASE_DIR, zipFileName)
            
            if os.path.exists(file_path):                
                with open(file_path, 'rb') as fh:                  
                    response = HttpResponse(fh.read(), content_type='application/txt')            
                    response['Content-Disposition'] = 'attachment; filename = %s' % smart_str(zipFileName)
                    response['X-Sendfile'] = smart_str(zipFileName)
                    #return Response({'Message':'No log Data...1'},status=status.HTTP_200_OK)
                    return response
            else:
                return Response({'Message':'No log Data'},status=status.HTTP_404_NOT_FOUND)
        except:
            logger.error(sys.exc_info())
            return HttpResponse(json.dumps({'Message':sys.exc_info()}), status=400)
        finally:
            logger.info('exiting from log reading file')
            
