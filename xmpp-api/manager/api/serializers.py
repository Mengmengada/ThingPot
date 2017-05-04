from models import Result, ExecutedTest
from rest_framework import serializers


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutedTest
        fields = '__all__'

