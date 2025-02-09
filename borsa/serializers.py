from rest_framework import serializers
from .models import AcademicYear, IseeRange, Request

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class IseeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IseeRange
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'