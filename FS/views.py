from django.shortcuts import render
from django.core.urlresolvers import reverse , reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth import authenticate , logout
from django.contrib.auth import  login as login_fun 
import logging
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from FS import BBH3
from FS.models import FS
from FS.forms import FSForm  ,UserForm
from django.views.generic import ListView ,DeleteView
import csv
from FS.serializer import FSSerializer , UserSerializer ,AuthTokenSerializer
from rest_framework import generics,authentication,permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
# Create your views here.

def index(request):
    render()


@login_required
def user_logout(requset):
    logout(requset)
    return HttpResponseRedirect(reverse('CAC:index'))

def register(requset):
    registered = False
    if(requset.method == 'POST'):
        user_form = UserForm(data = requset.POST)
        

        if user_form.is_valid() :
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            register = True
            return HttpResponseRedirect(reverse("FS:user_login"))
						
        else:
            
            dict = {
        'user_form':user_form,
        'registered':registered

             }

            return render(requset , 'FS/register.html',dict)
    else:
        user_form = UserForm
      

    dict = {
        'user_form':user_form,
        'registered':registered

    }

    return render(requset , 'FS/register.html',dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username= username ,password = password)

        if user :
            if user.is_active:
                login_fun(request , user)
                return HttpResponseRedirect(reverse('CAC:index'))
            else:
                data_dict={'error_message':"User not Active"};return render(request, 'FS/login.html',data_dict)
        else:
            data_dict={'error_message':"Invalid Credentials"};return render(request, 'FS/login.html',data_dict)
    else:
        return render(request , 'FS/login.html')
	


@login_required
def upload_csv(request):
	if request.method == 'GET':
		return render(request, 'FS/upload_csv.html')
	if request.method == 'POST':
		
			csv_file = request.FILES["csv_file"]
			if not csv_file.name.endswith('.csv'):
				data_dict={'error_message':"CSV file required"};return render(request, 'FS/upload_csv.html',data_dict)
			if csv_file.multiple_chunks():
				data_dict={'error_message':"File too big"};return render(request, 'FS/upload_csv.html',data_dict)
			try:
				old_accuracy , feat_num , new_accuracy, new_features , new_ds = BBH3.FS(csv_file)
		
				
				res = FS()
				res.csv = new_ds
				res.name = csv_file.name
				res.new_accurcay = new_accuracy
				res.old_accuracy = old_accuracy
				res.old_features = feat_num
				res.new_features = new_features
				res.user = request.user
				res.save()
				
				
				
			except Exception as e:
				data_dict={'error_message':"Error occured"+str(e)};return render(request, 'FS/upload_csv.html',data_dict)

                

	return HttpResponseRedirect(reverse("FS:results"))


class resultsList(ListView):
	model = FS
	context_object_name = "results_list"

@login_required
def user_FS_results(request):
    results_list = FS.objects.filter(user = request.user)
    dict={
        'results_list':results_list,        
    }
    return render(request , 'FS/fs_list.html',dict)
    

@login_required
def download_csv(request , result_id):
    file = FS.objects.filter(id= result_id)[0]
    response = HttpResponse(file.csv,content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+file.name+ '"'
    return response


class delete_result(DeleteView):
    model = FS
    context_object_name = "result"
    template_name = "FS/delete_result.html"
    success_url = reverse_lazy('FS:results')


class FSList(generics.ListAPIView):
    serializer_class = FSSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        print(self.request.META.get('HTTP_AUTHORIZATION'))
        token_str = self.request.META.get('HTTP_AUTHORIZATION').split(" ")
        token = Token.objects.filter(key=token_str[1] ).first()
        user = token.user_id
        return FS.objects.filter(user=user)


class UserAPIList(generics.ListCreateAPIView):
    serializer_class = UserSerializer


class create_user_API(generics.CreateAPIView):
    serializer_class = UserSerializer


class create_token_view(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self):
        return self.request.user


class FSListAPI(generics.ListAPIView):
    serializer_class = FSSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        print(self.request.META.get('HTTP_AUTHORIZATION'))
        token_str = self.request.META.get('HTTP_AUTHORIZATION').split(" ")
        token = Token.objects.filter(key=token_str[1] ).first()
        user = token.user_id
        return FS.objects.filter(user=user)