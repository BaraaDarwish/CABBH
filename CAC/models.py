from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django import forms
def check_value_Pregnancies(value):
    if value <0 or value >63 :
        raise forms.ValidationError("Pregnancies value out of interval")
    else:
        return value

def check_value_Glucose(value):
    if value <0 or value >511 :
        raise forms.ValidationError("Glucose value out of interval")

def check_value_BloodPressure(value):
    if value <0 or value >255 :
        raise forms.ValidationError("Blood Pressure value out of interval")

def check_value_SkinThickness(value):
    if value <0 or value >255 :
        raise forms.ValidationError("Skin Thickness value out of interval")
    else:
        return value


def check_value_Insulin(value):
    if value <0 or value >1023 :
        raise forms.ValidationError("Insulin value out of interval")

class DiabetesPrediction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE , blank = True)
    name = models.CharField(max_length=50,default='Untitled')
    Pregnancies = models.IntegerField( validators=[])
    Glucose = models.IntegerField()	
    BloodPressure = models.IntegerField()
    SkinThickness = models.IntegerField()	
    Insulin = models.IntegerField()
    BMI =  models.FloatField()	
    DiabetesPedigreeFunction = models.FloatField()	
    Age = models.IntegerField()	
    result = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

