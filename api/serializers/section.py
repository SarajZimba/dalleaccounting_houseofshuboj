# serializers.py
from rest_framework import serializers

class SectionSerializer(serializers.Serializer):
    section = serializers.CharField()