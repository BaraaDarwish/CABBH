from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework import serializers
from CAC.models import DiabetesPrediction

class DiabetesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiabetesPrediction
        fields = ("__all__" )

