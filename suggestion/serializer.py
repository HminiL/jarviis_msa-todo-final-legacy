from rest_framework import serializers
from suggestion.models import SuggestionEvent


class SuggsetionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionEvent
        fields = '__all__'