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
            return HttpResponseRedirect(reverse("FS:login"))
						
        else:
            print(user_form.errors)
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
                return HttpResponse('Account Not Active')
        else:
            print('someone failde login')
            print('Username :{} and password :{}'.format(username , password))
            return HttpResponse('Invalid Credentials')
    else:
        return render(request , 'FS/login.html')
	


@login_required
def upload_csv(request):
	if request.method == 'GET':
		return render(request, 'FS/upload_csv.html')
	if request.method == 'POST':
		
			csv_file = request.FILES["csv_file"]
			if not csv_file.name.endswith('.csv'):
				messages.error(request,'File is not CSV type')
			if csv_file.multiple_chunks():
				messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
				return HttpResponseRedirect(reverse("FS:upload_csv"))
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
				logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))

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


class FSList(generics.ListCreateAPIView):
    queryset = FS.objects.all()
    serializer_class = FSSerializer


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