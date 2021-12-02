from rest_framework import views, viewsets
from rest_framework.response import Response
import logging
import psycopg2
from datetime import datetime, timezone
from django.conf import settings
from file_reading.models import *
import os
import sys
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
basePath = os.path.join(BASE_DIR, "resources")
sys.path.append(basePath)
import config
from rest_framework import views, viewsets
import re
import json
from django.http import HttpResponse,JsonResponse
from django.db import models
from file_reading.serializer.S100UPLOADFILE import *
from file_reading.utils import utils
logger = logging.getLogger(__name__)
from rest_framework import status

class S100AgencyViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        return
    def list(self, request):
        try:
            queryset = AgencyInfo.objects.values('agency_name').distinct('agency_name')
            serializer_class = S100AgencySerializerName(queryset,many=True)
            return HttpResponse(json.dumps(serializer_class.data))
        except ValueError as errMessage:
            logger.error(str(errMessage))
            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND) 