from django.conf.urls import url
from FS import views

#template tagging
app_name = 'FS'

urlpatterns =[
    url(r'^$' , views.upload_csv , name='upload_csv'),
    url(r'^register/$' , views.register , name = 'register') ,
    url(r'^login/$' , views.user_login , name = 'user_login') ,
    url(r'^results/$' , views.user_FS_results , name = 'results') ,
    url(r'^download_csv/(?P<result_id>\d+)/$', views.download_csv, name='download_csv'),
    url(r'^delete/(?P<pk>\d+)/$' , views.delete_result.as_view() , name="delete_result"),
    url('rest/', views.FSList.as_view(),name="rest"),
    url('userrest/', views.UserAPIList.as_view(),name="userrest"),
    url('create-user' , views.create_user_API.as_view(),name="create_user"),
    url('token/',views.create_token_view.as_view(),name="token"),
    url('me/',views.ManageUserView.as_view(),name="me"),
 
]