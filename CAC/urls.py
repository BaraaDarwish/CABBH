from django.conf.urls import url
from CAC import views


#template tagging
app_name = 'CAC'


urlpatterns =[
    url(r'^$' , views.index , name='index'),
    url(r'^diabetes-prediction/' , views.diabetes_prediction , name="diabetes_prediction"),
    url(r'^diabetes-results/$' , views.user_Diabetes_results , name = 'diabetes_results') ,
    url(r'^delete-diabetes/(?P<pk>\d+)/$' , views.delete_diabetes_result.as_view() , name="delete_diabetes_result"),
    url(r'^diabetes-results-api/' , views.DiabetesListAPI.as_view() , name = 'diabetes_results_api') ,    
    
]