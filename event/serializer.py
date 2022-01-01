import json
from django.contrib.auth import authenticate
from rest_framework import serializers
# pip install Django django-rest-framework
from .models import Event as event
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    # user = serializers.SerializerMethodField()
    # event_id = serializers.SerializerMethodField(method_name='get_event_id')

    class Meta:
        model = event
        # read_only_fields = ('user')
        fields = '__all__'
        read_only_field = ['user', 'description', 'start']


    # def get_user(self, obj):
    #     pass
    #


