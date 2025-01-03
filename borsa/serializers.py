from rest_framework import serializers
from .models import AcademicYear, IseeRange, Scholarship,Request

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class IseeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IseeRange
        fields = '__all__'

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'