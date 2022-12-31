from rest_framework import serializers
from .models import Playstore

class PlayStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playstore
        fields = '__all__'
    