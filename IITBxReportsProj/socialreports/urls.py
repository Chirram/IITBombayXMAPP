from django.conf.urls import patterns, url
from socialreports import views

urlpatterns = patterns('',	
       url(r'^$',views.index,name="index1"),
       url(r'^gender/$',views.genderwise,name="gender"),
       url(r'^age/$',views.agewise,name="age"),
       url(r'^state/$',views.statewise,name="state"),
       url(r'^education/$',views.educationwise,name="education"),
       #url(r'^state/report$',views.myview,name="convert"),    
       url(r'^subject/$',views.subjectwise,name="subject"),   
              )
