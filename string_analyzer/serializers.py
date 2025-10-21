from rest_framework import serializers
from .models import StringAnalysis

class StringAnalysisSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = StringAnalysis
        fields = '__all__'
        created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
