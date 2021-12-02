from rest_framework import serializers
from django.contrib.auth.models import *
from file_reading.models import *

class S100FileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)
    
class S100FileReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fileinfo
        fields = ['file_name', 'file_path', 'file_size', 'uploaded_by', 'agency_name', 'updated_by', 'updated_date', 'description']
   
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100FileReadingSerializer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']

class S100HeaderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headerinfo
        fields = ['product_line', 'header_name', 'header_value', 'description']

class S100MetadataInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadatainfo
        fields = ['product_line', 'created_by', 'created_date', 'deleted_by', 'deleted_date', 'metadata']

class S100ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLineInfo
        fields = ['name', 'version', 'date', 'number', 'updated_by', 'updated_date']

class S100RoleSerializerIdName(serializers.ModelSerializer):
    class Meta:
        model = RoleInfo
        fields = ['role_name', 'id']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100RoleSerializerIdName, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class S100RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleInfo
        fields = ['role_name', 'id', 'restricted', 'active', 'description']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100RoleSerializer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class S100Userserializer(serializers.ModelSerializer):
    

    class Meta:
        model = UserInfo
        fields = ['user_id', 'user_name', 'first_name', 'last_name', 'email', 'phoneno', 'description', 'role_id']    

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100Userserializer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class S100AgencySerializerName(serializers.ModelSerializer):
    class Meta:
        model = AgencyInfo
        fields = ['agency_name']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100AgencySerializerName, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class S100AgencySerializer(serializers.ModelSerializer):
    
    agency_id = S100Userserializer()

    class Meta:
        model = AgencyInfo
        fields = ['agency_name', 'address', 'phoneno', 'contact_person', 'email', 'description', 'agency_id']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100AgencySerializer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        if 'agency_id' in validated_data:
            user_data = validated_data.pop('agency_id')
        else:
            print("agency_id not in validated_data")
        Userdata = UserInfo.objects.create(**user_data)
        agencydata = AgencyInfo.objects.create(agency_id = Userdata, **validated_data)
        return agencydata        

class S100UserSerializer(serializers.ModelSerializer):
    role_id = S100RoleSerializer()

    class Meta:
        model = UserInfo
        fields = ['user_id', 'user_name', 'first_name', 'last_name', 'email', 'phoneno', 'description']    

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100UserSerializer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        if 'role_id' in validated_data:
            role_data = validated_data.pop('role_id')
        else:
            print("role_id not in validated_data")
        Roledata = RoleInfo.objects.create(**role_data)
        userdata1 = UserInfo.objects.create(role_id = Roledata, **validated_data)
        return userdata1
