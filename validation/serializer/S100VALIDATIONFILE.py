from rest_framework import serializers

from django.contrib.auth.models import *
from validation.models import *
import re
import logging

logger = logging.getLogger(__name__)
class S100FileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)
    
    
class S100ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLineInfo
        fields = ['name', 'version', 'date', 'number', 'updated_by', 'updated_date']
        
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100ProductLineSerializer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    def validate_name(self, data):
        if(data != None and data != '' and data != 'None'):
            nameregex = re.match("^S-.*[0-9]{3}$", data)
            if (nameregex):
                logger.info('valid productspecification name')
            else:
                raise serializers.ValidationError("name field not in the form of S-111")
        else:
            logger.info("name is empty")
        return data 
     
    def validate_version(self, data):
        if(data != None and data != '' and data != 'None'):
            versionregex = re.match("([0-9]{6})", data)
            if (versionregex):
                logger.info('valid productspecification version')
            else:
                raise serializers.ValidationError("version should be in the form of 000000")
        else:
            logger.info("version is empty")
        return data
    def validate_date(self, data):
        if(data != None and data != '' and data != 'None'):
            dateregex = re.match("(^\d{4}\-)(\d{2}\-)(\d{2})$", str(data))
            if (dateregex):
                logger.info("valid productspecification date")
            else:
                raise serializers.ValidationError("not in the form of date")
        else:
            logger.info("date is blank")
        return data
        
    def validate_number(self, data):
        if(data != None and data != '' and data != 'None'):
            numberregex = re.match("([0-9]{3})", str(data))
            if (numberregex):
                logger.info("valid productspecification number")
            else:
                raise serializers.ValidationError("number should be integer type only")
        else:
            logger.info("number is blank")
        return data

class S100RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleInfo
        fields = ['role_name', 'restricted', 'active', 'description']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100RoleSerializer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    def validate_role_name(self, data):
        if(data != None and data != '' and data != 'None'):
            rolenameregex = re.match("^S-.*[0-9]{3}$", data)
            if (rolenameregex):
                logger.info('valid productspecification name')
            else:
                raise serializers.ValidationError("name field not in the form of S-111")
        else:
            logger.info("rolename is empty")
        return data 
    
class S100AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyInfo
        fields = ['agency_name', 'address', 'phoneno', 'contact_person', 'email', 'description']