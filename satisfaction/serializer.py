from django.contrib.auth import authenticate
from rest_framework import serializers
# pip install Django django-rest-framework
from .models import Satisfaction as satisfaction


class SatisfactionSerializer(serializers.ModelSerializer):

    # user = serializers.SerializerMethodField()

    class Meta:
        model = satisfaction
        # read_only_fields = ('user')
        fields = '__all__'
        read_only_field = ['_id']

    # def get_user(self, object):
    #     pass
    #
    # def create(self, validated_data):
    #     return satisfaction.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     satisfaction.objects.filter(pk=instance.id).update(**validated_data)
    #
    # def remove(self):
    #     pass

