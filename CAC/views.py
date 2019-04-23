from django.shortcuts import render
from django.http import HttpResponse
from .forms import DiabetesPredictionForm
from CAC import CAClassifier
from CAC import data_converter
from CAC.models import DiabetesPrediction
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView ,DeleteView
from django.core.urlresolvers import reverse , reverse_lazy
from CAC.serializers import DiabetesSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics,authentication,permissions

def index(request):
    return render(request , 'CAC/index.html' )

def diabetes_prediction(request):
    if(request.method == "POST"):
        diabetes_form = DiabetesPredictionForm(data = request.POST)
        if 1==1 :
            data = []
            data.append(int(request.POST.get('Pregnancies')))
            data.append(int(request.POST.get('Glucose')))
            data.append(int(request.POST.get('BloodPressure')))
            data.append(int(request.POST.get('SkinThickness')) )
            data.append(int(request.POST.get('Insulin')))
            data.append(round(float(request.POST.get('BMI'))*10))
            data.append(round(float(request.POST.get('DiabetesPedigreeFunction') )*1000))
            data.append(int(request.POST.get('Age')))
           
            if(diabetes_form.is_valid()):
                data = data_converter.convert_objects(data)
                print(data)
                res = CAClassifier.classify(data)
                print("result =",res)
                if res > 0 :
                        diabetes = diabetes_form.save(commit=False)
                        diabetes.result = '1'
                        diabetes.user = request.user
                        diabetes.save()
                
                else:
                    diabetes = diabetes_form.save(commit=False)
                    diabetes.result = '0'
                    diabetes.user = request.user
                    diabetes.save()
           
            

                
            
            return render(request, 'CAC/diabetes_prediction.html' , {'diabetes_form':diabetes_form })
        else:
            prediction_form = DiabetesPredictionForm
            return render(request, 'CAC/diabetes_prediction.html' , {'diabetes_form':prediction_form})

    else:
        prediction_form = DiabetesPredictionForm
        return render(request, 'CAC/diabetes_prediction.html' , {'diabetes_form':prediction_form}) 


@login_required
def user_Diabetes_results(request):
    results_list = DiabetesPrediction.objects.filter(user = request.user)
    dict={
        'results_list':results_list,        
    }
    return render(request , 'CAC/diabetes_result_list.html',dict)
    
class delete_diabetes_result(DeleteView):
    model = DiabetesPrediction
    context_object_name = "result"
    template_name = "CAC/delete_diabetes_result.html"
    success_url = reverse_lazy('CAC:diabetes_results')

class DiabetesListAPI(generics.ListAPIView):
    serializer_class = DiabetesSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        print(self.request.META.get('HTTP_AUTHORIZATION'))
        token_str = self.request.META.get('HTTP_AUTHORIZATION').split(" ")
        token = Token.objects.filter(key=token_str[1] ).first()
        user = token.user_id
        return DiabetesPrediction.objects.filter(user=user)
