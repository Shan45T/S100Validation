from rest_framework import serializers
from django.contrib.auth.models import *
from file_reading.models import *

class S100FileModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Fileinfo
        fields = ['file_name', 'file_path', 'file_size', 'uploaded_by', 'agency_name', 'updated_by', 'updated_date', 'description']
   
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100FileModifySerializer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
