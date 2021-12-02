import xml.etree.ElementTree as ET
from h5py._hl.files import File
import config
from rest_framework.response import Response
from rest_framework import views, viewsets
from django.http import HttpResponse
import os
import json
import h5py
import logging
from file_reading.serializer.S100UPLOADFILE import *
from django.db.models import Q
from rest_framework import status

logger = logging.getLogger(__name__)

class S100FeatureViewset(viewsets.ModelViewSet):
    def create(self, request):
        try:
            requested_user = request.user
            logger.info("Requested user is " +str(requested_user))
            role = RoleInfo.objects.get(role_name = 'Admin')
            logger.info("Admin role id is " + str(role.id))
            userinfo = UserInfo.objects.filter(Q(user_name = requested_user) & Q(role_id = role.id) )
            if (len(userinfo) != 0):
                file = request.FILES[config.FILE]
                logger.info("Requested file is " + str(file))
                fileName = request.FILES[config.FILE].name
                if(fileName.endswith('.xml') or fileName.endswith('.XML')):
                    tree = ET.parse(file)
                    root = tree.getroot()
                    vals = []
                    for item in root:
                        logger.info("Element tree of file is " +str(item))
                        vals.append(item)
                    with open('C:\\Users\\mndv8023\\Documents\\Manasa\\2021\\November\\check\\S-102FC_2.0.1.xml', 'w') as f:                
                        f.write(str(vals))
                    
                    f.close()
                    return Response("Feature catalogue file")
            else:
                return HttpResponse("Invalid user")      
        except ValueError as errMessage:
            logger.error(str(errMessage))
            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND) 