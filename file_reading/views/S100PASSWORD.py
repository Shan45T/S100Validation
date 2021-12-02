

from rest_framework import views, viewsets
import logging
from rest_framework.response import Response
import logging
import os
from django.http import HttpResponse
import psycopg2
from datetime import datetime, timezone
import ast
from file_reading.models import *
import sys
import json
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
from file_reading.serializer.S100PASSWORDFILE import *

logger = logging.getLogger(__name__)

class S100PasswordViewset(viewsets.ViewSet):
    def get_queryset(self):
        return
    def create(self, request):
        try:           
            requested_user = request.user
            queryset = UserInfo.objects.filter(user_id = requested_user.id)
            data1 = S100UserSerializer(queryset,many=True)
            data2 = UserInfo.objects.get(user_id = requested_user.id)
            
            if(request.data.get('new_password') == request.data.get('confirm_password')):
                retrieve_file = PasswordInfo.objects.filter(password_id=requested_user.id).first()
                fields = ['password_id', 'password', 'password_expiry', 'password_aig']
                dict2 = {'user_id':(data1.data)[0]["user_id"], 'user_name': (data1.data)[0]["user_name"], 'first_name': (data1.data)[0]["first_name"], 'last_name': (data1.data)[0]["last_name"], 'email': (data1.data)[0]["email"], 'phoneno': (data1.data)[0]["phoneno"], 'description': (data1.data)[0]["description"]}
                dict1 = {'password_id':dict2, 'password':request.data.get('new_password'), 'password_expiry': '2021-12-02', 'password_aig': 'password'}
                serializer = S100PasswordSeriallizer(retrieve_file, data = dict1,partial = True)
                object1=''
                if serializer.is_valid(raise_exception=True):
                    object1 = serializer.save() 
            else:
                return HttpResponse("The new passwords does not match ")

        except ValueError as errMessage:
            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)
        return HttpResponse("passwordfile")