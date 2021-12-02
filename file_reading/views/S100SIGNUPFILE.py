from django.db.models import query
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

from file_reading.views import S100READINGFILE
import ast
from file_reading.models import *

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
basePath = os.path.join(BASE_DIR, "resources")
sys.path.append(basePath)
import config
from rest_framework import views, viewsets
import re
from django.db import models
from file_reading.serializer.S100UPLOADFILE import *

logger = logging.getLogger(__name__)


class S100SignupViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        return
    def create(self, request):
        fields = ['agency_id','user_name', 'first_name', 'last_name', 'email', 'phoneno', 'description','agency_name', 'address', 'contact_person']
        dict2 = {'user_name': request.data.get('user_name'), 'first_name': request.data.get('first_name'), 'last_name': request.data.get('last_name'), 'email':request.data.get('email'), 'phoneno':int(request.data.get('phoneno')), 'description': (request.data.get('description').rstrip()), 'role_id' : '2'}
        dict1 = {'agency_id': dict2, 'agency_name':request.data.get('agency_name'), 'address': request.data.get('address'), 'phoneno': int(request.data.get('phoneno')), 'contact_person': request.data.get('contact_person'), 'email':request.data.get('email'), 'description': (request.data.get('description').rstrip())}
        serializer_class = S100AgencySerializer(data = dict1)
        object1=''
        try:
            if serializer_class.is_valid(raise_exception=True):                
                object1 = serializer_class.save()              
            queryset = AgencyInfo.objects.all()
            logger.info(queryset)
            serializer_class = S100AgencySerializer(queryset, many=True)            
            return HttpResponse(json.dumps(serializer_class.data), status=status.HTTP_201_CREATED)
        except ValueError as errMessage:            
            logger.error(str(errMessage))
            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)