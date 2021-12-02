from rest_framework import serializers
from django.contrib.auth.models import *
from file_reading.models import *


class S100UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ['user_id', 'user_name', 'first_name', 'last_name', 'email', 'phoneno', 'description']    


class S100PasswordSeriallizer(serializers.ModelSerializer):
    password_id = S100UserSerializer()

    class Meta:
        model = PasswordInfo
        fields = ['password_id','password', 'password_expiry', 'password_alg']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(S100PasswordSeriallizer, self).__init__(*args, **kwargs)
        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    def update(self, instance, validated_data):
        if 'password_id' in validated_data:
            nested_serializer = self.fields['password_id']
            nested_instance = instance.password_id
            if 'password_id' in validated_data:
                nested_data = validated_data.pop('password_id')
            return super(S100PasswordSeriallizer, self).update(instance, validated_data)
        else:
            return super(S100PasswordSeriallizer, self).update(instance, validated_data)