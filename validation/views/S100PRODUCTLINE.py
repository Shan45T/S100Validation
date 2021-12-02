from rest_framework import views, viewsets
import logging
from rest_framework.response import Response
import logging
import os
import psycopg2
from datetime import datetime, timezone
import ast
import json
from file_reading.models import *
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
basePath = os.path.join(BASE_DIR, "resources")
sys.path.append(basePath)
import config
from rest_framework import views, viewsets
import re
from django.db import models
from validation.serializer.S100VALIDATIONFILE import *
from rest_framework import status

logger = logging.getLogger(__name__)


class S100ProductlineViewset(viewsets.ViewSet):
    def get_queryset(self):
        return
    def list(self, request):
        try:
            queryset = ProductLineInfo.objects.distinct('name')
            logger.info(queryset)
            product_spc = ProductLineInfo.objects.filter(name='S-102').distinct('name')
            serializer_class = S100ProductLineSerializer(product_spc,many=True)
            logger.info("Data of productline is " +str(serializer_class.data))
            return Response(json.dumps(serializer_class.data), status=status.HTTP_200_OK)
        except ValueError as errMessage:
            logger.error(str(errMessage))
            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND) 
