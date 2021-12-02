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
import json
from rest_framework import views, viewsets
import re
from django.http import HttpResponse,JsonResponse
from django.db import models
from file_reading.serializer.S100UPLOADFILE import *
from file_reading.utils import utils
logger = logging.getLogger(__name__)

class S100RoleViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        return
    def list(self, request):
        queryset = RoleInfo.objects.values('role_name', 'id')
        serializer_class = S100RoleSerializerIdName(queryset,many=True)
        return HttpResponse(json.dumps(serializer_class.data))